"""Link each page to its translations with hreflang tags (rewritten on every run)."""
import re
from pages import all_pages, root, lang_of, base_rel, url_of

START, END = "<!-- hreflang:start -->", "<!-- hreflang:end -->"
pages = all_pages()
groups = {}
for p in pages:
    rel = p.relative_to(root).as_posix()
    groups.setdefault(base_rel(rel), {})[lang_of(rel)] = rel

changed = 0
for p in pages:
    rel = p.relative_to(root).as_posix()
    versions = groups[base_rel(rel)]
    s = p.read_text(encoding="utf-8")
    s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
    if len(versions) > 1:
        order = ["en", "fr", "de", "es", "th"]
        tags = [f'<link rel="alternate" hreflang="{l}" href="{url_of(versions[l])}">' for l in order if l in versions]
        if "en" in versions:
            tags.append(f'<link rel="alternate" hreflang="x-default" href="{url_of(versions["en"])}">')
        s = s.replace("</head>", START + "\n" + "\n".join(tags) + "\n" + END + "\n</head>", 1)
    if s != p.read_text(encoding="utf-8"):
        p.write_text(s, encoding="utf-8")
        changed += 1
print(f"hreflang: {changed} pages updated")
