"""Shared list of site pages, including translated copies under fr/, de/, es/."""
import pathlib

BASE = "https://znshinoshino-eng.github.io/ryou1210-flightlog/"
LANGS = ["fr", "de", "es"]          # translated languages; English lives at the root
root = pathlib.Path(__file__).resolve().parent.parent


def all_pages():
    pages = [root / "index.html", root / "about.html", root / "privacy.html"]
    pages += sorted((root / "articles").glob("*.html"))
    for lang in LANGS:
        d = root / lang
        if d.is_dir():
            pages += [p for p in [d / "index.html"] if p.exists()]
            pages += sorted((d / "articles").glob("*.html")) if (d / "articles").is_dir() else []
    return [p for p in pages if p.exists()]


def lang_of(rel):
    first = rel.split("/", 1)[0]
    return first if first in LANGS else "en"


def base_rel(rel):
    """Path of the page without its language folder: 'fr/articles/x.html' -> 'articles/x.html'."""
    lang = lang_of(rel)
    return rel[len(lang) + 1:] if lang != "en" else rel


def url_of(rel):
    if rel == "index.html":
        return BASE
    if rel.endswith("/index.html"):
        return BASE + rel[: -len("index.html")]
    return BASE + rel
