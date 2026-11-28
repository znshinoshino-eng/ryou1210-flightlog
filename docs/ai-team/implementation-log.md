# Implementation log (Agent 3)

## 2026-10-25
- style.css: phones ≤480px hide `nav.site-nav > a:first-child`; `article.post table:focus-visible` outline.
- site.js: table check sets/removes `tabindex="0"` when a table scrolls sideways; ResizeObserver re-check
  (fonts can change width after load); translated aria-labels for `nav.site-nav` and `nav.hero-links`.
- docs/ai-team/ created (this folder) + tools/qa_check.py.
- Commands: `node --check site.js` (OK); `python3 docs/ai-team/tools/qa_check.py --axe …` (see qa-results.md).
- Fix rounds: 2 (QA found 2 pages where a table overflowed by ≤2px but got no tabindex → made the tabindex check strict).

## 2026-10-28
- style.css (appended block "2026-10-28"): `@media (min-width:721px) .hero-pic img { aspect-ratio: 3/1 }`;
  `.why-klook { padding-top:0 }`, `.why-klook summary { padding: 11px 0 }`, `.why-klook summary:focus-visible` 3px outline.
- No site.js / HTML change (node --check not needed). `?v=` asset hashes are updated by the sitemap workflow (scripts/asset_versions.py).
- Commands: qa_check.py before/after; playwright measurements (hero height, first h2 top, summary size); screenshots read.
- Fix rounds: 1 (QA sub-agent: summary was 43.25px with 10px padding → 11px = 45.25px; added custom focus outline).

## 2026-11-01
- site.js (wide-table block): before adding swipe hints, an empty `<th>` that is the first cell of a table's first row is replaced
  by `<td class="corner">` (attributes copied). Affects 5 pages (nara, night-bus, tax-free-refund, welcome-suica en/zh).
- style.css (appended block "2026-11-01"): `article.post table td.corner { background: var(--sign); border-bottom: 1px solid var(--rule); }`.
- Commands: `node --check site.js` (OK); qa_check.py before/after; Playwright measurements and screenshots by the QA sub-agent.
- Fix rounds: 0.

## 2026-11-04
- site.js (after the menu-name block): skip-link block — translated text (en/fr/de/es/th/zh), `main.id="main"` and `tabindex="-1"` if missing,
  `<a class="skip-link" href="#main">` inserted first in `<body>`; returns early when there is no `<main>` or a skip link already exists.
- style.css (appended block "2026-11-04"): `.skip-link` fixed top-left, `transform: translateY(-200%)` until `:focus`; yellow box, dark bold text,
  white 3px focus ring; `main[tabindex="-1"]:focus { outline: none }`; `main#main { scroll-margin-top: 128px }`.
- Commands: `node --check site.js` (OK); qa_check.py before/after; Playwright Tab/Enter test on 5 pages × 2 widths; screenshots read.
- Fix rounds: 1 (QA P2: the focus ring was near-black and invisible on the dark header → changed to white; re-tested).

## 2026-11-08
- style.css (appended block "2026-11-08"): `@media (max-width:720px)` — `article.post table:has(tr > :nth-child(3)):not(:has(tr > :nth-child(4)))` th/td `min-width: 96px`.
  No site.js / HTML change (node --check not needed).
- Commands: qa_check.py before/after; Playwright measurement of all 3-column tables at 360/390 with the CSS injected (before committing); screenshots read.
- Fix rounds: 0.

## 2026-11-08 (2) — owner asked "直して" (fix the Sources link text); scripts/ change approved by the owner for this task
- scripts/sources_box.py: link text is the page's readable name only when the address reads like words; code-like addresses
  ("20", "001291790.pdf", "page01_000001_00027") now show "page 1", "page 2" … (translated: Seite, página, หน้าเว็บ, 網頁); PDFs get "(PDF)".
  Sub-sites are grouped under their operator (faq.westjr.co.jp → JR West); 15 more operator names (police, Japan Post, Keio, Tokyu …).
  PER_ORG 4 → 5 so grouping never drops a link (net: no link removed, ~20 official links from the existing comments now shown).
- Regenerated: 57 article pages (only lines inside the sources box changed; checked with git diff). Re-run is idempotent (0 pages updated).
- QA: qa_check.py 99 pages × 390/1280: exit 0, 0 errors, axe 0 rules; sources box screenshot at 390 read.

## 2026-11-11
- style.css (appended block "2026-11-11"): `@media (max-width:380px)` — `article.post p, article.post li { overflow-wrap: break-word }`;
  `header.site-header .wrap { gap: 8px }`. No site.js / HTML change (node --check not needed).
- docs/ai-team/tools/qa_check.py: also loads every page at 360px (overflow + JS errors; no axe/screenshots there); overflow threshold `sw > width`.
- Commands: qa_check.py before/after; Playwright sweep of 103 pages at 360 (6 → 0 overflowing); before/after size comparison of every
  table, article p/li and header at 360/390/1280 (only the 2 zh pages change, at 360 only); screenshots read.
- Fix rounds: 1 (QA round 1: first version applied break-word to all of article.post at every width → changed wrapping at 390 and a
  table cell; narrowed to p/li at ≤380px).

## 2026-11-25
- site.js (wide-table block): new `edge(t)` toggles class `more-right` when `scrollLeft + clientWidth < scrollWidth - 2`; called from
  `check()` (load/resize/ResizeObserver) and on each table's `scroll` (passive listener).
- style.css (appended block "2026-11-25"): `article.post table.more-right { mask-image: linear-gradient(to right, #000 calc(100% - 44px), rgba(0,0,0,.12)) }`
  (+ -webkit- prefix); `:focus-visible` removes the mask so the focus outline stays visible.
- Commands: `node --check site.js` → ok. Screenshots shinkansen-how-to-ride table @390 at scroll 0 (fade) and scrolled to end (no fade).
  `?v=` hashes are updated by the sitemap workflow (scripts/asset_versions.py), not by hand.
- After QA: added `@media print` rule removing the mask (QA P2 note: printed tables could keep the fade). Print-only, no screen change.

## 2026-11-28
- style.css (appended block "2026-11-28"): `@media (max-width:380px) { article.post h1,h2,h3 { overflow-wrap: break-word } }`;
  `@media (max-width:359px) { nav.site-nav > a { white-space: normal; word-break: keep-all; text-align: center } }`. No site.js / HTML change.
- docs/ai-team/tools/qa_check.py: widths (320, 360, 390, 1280); 320 = overflow + JS errors only (no axe/screenshots).
- Commands: Playwright 320px sweep of 140 pages with CSS injected (9 → 0 overflowing; only those 9 pages changed size); qa_check.py (sub-agent).
- Fix rounds: 1. QA round 1 (first version ≤340px, `nav.site-nav a`, line-height 1.15) found: zh 關於我們 broke mid-word; rule also centred
  the language-menu links; one-line links lost height (38→30px). I also measured es still overflowing at 341–359px.
  → child selector, keep-all, no line-height, breakpoint 359px. Round 2 passed.
