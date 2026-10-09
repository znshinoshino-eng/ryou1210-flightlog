"""Put the guide-section bar (Start here / Getting around / ...) under the header of every English page.

The bar is plain HTML (not added by JavaScript) so search engines can read it.
Rewritten on every run, so changing SECTIONS here updates all pages.
"""
import re
from pages import all_pages, root, lang_of

# (section id, label on wider screens, shorter label on phones)
SECTIONS = [
    ("first-trip", "Start here", "Start here"),
    ("getting-around", "Getting around", "Transit"),
    ("sightseeing", "Sightseeing", "Sightseeing"),
    ("plane-spotting", "Plane spotting", "Plane spotting"),
]
START, END = "<!-- section-nav:start -->", "<!-- section-nav:end -->"

changed = 0
for p in all_pages():
    rel = p.relative_to(root).as_posix()
    if lang_of(rel) != "en":
        continue
    s = p.read_text(encoding="utf-8")
    if "</header>" not in s:
        continue
    up = "../" * rel.count("/")
    links = "\n".join(
        (f'      <a href="{up}index.html#{sid}">{label}</a>' if label == short else
         f'      <a href="{up}index.html#{sid}"><span class="nav-long">{label}</span><span class="nav-short">{short}</span></a>')
        for sid, label, short in SECTIONS
    )
    block = (f'{START}\n  <nav class="section-nav" aria-label="Guide sections">\n    <div class="wrap">\n'
             f'{links}\n    </div>\n  </nav>\n  {END}\n')
    new = re.sub(r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"\n", "", s, flags=re.S)
    new = new.replace("</header>", "  " + block + "</header>", 1)
    if new != s:
        p.write_text(new, encoding="utf-8")
        changed += 1
print(f"section nav: {changed} pages updated")
