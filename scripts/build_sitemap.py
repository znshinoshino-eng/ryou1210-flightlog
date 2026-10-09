"""Write sitemap.xml listing every page on the site (run by the GitHub Action)."""
import pathlib, subprocess, datetime

from pages import all_pages, root, url_of

def lastmod(path):
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
