"""Add the Google AdSense tag to any page that doesn't have it yet.

Run by the GitHub Action on every page change, so new articles get ads automatically.
"""
import pathlib

from pages import all_pages

CLIENT = "ca-pub-8106228067608731"
TAG = (f'<meta name="google-adsense-account" content="{CLIENT}">\n'
       f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={CLIENT}" '
       'crossorigin="anonymous"></script>\n')

changed = 0
for p in all_pages():
    s = p.read_text(encoding="utf-8")
    if CLIENT in s or "</head>" not in s:
        continue
    p.write_text(s.replace("</head>", TAG + "</head>", 1), encoding="utf-8")
    changed += 1
print(f"adsense: tagged {changed} page(s)")
