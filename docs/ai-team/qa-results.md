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

## 2026-11-01 — verdict: PASS (合格)
QA run by an independent sub-agent (PASS in round 1); screenshots also checked in the main session.
- qa_check.py, 89 pages × 390/1280: exit 0, 0 errors, 0 warnings, 0 overflow, 0 JS errors, 0 broken links. axe: empty-table-header 5 → 0; no rules left.
- `node --check site.js`: OK.
- All 5 corner cells are `TD.corner`; background rgb(27,29,32) = neighbouring header; 1px bottom rule = neighbour; header row height equal to
  neighbours at 390 and 1280; on phones the corner stays pinned (sticky, left 0) while the welcome-suica tables scroll 112px.
  Before/after measurements identical apart from tag/class. Screenshots: dark header row, no white gap.
- Tables without an empty corner (taxis-in-japan, japan-rail-passes-worth-it, others) unchanged.
Limits: no real devices or screen reader; photos/fonts blocked; no Lighthouse.

## 2026-11-04 — verdict: PASS (合格)
QA run by an independent sub-agent (PASS, one P2 note), fix and re-test in the main session.
- qa_check.py, 96 pages × 390/1280: exit 0, 0 errors, 0 warnings, 0 overflow, 0 JS errors, 0 broken links, axe 0 rules (before and after; re-run after the fix too).
- `node --check site.js`: OK.
- Skip link (10 pages incl. en/fr/de/es/th/zh index, article, about, contact, privacy × 390/1280): exactly one skip link and one `#main` per page;
  hidden above the viewport before any key press (bottom −41/−43px); header box, main top, page width/height identical to HEAD;
  first Tab shows it fully at (8,8), ~157×49px (widest de 208px), yellow/dark text; Enter → focus on MAIN (no outline), next Tab lands inside main
  (breadcrumb / "All" filter / back link), never in the header. From mid-page the jump ends with main just below the sticky header.
  Contents box, swipe hints and "Keep reading" still present; no JS page errors.
- Only page without `<main>`: google verification stub (script not loaded there; code returns early anyway).
- Round-1 issue (P2): 3px focus ring was `--sign` (near-black) → invisible on the dark header → now white; screenshot re-checked.
Limits: no real devices, no screen reader, photos/fonts blocked; no Lighthouse.
