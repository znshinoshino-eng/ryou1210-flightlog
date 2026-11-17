"""Show each guide's last-updated date on the article cards of every index page.

Dates come from git history (last commit that touched the article), so they stay
honest without anyone editing them by hand. Run by the GitHub Action.
"""
import datetime
import json
import pathlib
import re
import subprocess
from pages import root, LANGS

MONTHS = {
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "fr": ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."],
    "de": ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Okt.", "Nov.", "Dez."],
    "es": ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sept.", "oct.", "nov.", "dic."],
    "th": ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."],
}


def label(lang, d):
    m = MONTHS.get(lang, MONTHS["en"])[d.month - 1]
    if lang == "en":
        return f"Updated {m} {d.day}, {d.year}"
    if lang == "fr":
        return f"Mis à jour le {d.day} {m} {d.year}"
    if lang == "de":
        return f"Aktualisiert am {d.day}. {m} {d.year}"
    if lang == "es":
        return f"Actualizado el {d.day} {m} {d.year}"
    if lang == "zh":
        return f"更新於 {d.year}年{d.month}月{d.day}日"
    return f"อัปเดต {d.day} {m} {d.year + 543}"


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
    try:
        return datetime.date.fromisoformat(dm) if dm else None
    except ValueError:
        return None


def last_changed(path):
    out = subprocess.run(["git", "log", "-1", "--format=%cs", *SKIP_BOT, "--", str(path)],
                         cwd=root, capture_output=True, text=True).stdout.strip()
    if out:
        return datetime.date.fromisoformat(out)
    # No real content edit in git: trust the article's own structured data,
    # then the last commit of any kind, so the card never claims a refresh
    # that didn't happen.
    dated = ldjson_date(path)
    if dated:
        return dated
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(path)],
                         cwd=root, capture_output=True, text=True).stdout.strip()
    return datetime.date.fromisoformat(out) if out else datetime.date.today()


changed = 0
for lang in ["en"] + LANGS:
    index = root / "index.html" if lang == "en" else root / lang / "index.html"
    if not index.exists():
        continue
    s = index.read_text(encoding="utf-8")

    def add_date(m):
        card = m.group(0)
        href = re.search(r'href="([^"]+)"', card).group(1)
        d = last_changed(index.parent / href)
        tag = f'<time class="card-date" datetime="{d.isoformat()}">{label(lang, d)}</time>'
        card = re.sub(r'\s*<time class="card-date"[^>]*>.*?</time>', "", card)
        return card.replace("</a>", f"      {tag}\n    </a>", 1)

    new = re.sub(r'<a class="post-card[^"]*" href="[^"]+".*?</a>', add_date, s, flags=re.S)
    if new != s:
        index.write_text(new, encoding="utf-8")
        changed += 1
print(f"card dates: {changed} index pages updated")
