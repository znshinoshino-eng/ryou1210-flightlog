"""Make sure every page links the site icon (browser tab, bookmarks, Google results)."""
from pages import all_pages, root

changed = 0
for p in all_pages():
    rel = p.relative_to(root).as_posix()
    s = p.read_text(encoding="utf-8")
    if 'rel="icon"' in s:
        continue
    up = "../" * rel.count("/")
    tags = (f'<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">\n'
            f'<link rel="icon" href="{up}favicon-48.png" sizes="48x48" type="image/png">\n'
            f'<link rel="icon" href="{up}favicon-192.png" sizes="192x192" type="image/png">\n'
            f'<link rel="apple-touch-icon" href="{up}apple-touch-icon.png">\n')
    s = s.replace('<link rel="stylesheet"', tags + '<link rel="stylesheet"', 1)
    p.write_text(s, encoding="utf-8")
    changed += 1
print(f"icons: {changed} pages updated")
