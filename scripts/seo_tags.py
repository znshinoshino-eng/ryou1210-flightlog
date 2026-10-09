"""Add search and sharing tags to any page that doesn't have them yet.

Run by the GitHub Action on every page change, so new articles get:
canonical URL, Open Graph / Twitter card tags, and Article structured data.
Pages that already have a canonical link are left untouched.
"""
import html
import json
import pathlib
import re
import subprocess

from pages import BASE, all_pages, lang_of, url_of
SITE = "Flightlog Japan"
root = pathlib.Path(__file__).resolve().parent.parent


def text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def git_date(path, fmt):
    out = subprocess.run(["git", "log", fmt, "--", str(path)], cwd=root,
                         capture_output=True, text=True).stdout.strip().splitlines()
    return out


changed = 0
pages = all_pages()
LOCALE = {"en": "en_US", "fr": "fr_FR", "de": "de_DE", "es": "es_ES"}
for p in pages:
    if not p.exists():
        continue
    s = p.read_text(encoding="utf-8")
    if 'rel="canonical"' in s or "</head>" not in s:
        continue
    rel = p.relative_to(root).as_posix()
    url = url_of(rel)
    lang = lang_of(rel)
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    title = text(m.group(1)) if m else SITE
    m = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
    desc = html.unescape(m.group(1)) if m else ""
    m = re.search(r'<figure class="hero-img">\s*<img src="([^"]+)"', s)
    image = html.unescape(m.group(1)) if m else ""
    is_article = "articles/" in rel
    h1 = re.search(r"<h1>(.*?)</h1>", s, re.S)
    headline = text(h1.group(1)) if h1 else title

    e = lambda v: html.escape(v, quote=True)
    tags = [
        f'<link rel="canonical" href="{e(url)}">',
        f'<meta property="og:site_name" content="{SITE}">',
        f'<meta property="og:type" content="{"article" if is_article else "website"}">',
        f'<meta property="og:title" content="{e(headline if is_article else title)}">',
        f'<meta property="og:description" content="{e(desc)}">',
        f'<meta property="og:url" content="{e(url)}">',
        f'<meta property="og:locale" content="{LOCALE[lang]}">',
    ]
    if image:
        tags.append(f'<meta property="og:image" content="{e(image)}">')
    tags.append(f'<meta name="twitter:card" content="{"summary_large_image" if image else "summary"}">')

    if is_article:
        dates = git_date(p, "--format=%cI")
        data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": headline[:110],
            "description": desc,
            "inLanguage": lang,
            "mainEntityOfPage": url,
            "publisher": {"@type": "Organization", "name": SITE, "url": BASE},
            "author": {"@type": "Person", "name": "Ryo", "url": BASE + "about.html"},
        }
        if image:
            data["image"] = [image]
        if dates:
            data["dateModified"] = dates[0]
            data["datePublished"] = dates[-1]
        tags.append('<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>")
    elif rel.endswith("index.html"):
        data = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": url, "inLanguage": lang, "description": desc}
        tags.append('<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>")

    s = s.replace("</head>", "\n".join(tags) + "\n</head>", 1)
    p.write_text(s, encoding="utf-8")
    changed += 1

print(f"{changed} pages updated")
