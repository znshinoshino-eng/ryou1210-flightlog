# Next actions

1. P2 (owner's call, article text): on zh/ic-cards-suica-pasmo-icoca and zh/welcome-suica-guide the list "¥1,000、¥2,000、…¥10,000" can
   split inside a price at 360px ("¥5 / ,000"). Adding `<wbr>` after each 、 before ¥ in those articles would wrap between whole prices.
   Not done: article text is outside the AI team's scope.
2. P2 site.js table check: tabindex uses 0px tolerance, the hint 2px → a 1–2px overflow is focusable with no hint. Parked: making tabindex
   2px could trigger axe scrollable-region-focusable; no user-visible gain measured.
3. P2 Try a Lighthouse run (npm lighthouse + local Chromium) to get real performance/accessibility numbers before claiming any speed change.
4. P2 Desktop top page: the yellow sign's four jump buttons repeat the section bar right above. Consider hiding on desktop only if a measurement shows a clear gain.
5. P2 Floating "↑ Contents" button sits over the last line of text while scrolling on phones (seen 11-11, narita-or-haneda @390); it moves
   with scroll, so text is readable — check only if a page shows it covering something that never scrolls clear (e.g. footer links).
6. Done 11-11: no sideways scroll at 360px; qa_check.py tests 360px. Done 11-08: 3-column tables fit. Done 11-04: skip link. Done 11-01: empty table corner cells.
7. Note: the full qa_check.py run takes ~5–6 min (103 pages × 3 widths); use a long timeout (≥600 s).
