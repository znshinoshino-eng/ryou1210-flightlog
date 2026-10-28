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
