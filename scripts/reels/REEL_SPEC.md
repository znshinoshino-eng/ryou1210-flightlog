# Daily Instagram Reel spec (Flightlog Japan)

One silent 1080x1920 Reel + one English caption per day, made from ONE existing article on the site.
The owner posts it by hand and adds trending audio in Instagram.

## Pick the article
- Take the first article on the top page (index.html, in page order) whose slug is NOT in REELS_LOG.md.
  If every article has been used, start again from the oldest entry in the log, with a new angle.
- Prefer travel-prep and transit guides; skip pure plane-spotting guides unless nothing else is left.

## Write the spec (spec.json, see gen.py)
- hook: [kicker (≤ 25 chars), title (≤ 28 chars, a question works well), sub (≤ 26 chars)]
- tips: exactly 5 × [head (≤ 28 chars), body (≤ 110 chars), note (≤ 55 chars)]
- Every fact, price, time and rule must come from the article text. Do not add anything the article
  doesn't say (owner's rule: unverified facts are never published). Prices only with "(Oct 2026)" style dates
  if the article dates them.
- Plain, friendly English. No Klook or affiliate mentions in the video.

## Render and check
- python3 scripts/reels/gen.py spec.json /home/claude/flightlog_reel_<YYYYMMDD>_<slug>.mp4
- Read the .contact.png and check no text overflows or overlaps. Shorten text and re-render if it does.

## Caption (English, for Instagram)
Hook line with 1 emoji + 👇
1️⃣–5️⃣ one line each (same facts as the video)
One line from the railway-worker angle ("I work at a station and …"), only things that are generally true, no invented stories
✈️ Full guide on Flightlog Japan, free Japan travel guides written by someone who works on Japan's railways 👉 link in bio
💾 Save this for your Japan trip
10–12 hashtags (#japantravel #japantrip #visitjapan #japantips #traveljapan #firsttimeinjapan #japantravelguide + topic tags)

Also give a YouTube Shorts title (≤ 70 chars) and description line with the article link:
https://flightlogjapan.com/articles/<slug>.html?utm_source=youtube&utm_campaign=shorts

## Log
Append to REELS_LOG.md: "- YYYY-MM-DD | <slug> | <hook title>".
