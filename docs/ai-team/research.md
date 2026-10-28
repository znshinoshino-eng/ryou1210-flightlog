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
