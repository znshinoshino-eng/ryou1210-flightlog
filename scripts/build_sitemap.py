"""Write sitemap.xml listing every page on the site (run by the GitHub Action)."""
import json
import pathlib, re, subprocess, datetime

from pages import all_pages, root, url_of

# Commits made by the GitHub Action only refresh shared blocks (related guides, tags,
# sources list) on every page; they are not content updates, so they don't count as
# "last updated" (otherwise every page would look freshly updated every day).
SKIP_BOT = ["--invert-grep", "--grep=^Update sitemap and search tags$"]

def ldjson_date(path):
    """dateModified from the article's own structured data, if it has one."""
    try:
        s = pathlib.Path(path).read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    if not m:
        return None
    try:
        data = json.loads(m.group(1))
    except ValueError:
        return None
    dm = data.get("dateModified", "")[:10] if isinstance(data, dict) else ""
    return dm or None

def lastmod(path):
    out = subprocess.run(["git", "log", "-1", "--format=%cs", *SKIP_BOT, "--", str(path)],
                         cwd=root, capture_output=True, text=True).stdout.strip()
    if out:
        return out
    # No real content edit in git: trust the article's own structured data,
    # then the last commit of any kind, so the sitemap never claims a refresh
    # that didn't happen.
    dated = ldjson_date(path)
    if dated:
        return dated
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(path)],
                         cwd=root, capture_output=True, text=True).stdout.strip()
    return out or datetime.date.today().isoformat()

pages = all_pages()

rows = []
for p in pages:
    if not p.exists():
        continue
    rel = p.relative_to(root).as_posix()
    url = url_of(rel)
    rows.append(f"  <url><loc>{url}</loc><lastmod>{lastmod(p)}</lastmod></url>")

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + "\n".join(rows) + "\n</urlset>\n")
(root / "sitemap.xml").write_text(xml, encoding="utf-8")
print(f"{len(rows)} URLs written")
