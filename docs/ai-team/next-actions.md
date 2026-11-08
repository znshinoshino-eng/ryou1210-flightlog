# Next actions

1. P2 Page-level sideways scroll at 360px (small Android) on zh/ic-cards-suica-pasmo-icoca (24px) and zh/welcome-suica-guide (20px), 1px on 3 es pages
   (found 11-08; qa_check only tests 390px). Find the wide element and fix next run; consider adding 360px to qa_check.py.
2. P2 site.js table check: tabindex uses 0px tolerance, the hint 2px → a 1px overflow is focusable with no hint. Align both to 2px (small site.js change).
3. Owner's call (out of AI-team scope: scripts/): Sources boxes use URL fragments as link text ("20", "001291790.pdf"). A clearer label
   (page title or "PDF") from the generator would help readers and screen readers.
4. P2 Try a Lighthouse run (npm lighthouse + local Chromium) to get real performance/accessibility numbers before claiming any speed change.
5. P2 Desktop top page: the yellow sign's four jump buttons repeat the section bar right above. Consider hiding on desktop only if a measurement shows a clear gain.
6. Done 11-08: 3-column tables fit on phones. Done 11-04: skip link. Done 11-01: empty table corner cells. Done 10-28: tap targets; landmark names.
7. Note: the full qa_check.py run takes ~3–4 min (97 pages); use a long timeout (≥600 s).
