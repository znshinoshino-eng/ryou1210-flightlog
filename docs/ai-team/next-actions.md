# Next actions

1. P2 Try a Lighthouse run (npm lighthouse + local Chromium) to get real performance/accessibility numbers before claiming any speed change.
2. P2 Desktop top page: the yellow sign's four jump buttons repeat the section bar right above (already hidden on phones since 10-24). Consider hiding on desktop too only if a measurement shows a clear gain.
3. P2 (watch) Tables that overflow by only ~10px on phones (contactless-credit-card-trains, hiroshima-miyajima) show the swipe hint; correct, but a slightly smaller phone font could make them fit. Only act if more appear.
4. Done 11-04: "Skip to content" link (site.js). Done 11-01: empty table corner cells. Done 10-28: tap targets; landmark names.
5. Ideas from research: re-read W3C G1 (skip links) when a fetch is possible, to confirm wording/behaviour.
6. P2 The full qa_check.py run takes ~3 min (96 pages); use a longer timeout (≥400 s).
