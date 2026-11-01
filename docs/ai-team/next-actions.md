# Next actions

1. P2 Try a Lighthouse run (npm lighthouse + local Chromium) to get real performance/accessibility numbers before claiming any speed change.
2. P2 Desktop top page: the yellow sign's four jump buttons repeat the section bar right above (already hidden on phones since 10-24). Consider hiding on desktop too only if a measurement shows a clear gain.
3. Done 11-01: empty top-left `<th>` in tables is turned into a `<td class="corner">` by site.js (axe empty-table-header 0). New articles with the same pattern are covered automatically.
4. Done/closed: tap targets at 390px swept on 10-28 (only the Klook toggle was small → fixed); unnamed nav — axe landmark-unique is 0, nothing to do.
5. Ideas from research: none pending.
6. P2 The full qa_check.py run now takes ~2.5 min (89 pages); use a longer timeout (≥300 s).
