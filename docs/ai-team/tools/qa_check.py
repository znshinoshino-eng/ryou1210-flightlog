"""Flightlog Japan QA check (used by the AI team's QA step).

Serves the repo locally, opens every page at phone (390px) and desktop (1280px)
width in headless Chromium, and reports:
  - horizontal overflow (page wider than the screen)
  - JavaScript errors (uncaught errors and console.error)
  - broken internal links (href to a local file that does not exist)
  - images without alt text
  - accessibility violations from axe-core (if --axe path is given)
External requests (images, ads, analytics) are blocked, so only the site's own
code is tested.

Usage:
  python3 docs/ai-team/tools/qa_check.py [--axe path/to/axe.min.js] [--shots DIR] [--pages glob ...]
Exit code 1 if any error-level problem is found.
"""
import argparse, glob, http.server, json, os, socketserver, sys, threading
from urllib.parse import urlparse, unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SKIP = ("google", "d03675700b")  # search-console verification files


def serve(port):
    os.chdir(ROOT)
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=ROOT, **k)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    handler_cls = httpd.RequestHandlerClass
    http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def pages(patterns):
    out = []
    for p in patterns:
        out += glob.glob(os.path.join(ROOT, p), recursive=True)
    return sorted({os.path.relpath(f, ROOT) for f in out if not os.path.basename(f).startswith(SKIP)})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--axe")
    ap.add_argument("--shots")
    ap.add_argument("--port", type=int, default=8799)
    ap.add_argument("--pages", nargs="*", default=["*.html", "articles/*.html", "*/index.html", "*/articles/*.html"])
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright

    serve(a.port)
    base = f"http://127.0.0.1:{a.port}/"
    axe_src = open(a.axe).read() if a.axe else None
    problems, axe_counts = [], {}
    files = pages(a.pages)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for width in (390, 1280):
            ctx = b.new_context(viewport={"width": width, "height": 900})
            ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
            page = ctx.new_page()
            errs = []
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.on("console", lambda m: errs.append(m.text) if m.type == "error" and "net::ERR_FAILED" not in m.text and "Failed to load resource" not in m.text else None)
            for f in files:
                errs.clear()
                page.goto(base + f, wait_until="load")
                page.wait_for_timeout(300)
                sw = page.evaluate("document.documentElement.scrollWidth")
                if sw > width + 1:
                    problems.append(("error", f, width, f"horizontal overflow: page is {sw}px wide"))
                for e in errs:
                    problems.append(("error", f, width, "JS error: " + e[:200]))
                if width == 390:
                    links = page.evaluate("[...document.querySelectorAll('a[href]')].map(a=>a.href)")
                    for href in set(links):
                        u = urlparse(href)
                        if href.startswith(base) and not u.fragment:
                            path = os.path.join(ROOT, unquote(u.path.lstrip("/")))
                            if path.endswith("/"):
                                path += "index.html"
                            if not os.path.exists(path):
                                problems.append(("error", f, width, "broken link: " + u.path))
                    noalt = page.evaluate("[...document.querySelectorAll('img:not([alt])')].length")
                    if noalt:
                        problems.append(("warn", f, width, f"{noalt} image(s) without alt"))
                if axe_src:
                    page.add_script_tag(content=axe_src)
                    res = page.evaluate("axe.run(document,{resultTypes:['violations']}).then(r=>r.violations.map(v=>[v.id,v.impact,v.nodes[0].target.join(' ')+' '+v.nodes[0].html.slice(0,80)]))")
                    for vid, impact, sample in res:
                        key = (vid, impact)
                        axe_counts.setdefault(key, set()).add(f"{f} @{width}: {sample}")
                if a.shots and f in ("index.html", files[min(5, len(files) - 1)]):
                    os.makedirs(a.shots, exist_ok=True)
                    page.screenshot(path=os.path.join(a.shots, f.replace("/", "_") + f"-{width}.png"), full_page=True)
            ctx.close()
        b.close()

    print(f"Checked {len(files)} pages at 390px and 1280px.")
    for lvl, f, w, msg in problems:
        print(f"[{lvl}] {f} @{w}: {msg}")
    if axe_src:
        print("axe-core violations (rule, impact: pages affected):")
        for (vid, impact), fs in sorted(axe_counts.items(), key=lambda x: -len(x[1])):
            print(f"  {vid} ({impact}): {len({x.split(' @')[0] for x in fs})} pages, e.g. {sorted(fs)[0]}")
    errors = [x for x in problems if x[0] == "error"]
    print(f"RESULT: {'FAIL' if errors else 'PASS'} ({len(errors)} errors, {len(problems) - len(errors)} warnings)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
