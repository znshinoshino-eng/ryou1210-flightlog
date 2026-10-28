# Proposals (Agent 2)

## 2026-10-25
Baseline QA (before changes): 8 errors. Spanish and Thai pages are wider than a 390px phone (es 442px, th 393px);
the language button is pushed off the dark header (axe color-contrast fails on it).
axe: scrollable-region-focusable on 33 pages; landmark-unique on 71 pages; empty-table-header on 4 pages.

| # | Pri | Problem (fact) | Plan | Files | Acceptance | Risk / rollback |
|---|---|---|---|---|---|---|
| 1 | P1 | es/th header overflows on phones; language button cut off | ≤480px: hide the first menu link ("Articles"); the logo links to the same page and the guide bar covers sections | style.css | 0 overflow at 390/1280 on all 71 pages; language button visible and menu opens | Articles link gone on small phones (logo still goes there). Revert commit |
| 2 | P2 | wide tables can't be scrolled by keyboard | site.js gives overflowing tables `tabindex=0` (+ re-check on resize/font load); visible focus outline | site.js, style.css | axe scrollable-region-focusable = 0; Tab reaches table; arrows scroll it | extra Tab stop per wide table only. Revert commit |
| 3 | P2 | two menus share the name "Guide sections"; main menu unnamed | site.js sets translated aria-label on nav.site-nav and nav.hero-links | site.js | axe landmark-unique = 0 | none visible. Revert commit |

On hold: empty-table-header (4 articles) — needs article HTML change, out of scope.

## 2026-10-28
Baseline QA: 80 pages, 0 errors, axe only empty-table-header ×4 (same as 10-25; no regressions).

| # | Pri | Problem (fact) | Plan | Files | Acceptance | Risk / rollback |
|---|---|---|---|---|---|---|
| 1 | P2 | Desktop top page: 400px-tall photo pushes all guides below the first screen (first section h2 at y≈945 @1280×800) | ≥721px: `.hero-pic img` aspect-ratio 3/1 (photo 333px) | style.css | h2 ≥60px higher; filter chips visible on first screen @1280×800; phones unchanged (16:9); caption/plane icon not overlapping; QA 0 errors | photo cropped a little more (object-fit: cover). Revert commit |
| 2 | P2 | "Why we link to Klook" toggle only 23px tall (66 pages) | summary padding 11px 0 (container padding-top 0) + 3px focus outline like tables | style.css | summary ≥44px; opens by click and Enter; focus ring visible; QA 0 errors | affiliate box ~14px taller. Revert commit |
