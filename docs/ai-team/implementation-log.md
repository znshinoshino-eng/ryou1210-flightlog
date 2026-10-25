# Implementation log (Agent 3)

## 2026-10-25
- style.css: phones ≤480px hide `nav.site-nav > a:first-child`; `article.post table:focus-visible` outline.
- site.js: table check sets/removes `tabindex="0"` when a table scrolls sideways; ResizeObserver re-check
  (fonts can change width after load); translated aria-labels for `nav.site-nav` and `nav.hero-links`.
- docs/ai-team/ created (this folder) + tools/qa_check.py.
- Commands: `node --check site.js` (OK); `python3 docs/ai-team/tools/qa_check.py --axe …` (see qa-results.md).
- Fix rounds: 2 (QA found 2 pages where a table overflowed by ≤2px but got no tabindex → made the tabindex check strict).
