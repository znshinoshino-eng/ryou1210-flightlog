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
