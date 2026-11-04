# Research log (Agent 1)

## 2026-10-25 (first run)
**Looked at**
- japan-guide.com, shinkansen page (https://www.japan-guide.com/e/e2018.html), checked 2026-10-25 via a summarising fetch tool.
  Good: breadcrumb, "on this page" contents near the top, question-style subheadings, related-page sub-navigation.
  Compared with us: we already have breadcrumb, contents box, short answer box (added 10-24) and related guides. Nothing new to copy this time.
- axe-core rule *scrollable-region-focusable* (https://dequeuniversity.com/rules/axe/4.10/scrollable-region-focusable), checked 2026-10-25.
  Scrollable areas must be reachable by keyboard (WCAG 2.1.1). Fix: `tabindex="0"` on the scrolling element.

**Applicable ideas** → keyboard-reachable wide tables (done); unique names for menus (done).
Later candidates: question-style subheadings are article content (out of our scope).

**Limits**: the fetch tool summarises pages with a small model, so its suggestions are hints, not facts.
No Lighthouse/real-device run this time.

## 2026-10-28
**Looked at (own site, local headless Chromium, photos blocked)**
- Top page and 2 guides (nikko-day-trip-from-tokyo, taxis-in-japan) at 390px and 1280px.
  - Desktop 1280×800: the top-page photo is 1000×400 (5:2); the first guide section heading starts at y≈945, so no guide,
    filter or section heading is on the first screen. Guide pages already use a shorter 2:1 photo (10-21).
  - Tap-target sweep of all 80 pages at 390px (links/buttons/summary, inline text links excluded): the "Why we link to Klook"
    toggle is 23px tall on 66 pages; photo-credit links are 16px tall but are inline caption text (exempt); breadcrumb 24px (OK).
  - Nikko 4-column table overflows (468 vs 356px) and the swipe hint shows — works as designed.
- W3C technique C42 (https://www.w3.org/WAI/WCAG22/Techniques/css/C42.html), checked 2026-10-28: SC 2.5.8 asks for 24×24 CSS px
  targets (or enough spacing); padding/min-height on the target is the usual fix. The W3C Understanding page for 2.5.8 could not
  be fetched this run (permission prompt timed out) — summary came from the technique page via a summarising fetch tool.
**Limits**: the 23px toggle likely already passes 2.5.8 through its spacing exception; the fix is for comfort on phones (~44px), not a compliance failure.

## 2026-11-01
**Looked at (own site, local headless Chromium, photos blocked)**
- Top page, tax-free-refund-japan-airport (new 10-31) and welcome-suica-guide at 390×844 and 1280×800. No new layout problem seen:
  header fits, short-answer box and filters as before.
- QA baseline: 89 pages (+9 since 10-28), 0 errors. axe empty-table-header went 4 → 5 pages: the new tax-free guide also has an
  empty top-left `<th>` (same pattern as nara, night-bus, welcome-suica en/zh). All 5 are the first cell of the first row.
- W3C WAI tables tutorial, "Tables with two headers" (https://www.w3.org/WAI/tutorials/tables/two-headers/), checked 2026-11-01
  via a summarising fetch tool: its example marks the empty corner cell as `<td></td>`, not `<th>`.
**Applicable idea** → turn an empty corner `<th>` into `<td>` with site.js (no article HTML change), keep the dark look with CSS.
**Limits**: fetch tool summary only; no screen-reader test on a real device.

## 2026-11-04
**Looked at (own site, local headless Chromium, photos blocked)**
- Top page, finding-your-platform-japan-stations (new 11-03) and onsen-towns-by-train-from-tokyo at 390×844 and 1280×800.
  No layout problem: header fits, short-answer box, contents, tables with swipe hint, "Keep reading", footer as before.
- QA baseline: 96 pages (+7 since 11-01), 0 errors, 0 axe rules.
- Wide-table sweep at 390px: 25 tables on 24 guides show the swipe hint; all really overflow (most 468 vs 356px).
  contactless-credit-card-trains (366/356) and hiroshima-miyajima (368/356) overflow only 10–12px — hint is correct but borderline (not acted on).
- Keyboard: no "skip to content" link on any page. Keyboard users press Tab 7–8 times (EN, logo + menu + 4 section links)
  before reaching anything inside `<main>` on every page (4–5 times on translated pages). Every page has exactly one `<main class="wrap">`.
- W3C technique G1 (skip link, WCAG 2.4.1 Bypass Blocks; https://www.w3.org/WAI/WCAG22/Techniques/general/G1): fetch was not
  approved in time (unattended run), so not re-read this run. The site already passes 2.4.1 through the `<main>` landmark; a visible-on-focus
  skip link is the common extra for sighted keyboard users (from general knowledge, not a fetched source).
**Applicable idea** → add a skip link with site.js (no HTML change to 96 pages).
**Limits**: no external source fetched this run; no real devices or screen reader.
