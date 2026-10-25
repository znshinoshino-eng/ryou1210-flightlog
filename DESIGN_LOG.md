# Design log

Small, safe design improvements to Flightlog Japan (style.css / site.js / shared HTML only).

## Earlier (from git history)
- 2026-10-09: airport-wayfinding redesign; photos; reading aids (breadcrumbs, reading time, contents box, related guides, topic/area filters); language switcher; Klook explanation; top-page photo hero and reader sections.
- 2026-10-10: guide-section bar under the header.

## 2026-10-10
- Phones: top-page filter chips no longer make the whole page scroll sideways (chips now scroll inside their own row).
- Phones: wide tables show a "swipe sideways" hint (only when they overflow), and the first column stays fixed while swiping.

## 2026-10-14
- Phones: top-page guide cards (except the featured one) show a small square photo beside the title, so the page is about a third shorter and more guides fit on screen.
- Booking buttons placed mid-sentence are slimmer and centred on the line, so the surrounding text keeps even line spacing.

## 2026-10-18
- Tapping a heading in "In this guide" (or a top-page section button) now lands with the heading fully visible, instead of half hidden under the sticky header.
- Long guides show a floating "↑ Contents" button once you scroll past the contents box, to jump back to the section list.
- Phones: table text and cell padding slightly smaller, so fare tables have shorter rows.
- (re-run for 10/17) Phones: two-column tables use the full width (left column no longer pinned and squeezed), so their rows are much shorter.

## 2026-10-21
- The floating "↑ Contents" button now hides at the end of a guide, so it no longer covers the "Keep reading" links or the footer.
- Desktop: the top photo of each guide is a little shorter (2:1), so the short answer starts sooner.
- Phones: footer links have finger-sized tap areas.

## 2026-10-24
- The short answer at the top of each guide now sits in a pale-yellow box, so the key facts (prices, time limits) stand out.
- Phones: the yellow top sign no longer repeats the four section buttons already in the bar above, so the guides start higher on the first screen.

## 2026-10-25
- Phones: Spanish and Thai pages no longer scroll sideways; the language button is fully visible (the "Articles" link hides on small screens — the logo goes to the same page).
- Wide tables can be scrolled with the keyboard; menus have distinct names for screen readers.
- From now on the full records are in docs/ai-team/ (research, proposals, QA, monitoring, next actions).
