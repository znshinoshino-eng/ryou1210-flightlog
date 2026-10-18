"""Tell Bing (and other IndexNow engines: Yandex, Naver, Seznam...) about pages that changed in this push.

IndexNow lets a site announce new or updated URLs instantly instead of waiting for a crawl.
Ownership is proven by the key file at the site root (d03675700b33ad5155498239f1981202.txt).
Run by the GitHub Action with BEFORE=<sha before the push>. Never fails the build.
"""
import json, os, subprocess, sys, urllib.request
from pages import root, url_of, all_pages

KEY = "d03675700b33ad5155498239f1981202"
HOST = "flightlogjapan.com"
before = os.environ.get("BEFORE", "")
if not before or set(before) == {"0"}:
    before = "HEAD~1"
try:
    out = subprocess.run(["git", "diff", "--name-only", before, "HEAD", "--", "*.html"],
                         cwd=root, capture_output=True, text=True, check=True).stdout.split()
except Exception as e:
    print("indexnow: could not diff:", e); sys.exit(0)
urls = sorted({url_of(p) for p in out if (root / p).exists() and not p.startswith("google")})
if os.environ.get("ALL") == "true":   # manual run: send every page
    urls = sorted(url_of(p.relative_to(root).as_posix()) for p in all_pages())
if not urls:
    print("indexnow: nothing to send"); sys.exit(0)
body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"indexnow: sent {len(urls)} URLs, HTTP {r.status}")
except Exception as e:
    print("indexnow: send failed (ignored):", e)
