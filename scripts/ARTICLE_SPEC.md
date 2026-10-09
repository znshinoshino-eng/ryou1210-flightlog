# New article spec for Flightlog Japan (English)

Site: https://znshinoshino-eng.github.io/ryou1210-flightlog/ — practical guides for first-time visitors to Japan, written by someone who works for a Japanese railway company. Repo: /home/claude/ryou1210-flightlog

## Template
Copy the structure of `articles/japan-rail-passes-worth-it.html` exactly: same header, `<main class="wrap"><article class="post">`, the `.cat` div with the same inline style, `<h1>`, `.meta` line, `<figure class="hero-img">` with an Unsplash photo + credit, body, `<a class="back-link" href="../index.html">← Back to articles</a>`, same footer, `<script src="../site.js" defer></script>`.
- In `<head>` keep only: charset, viewport, `<title>… - Flightlog Japan</title>` (title before the suffix ≤ 60 chars), `<meta name="description">` (≤ 155 chars), the four icon `<link>` lines exactly as in the template, stylesheet. Do NOT add canonical / og / twitter / hreflang / JSON-LD (a build script adds them).
- `.meta` line: e.g. "Transit guide · Written by someone who works on Japan's railways · Checked October 2026".
- Use at least 4 `<h2>` sections. Start with a `<p><strong>Short answer:</strong> …</p>`. Include one comparison or summary `<table>` if it helps. Short paragraphs, plain English, friendly and practical. ~1,000–1,400 words.
- Internal links where natural (relative): `japan-rail-passes-worth-it.html`, `narita-tokyo-tickets-passes.html`, `haneda-tokyo-tickets-passes.html`, `getting-to-haneda-spotting-decks.html` (IC cards & trains to Haneda), `tokyo-sightseeing-bookings.html`, `private-car-transfer-chauffeur-tokyo.html`, `esim-wifi-powerbank-guide.html`, plus the other new articles: `luggage-forwarding-japan.html`, `shinkansen-how-to-ride.html`, `ic-cards-suica-pasmo-icoca.html`, `kyoto-osaka-getting-around.html`.
- Affiliate links: only products listed in scripts/klook_products.md, and only when they genuinely fit the topic (href exactly as given, rel="sponsored noopener" target="_blank", " (affiliate link)" after the link text). Never construct new affiliate links.

## Accuracy (most important)
- Every price, fee, size limit, time and rule must be checked against an official or primary source with WebSearch/WebFetch (operator websites like JR Central/JR East/JR West, Yamato Transport, Kyoto City Bus, Osaka Metro, JNTO). If you cannot verify a fact or number from an official or primary source, leave it out entirely (owner rule: unverified things are not published). Never guess.
- Say "at the time of writing (October 2026)" for prices that can change.
- At the very end of the file, after `</html>`, add nothing. Instead put an HTML comment just before `</article>`: `<!-- sources: url1 | url2 | ... -->` listing the pages you used.

## Photo
Find a free (not Unsplash+) photo on Unsplash with WebFetch (e.g. https://unsplash.com/s/photos/<topic>). Then WebFetch the photo page to confirm the photographer name and the exact `images.unsplash.com/photo-…` id. Use `?w=1200&amp;h=675&amp;fit=crop&amp;auto=format&amp;q=75`, and credit like the template (photographer link + Unsplash link with `utm_source=flightlog_japan&amp;utm_medium=referral`). Good `alt` text.

## Reply
Reply with: file path, title, a 1-sentence excerpt for the index card (≤ 170 chars), the Unsplash thumb URL (`?w=720&amp;h=405&amp;fit=crop&amp;auto=format&amp;q=70`), category label, and a list of the key numbers/rules with the source URL for each.
