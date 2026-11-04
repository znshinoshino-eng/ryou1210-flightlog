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
