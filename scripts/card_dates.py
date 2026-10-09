"""Show each guide's last-updated date on the article cards of every index page.

Dates come from git history (last commit that touched the article), so they stay
honest without anyone editing them by hand. Run by the GitHub Action.
"""
import datetime
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
    m = MONTHS[lang][d.month - 1]
    if lang == "en":
        return f"Updated {m} {d.day}, {d.year}"
    if lang == "fr":
        return f"Mis à jour le {d.day} {m} {d.year}"
    if lang == "de":
        return f"Aktualisiert am {d.day}. {m} {d.year}"
    if lang == "es":
        return f"Actualizado el {d.day} {m} {d.year}"
    return f"อัปเดต {d.day} {m} {d.year + 543}"


def last_changed(path):
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
