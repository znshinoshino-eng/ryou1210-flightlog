# QA results (Agent 4)

## 2026-10-25 — verdict: PASS (合格)
Checks run (71 pages × 390px and 1280px, headless Chromium, external requests blocked):
- Horizontal overflow: before 8 pages (es ×4, th ×4) → after 0.
- JS errors: 0. Broken internal links: 0. Images without alt: 0. `node --check site.js`: OK.
- axe-core 4.10.2: color-contrast 4 → 0; scrollable-region-focusable 33 → 2 (round 1) → 0 (round 2); landmark-unique 71 → 0;
  empty-table-header 4 (known, out of scope).
- Manual: es/th/en phone headers show logo, About and language button; Spanish language menu opens inside the screen;
  desktop header unchanged (Articles link visible); Tab reaches the locker-fee table after 13 Tabs, blue outline shows,
  arrow keys scroll it (scrollLeft 80).
Round 1 issue: tables overflowing by 1–2px got the swipe-hint tolerance and no tabindex (P2) → fixed in round 2.
Limits: the QA sub-agent could not run (usage limit), so QA was run in the same session. No Lighthouse/performance measurement; no real devices.

## 2026-10-28 — verdict: PASS (合格)
QA run by an independent sub-agent (round 1: CONDITIONAL PASS), re-test after fix in the main session.
- qa_check.py, 80 pages × 390/1280: 0 errors, 0 warnings, 0 overflow, 0 JS errors, 0 broken links; axe: empty-table-header ×4 only (unchanged).
- Hero @1280: photo 1000×333 (ratio 3.000); first section h2 945 → 878px, first card 1028 → 962px; filter chips now on the first screen.
  @390: unchanged (16:9, h2 at 746). Caption and plane icon do not overlap. Translated top pages have no photo hero (unaffected).
- Klook toggle: 23.25 → 45.25px tall at 390 and 1280; click opens; Tab (12 presses) + Enter opens/closes; 3px blue focus ring seen in screenshot.
- Round-1 issues (P2): height 43.25px < 44 target; default thin focus ring → both fixed, re-tested.
Limits: no real devices, no Lighthouse; photos blocked so crop of the real image not seen (object-position 50% 55% kept).
