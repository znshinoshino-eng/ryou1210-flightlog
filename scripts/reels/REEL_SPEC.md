# Daily Instagram Reel spec (Flightlog Japan)

One silent 1080x1920 Reel + one English caption per day, made from ONE existing article on the site.
The owner posts it by hand and adds trending audio in Instagram.

## Pick the article
- Take the first article on the top page (index.html, in page order) whose slug is NOT in REELS_LOG.md.
  If every article has been used, start again from the oldest entry in the log, with a new angle.
- Prefer travel-prep and transit guides; skip pure plane-spotting guides unless nothing else is left.

## Write the spec (spec.json, see gen.py — format v2, since 2026-10-30)
Why v2: the old 26 s text-slide reels had a very high skip rate. v2 is ~15-18 s, the hook is readable
on frame 0, there is a cut every 2.4-3.2 s, one idea per card, constant motion, and the end loops to the hook.
- kicker: "I work on Japan's railways" (default; ≤ 30 chars). It is the channel's strongest angle.
- hook: ≤ 34 chars (not counting the asterisks), ≤ 7 words. Put ONE key word in *asterisks* (yellow sign
  highlight). Punctuation may follow the closing asterisk ("*Suica*," works).
  Use a proven pattern, filled ONLY with facts from the article:
  - "Do kids ride *FREE* on Japan's trains?" (yes/no question with a surprising answer)
  - "Don't *buy* this until you see this" / "Stop doing *this* at Japanese stations"
  - "4 things I wish I knew about *Suica*"
  - "Tourists always *miss* this at Tokyo Station"
  - "The *¥___* mistake tourists make" (only with a price the article states)
  No clickbait the cards don't pay off; the first card must answer the hook.
- cards: exactly 4 × [head (≤ 34 chars without asterisks, ≤ 7 words, one *highlight* word), sub (≤ 48 chars, ≤ 10 words)].
  One idea per card. Long explanations go in the caption, not the video.
- end (optional): [big line, small yellow line]; defaults to ["Save this for your Japan trip", "Full guide: link in bio"].
- photo (optional): path to a real photo in scripts/reels/photos/ (the owner's own station/train photos).
  Use one when a fitting photo exists (the folder may still be empty: then leave "photo" out).
  Avoid the photos used in the last 3 log lines. The cloud run cannot download photos (Unsplash etc.
  are blocked), so only use photos in that folder.
- Every fact, price, time and rule must come from the article text. Do not add anything the article
  doesn't say (owner's rule: unverified facts are never published). Prices only with "(Oct 2026)" style dates
  if the article dates them: if a price appears, add the article's date in the sub, e.g. "(Oct 2026)".
- Plain, friendly English. No Klook or affiliate mentions in the video.

## Render and check
- python3 scripts/reels/gen.py spec.json /home/claude/flightlog_reel_<YYYYMMDD>_<slug>.mp4
- If it prints any "WARN", fix it (shorten the text / fix the photo path) and re-render.
- Read the .contact.png (one frame per card) and check nothing overflows, overlaps or is cut off.
- gen_classic.py is the old style; don't use it unless gen.py fails.

## Caption (English, for Instagram)
First line = the video's hook (same words, no asterisks) + 1 emoji + 👇
1️⃣–4️⃣ one line each, same facts as the cards but with the detail the video left out
(this is where the longer explanation goes)
One line from the railway-worker angle ("I work at a station and …"), only things that are generally true, no invented stories
✈️ Full guide on Flightlog Japan, free Japan travel guides written by someone who works on Japan's railways 👉 link in bio
💾 Save this for your Japan trip
10–12 hashtags (#japantravel #japantrip #visitjapan #japantips #traveljapan #firsttimeinjapan #japantravelguide + topic tags)

Also give a YouTube Shorts title (≤ 70 chars) and description line with the article link:
https://flightlogjapan.com/articles/<slug>.html?utm_source=youtube&utm_campaign=shorts

## Log
Append to scripts/reels/REELS_LOG.md: "- YYYY-MM-DD | <slug> | <hook, without asterisks> | <photo file name or ->".
