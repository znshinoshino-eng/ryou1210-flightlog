"""Show the official pages each guide was checked against, as a visible "Sources" list.

Every article already carries an HTML comment `<!-- sources: url | url | ... -->` written when
the guide was researched. Readers (and search engines) can't see comments, so this script adds a
plain-HTML list right after it. The list is rewritten on every run from the comment, so the
comment stays the single source of truth. Photo pages (Unsplash) and affiliate/booking links are
left out: the list is only for the official pages behind the facts. Run by the GitHub Action.
"""
import html
import re
from urllib.parse import urlparse

from pages import all_pages, root, lang_of

START, END = "<!-- sources-box:start -->", "<!-- sources-box:end -->"
MAX_ORGS = 8
PER_ORG = 4
SKIP_HOSTS = ("unsplash.com", "klook.com", "google.com", "apps.apple.com", "play.google.com")

HEADING = {"en": "Sources", "fr": "Sources", "de": "Quellen", "es": "Fuentes",
           "th": "แหล่งข้อมูล", "zh": "資料來源"}
NOTE = {
    "en": "Official pages we checked the facts in this guide against. Fares and rules can change, so check them before you travel.",
    "fr": "Pages officielles utilisées pour vérifier les informations de ce guide. Tarifs et règles peuvent changer : vérifiez-les avant de partir.",
    "de": "Offizielle Seiten, mit denen die Angaben in diesem Ratgeber geprüft wurden. Preise und Regeln können sich ändern – bitte vor der Reise prüfen.",
    "es": "Páginas oficiales con las que comprobamos los datos de esta guía. Las tarifas y normas pueden cambiar: compruébalas antes de viajar.",
    "th": "หน้าเว็บทางการที่ใช้ตรวจสอบข้อมูลในบทความนี้ ค่าโดยสารและกฎอาจเปลี่ยนแปลงได้ โปรดตรวจสอบก่อนเดินทาง",
    "zh": "本文資訊所核對的官方網頁。票價與規定可能變動，出發前請再次確認。",
}
NAMES = {
    "jreast.co.jp": "JR East", "media.jreast.co.jp": "JR East", "timetables.jreast.co.jp": "JR East timetables",
    "global.jr-central.co.jp": "JR Central", "jr-central.co.jp": "JR Central", "smart-ex.jp": "smart EX (JR Central)",
    "westjr.co.jp": "JR West", "japanrailpass.net": "Japan Rail Pass (official)",
    "tokyometro.jp": "Tokyo Metro", "kotsu.metro.tokyo.jp": "Toei (Tokyo Metropolitan Bureau of Transportation)",
    "tokyo-haneda.com": "Haneda Airport", "narita-airport.jp": "Narita Airport",
    "kansai-airport.or.jp": "Kansai Airport", "mlit.go.jp": "Ministry of Land, Infrastructure, Transport and Tourism",
    "nankai.co.jp": "Nankai Electric Railway", "japan.travel": "JNTO (Japan National Tourism Organization)",
    "kate.co.jp": "Keisei Electric Railway", "kuronekoyamato.co.jp": "Yamato Transport",
    "shinjuku-busterminal.co.jp": "Busta Shinjuku", "city.kyoto.lg.jp": "Kyoto City",
    "www2.city.kyoto.lg.jp": "Kyoto City", "tobu.co.jp": "Tobu Railway", "odakyu-global.com": "Odakyu",
    "customs.go.jp": "Japan Customs", "kyoto.travel": "Kyoto City Tourism", "nta.go.jp": "National Tax Agency",
    "kintetsu.co.jp": "Kintetsu", "ana.co.jp": "ANA", "jal.co.jp": "JAL", "sagano-kanko.co.jp": "Sagano Scenic Railway",
    "pasmo.co.jp": "PASMO", "limousinebus.co.jp": "Airport Limousine Bus", "keikyu.co.jp": "Keikyu",
    "tokyo-monorail.co.jp": "Tokyo Monorail", "osakametro.co.jp": "Osaka Metro", "usj.co.jp": "Universal Studios Japan",
    "jreast-shinkansen-reservation.eastjr.co.jp": "JR East (eki-net)", "eki-net.com": "JR East (eki-net)",
    "kyotobus.jp": "Kyoto Bus", "hakonenavi.jp": "Odakyu Hakone", "odakyu.jp": "Odakyu",
}


def org_of(url):
    host = (urlparse(url).hostname or "").lower()
    bare = host[4:] if host.startswith("www.") else host
    return NAMES.get(host) or NAMES.get(bare) or bare


def page_label(url):
    """Short, readable name for one page: the last part of its address."""
    path = urlparse(url).path.rstrip("/")
    last = path.rsplit("/", 1)[-1] if path else ""
    last = re.sub(r"\.(html?|php|aspx?)$", "", last)
    last = re.sub(r"[-_]+", " ", last).strip()
    if not last or last.lower() == "index":
        last = (urlparse(url).hostname or "").removeprefix("www.")
    return last[:40] + ("…" if len(last) > 40 else "")


def urls_from(comment):
    seen, out = set(), []
    for raw in comment.split("|"):
        url = html.unescape(raw.strip())
        if not re.match(r"https?://", url) or url in seen:
            continue
        host = (urlparse(url).hostname or "").lower()
        if any(host == h or host.endswith("." + h) for h in SKIP_HOSTS):
            continue
        seen.add(url)
        out.append(url)
    return out


def build(lang, urls):
    groups = {}
    for url in urls:
        links = groups.setdefault(org_of(url), [])
        # Same page in two languages (…/en/x.html and …/x.html) is listed once.
        if all(page_label(u) != page_label(url) for u in links):
            links.append(url)
    items = []
    for org, links in list(groups.items())[:MAX_ORGS]:
        parts = [f'<a href="{html.escape(u, quote=True)}" target="_blank" rel="noopener">{html.escape(page_label(u))}</a>'
                 for u in links[:PER_ORG]]
        items.append(f"      <li><strong>{html.escape(org)}</strong>: " + " · ".join(parts) + "</li>")
    return (f"{START}\n  <section class=\"sources\" aria-labelledby=\"sources-h\">\n"
            f"    <h2 id=\"sources-h\">{HEADING[lang]}</h2>\n"
            f"    <p class=\"sources-note\">{NOTE[lang]}</p>\n    <ul>\n"
            + "\n".join(items) + "\n    </ul>\n  </section>\n  " + END + "\n")


changed = 0
for p in all_pages():
    rel = p.relative_to(root).as_posix()
    if "articles/" not in rel:
        continue
    s = p.read_text(encoding="utf-8")
    clean = re.sub(r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"\n", "", s, flags=re.S)
    m = re.search(r"([ \t]*)<!-- sources:(.*?)-->\n?", clean, re.S)
    new = clean
    if m:
        urls = urls_from(m.group(2))
        if urls:
            box = build(lang_of(rel), urls)
            # Put the list just above "Keep reading" / the back link, so it ends the guide itself.
            anchor = re.search(r"[ \t]*(<!-- related:start -->|<a class=\"back-link\")", clean)
            if anchor:
                new = clean[:anchor.start()] + "  " + box + clean[anchor.start():]
            else:
                new = clean[:m.end()] + ("" if clean[m.end() - 1] == "\n" else "\n") + "  " + box + clean[m.end():]
    if new != s:
        p.write_text(new, encoding="utf-8")
        changed += 1
print(f"sources: {changed} pages updated")
