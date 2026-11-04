# Monitoring (Agent 4)

Re-run tools/qa_check.py every run and compare with the last row. Any new error = regression → fix before other work.

| Date | Pages | Overflow | JS errors | Broken links | axe rules (pages) |
|---|---|---|---|---|---|
| 2026-10-25 before | 71 | 8 | 0 | 0 | landmark-unique 71, scrollable-region-focusable 33, color-contrast 4, empty-table-header 4 |
| 2026-10-25 after | 71 | 0 | 0 | 0 | empty-table-header 4 |
| 2026-10-28 before | 80 | 0 | 0 | 0 | empty-table-header 4 |
| 2026-10-28 after | 80 | 0 | 0 | 0 | empty-table-header 4 |
| 2026-11-01 before | 89 | 0 | 0 | 0 | empty-table-header 5 |
| 2026-11-01 after | 89 | 0 | 0 | 0 | none |
| 2026-11-04 before | 96 | 0 | 0 | 0 | none |
| 2026-11-04 after | 96 | 0 | 0 | 0 | none |

Watch items: axe should stay at 0 rules — any new rule is a regression; new translated pages (long menu words) for header overflow; new articles with wide tables;
the "↑ Contents" button not covering content; the deploy run after each push (gh run list); the skip link stays hidden until Tab and is the first Tab stop.
Not monitored continuously — checks only run on the Wed/Sat schedule.
