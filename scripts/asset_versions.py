"""Add ?v=<hash> to style.css and site.js links so browsers load the new file
as soon as it changes (instead of showing a cached old design)."""
import hashlib
import re
from pages import all_pages, root

ver = {}
for name in ("style.css", "site.js"):
    ver[name] = hashlib.sha1((root / name).read_bytes()).hexdigest()[:8]

changed = 0
for p in all_pages():
    s = p.read_text(encoding="utf-8")
    new = s
    for name, v in ver.items():
        new = re.sub(r'((?:\.\./)*' + re.escape(name) + r')(\?v=[0-9a-f]+)?"', r'\1?v=' + v + '"', new)
    if new != s:
        p.write_text(new, encoding="utf-8")
        changed += 1
print(f"asset versions: {changed} pages updated", ver)
