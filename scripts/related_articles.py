"""Write a "Keep reading" block of related guides into every article, as plain HTML.

Search engines read it directly (no JavaScript needed), and every guide gets links
from the guides closest to it in topic, not just from the first cards on the top page.

How guides are picked (data comes from the cards on each language's index page):
  - same top-page section (Start here / Getting around / ...)  +3
  - each shared area in data-region (tokyo, kansai, ...)        +2
  - shared words in the card title and excerpt                  +1 each (max 6)
  - a link the article body already has to that guide           -2 (no need to repeat it)
Ties go to the guide with the fewest "Keep reading" links so far, so links spread out.

Rewritten on every run, so new articles get a block (and appear in others) automatically.
Run by the GitHub Action.
"""
import html
import re
from pages import root, LANGS

COUNT = 6
START, END = "<!-- related:start -->", "<!-- related:end -->"
HEADING = {"en": "Keep reading", "fr": "À lire aussi", "de": "Weiterlesen",
           "es": "Sigue leyendo", "th": "อ่านต่อ", "zh": "延伸閱讀"}
STOP = set("""a an and the of to in on for from with by or vs is are your you what which how
when where why it its at as be can do not no but more most all one two into than this that
these those there their they them our we explained guide guides japan japanese tokyo
should actually worth really step simple""".split())

CARD = re.compile(r'<a class="post-card[^"]*" href="articles/([^"]+)"(?: data-region="([^"]*)")?>(.*?)</a>', re.S)


def words(text):
    return {w for w in re.findall(r"[a-z0-9]+", html.unescape(text).lower()) if len(w) > 2 and w not in STOP}


def read_cards(index_path):
    s = index_path.read_text(encoding="utf-8")
    sections = [(m.start(), m.group(1)) for m in re.finditer(r'<section class="post-section" id="([^"]+)"', s)]
    cards = {}
    for m in CARD.finditer(s):
        slug, region, body = m.group(1), m.group(2) or "", m.group(3)
        sec = ""
        for pos, sid in sections:
            if pos < m.start():
                sec = sid
        get = lambda pat: (re.search(pat, body, re.S) or [None, ""])[1].strip()
        cards[slug] = {
            "slug": slug,
            "section": sec,
            "regions": set(region.split()) - {"japan"},
            "thumb": get(r'<img class="thumb" src="([^"]+)"'),
            "cat": get(r'<div class="cat">(.*?)</div>'),
            "title": get(r"<h2>(.*?)</h2>"),
            "words": words(get(r"<h2>(.*?)</h2>") + " " + get(r'<p class="excerpt">(.*?)</p>')),
        }
    return cards


def score(a, b, body_links):
    s = 3 if a["section"] and a["section"] == b["section"] else 0
    s += 2 * len(a["regions"] & b["regions"])
    s += min(6, len(a["words"] & b["words"]))
    if b["slug"] in body_links:
        s -= 2
    return s


def block(lang, picks):
    items = []
    for c in picks:
        img = (f'<img src="{c["thumb"]}" alt="" loading="lazy" width="720" height="405">' if c["thumb"] else "")
        cat = f'<span class="rcat">{c["cat"]}</span>' if c["cat"] else ""
        items.append(f'      <a class="related-card" href="{c["slug"]}">{img}{cat}'
                     f'<span class="rtitle">{c["title"]}</span></a>')
    return (f'{START}\n  <section class="related" aria-labelledby="related-h">\n'
            f'    <h2 id="related-h">{HEADING[lang]}</h2>\n    <div class="related-list">\n'
            + "\n".join(items) + "\n    </div>\n  </section>\n  " + END + "\n")


def run(lang):
    base = root if lang == "en" else root / lang
    index = base / "index.html"
    if not index.exists():
        return 0
    cards = read_cards(index)
    inbound = {slug: 0 for slug in cards}
    changed = 0
    for slug in sorted(cards):
        page = base / "articles" / slug
        if not page.exists():
            continue
        s = page.read_text(encoding="utf-8")
        s_clean = re.sub(r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"\n", "", s, flags=re.S)
        if '<a class="back-link"' not in s_clean:
            continue
        body_links = set(re.findall(r'href="([a-z0-9-]+\.html)"', s_clean))
        me = cards[slug]
        others = [c for c in cards.values() if c["slug"] != slug and (base / "articles" / c["slug"]).exists()]
        others.sort(key=lambda c: (-score(me, c, body_links), inbound[c["slug"]], c["slug"]))
        picks = others[:COUNT]
        for c in picks:
            inbound[c["slug"]] += 1
        if not picks:
            new = s_clean
        else:
            new = re.sub(r'([ \t]*)<a class="back-link"', lambda m: "  " + block(lang, picks) + m.group(0), s_clean, count=1)
        if new != s:
            page.write_text(new, encoding="utf-8")
            changed += 1
    return changed


total = sum(run(lang) for lang in ["en"] + LANGS)
print(f"related articles: {total} pages updated")
