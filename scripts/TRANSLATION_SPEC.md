# Translation spec for Flightlog Japan

Languages: fr (French), de (German), es (Spanish, neutral, readable in Spain and Latin America).

## What to translate
Source (English) files, all in the repo root:
- index.html → `<lang>/index.html`
- articles/japan-rail-passes-worth-it.html → `<lang>/articles/japan-rail-passes-worth-it.html`
- articles/narita-tokyo-tickets-passes.html → `<lang>/articles/narita-tokyo-tickets-passes.html`
- articles/haneda-tokyo-tickets-passes.html → `<lang>/articles/haneda-tokyo-tickets-passes.html`

Keep the same file names (slugs stay English).

## Rules
1. Write natural, native-sounding text for a traveler, not a literal translation. Keep the friendly, practical tone and the "written by someone who works on Japan's railways" voice. Keep every fact, number, price and date exactly as in the English source. Do not add new facts.
2. `<html lang="fr">` / `"de"` / `"es"`.
3. Translate: `<title>` (keep " - Flightlog Japan" at the end), meta description (max ~155 chars), h1/h2, body text, table cells, image `alt`, figcaption words ("Photo" stays fine; "on Unsplash" → "sur Unsplash" / "auf Unsplash" / "en Unsplash"), the `.meta` line, the `.cat` label, excerpts on index cards.
4. Category labels: Access & Transit → fr "Accès et transports", de "Anreise & Verkehr", es "Acceso y transporte".
5. Affiliate links: keep every `href` to affiliate.klook.com exactly as is, keep `rel="sponsored noopener" target="_blank"`. Translate "(affiliate link)" → fr "(lien affilié)", de "(Affiliate-Link)", es "(enlace de afiliado)".
6. Paths (the files sit one or two levels deeper than the English ones):
   - In `<lang>/index.html`: stylesheet `../style.css`, script `../site.js`, brand + "Articles" nav → `index.html`, "About" nav → `../about.html`, footer Privacy → `../privacy.html`, About → `../about.html`, cards → `articles/<slug>.html`.
   - In `<lang>/articles/*.html`: stylesheet `../../style.css`, script `../../site.js`, brand + nav "Articles" + back link → `../index.html`, About → `../../about.html`, Privacy → `../../privacy.html`.
   - Links between the three translated articles: just `<slug>.html`. Links to any other English-only article: `../../articles/<slug>.html`.
7. Nav/footer words: "Articles" → fr "Articles", de "Artikel", es "Artículos"; "About" → fr "À propos", de "Über uns", es "Sobre nosotros"; "Privacy & Disclosure" → fr "Confidentialité", de "Datenschutz", es "Privacidad"; "← Back to articles" → fr "← Retour aux articles", de "← Zurück zu den Artikeln", es "← Volver a los artículos".
8. Do NOT add canonical, Open Graph, hreflang or JSON-LD tags. A build script adds them. Keep everything else in `<head>` as in the source.
9. `<lang>/index.html`: keep the same layout/classes as the English index, translate the hero, and include ONLY the three translated article cards (keep their `data-region`, thumbnails and classes). Write the hero for the broader site ("Practical guides for visiting Japan: rail passes, airport transfers, IC cards…") rather than only Haneda.
10. Keep all classes, ids, structure, image URLs and the photo credit links unchanged. The `.cat` inline style stays.
11. Measurements and money: keep ¥ and US$ amounts as written. Use the language's normal number formatting only if it doesn't change a value (e.g. "¥50,000" may become "50 000 ¥" in French — prefer keeping "¥50,000" for clarity).

## Thai (th)
- `<html lang="th">`. Natural, friendly Thai for travelers (use ครับ/ค่ะ sparingly or not at all; neutral polite style like Thai travel blogs).
- Keep proper nouns that Thai travelers search in English as well, e.g. "Narita Express (N'EX)", "Skyliner", "JR Pass", "Suica". Thai transliteration can be added in parentheses on first mention when common (e.g. นาริตะ, ฮาเนดะ).
- Category: Access & Transit → "การเดินทางและขนส่ง".
- "(affiliate link)" → "(ลิงก์พันธมิตร)".
- Nav: "Articles" → "บทความ", "About" → "เกี่ยวกับเรา", "Privacy & Disclosure" → "ความเป็นส่วนตัว", "← Back to articles" → "← กลับไปที่บทความ".
- "on Unsplash" → "บน Unsplash".

## Traditional Chinese (zh) — Taiwan and Hong Kong
- Folder `zh/`, `<html lang="zh-Hant">`. The build scripts output hreflang `zh-Hant` and og:locale `zh_TW`.
- OWNER'S REQUEST: write the way people in Taiwan actually talk and search, like a popular Taiwanese Japan-travel blog (痞客邦 / Dcard style), not a translation. Friendly 你, short sentences, full-width punctuation. Light colloquial touches are welcome (超方便, 回本, CP 值, 記得, 不亂猜) but never at the cost of a fact.
- Titles: use the words Taiwanese readers search for: 攻略, 怎麼選, 怎麼買最划算, 值得買嗎, 自由行, 東京市區.
- Glossary (always use the right-hand word):
  | English | zh |
  | --- | --- |
  | Suica | Suica 西瓜卡 (first mention: 也就是大家說的「西瓜卡」), later "Suica" or "西瓜卡" |
  | convenience store | 超商 (not 便利商店) |
  | coin locker | 寄物櫃 / 投幣式寄物櫃 (not 置物櫃) |
  | fare adjustment machine | 精算機（補票機） |
  | SIM / mobile data | 網卡、eSIM、網路 |
  | pocket WiFi | Wi-Fi 分享器 |
  | reserved / non-reserved seat | 指定席 / 自由席; to reserve a seat = 劃位 |
  | top up | 儲值 |
  | ticket gate | 剪票口 |
  | eki-ben | 鐵路便當（駅弁） |
  | Tokyo Subway Ticket | 東京地鐵通票（Tokyo Subway Ticket） |
  | limousine bus | 利木津巴士 |
  | first-time visitor | 第一次去日本自由行的人 |
  | Nozomi / Hikari / Kodama | 希望號（Nozomi）/ 光號（Hikari）/ 回聲號（Kodama） |
- Keep names travelers search in English alongside Chinese on first mention, e.g. 希望號（Nozomi）, 東京地鐵通票（Tokyo Subway Ticket）, Skyliner, JR Pass, Suica, PASMO, smartEX.
- Categories: Access & Transit → "交通與移動", Travel Prep → "行前準備", Sightseeing → "觀光", Spotting Guide → "賞機指南".
- "(affiliate link)" → "（聯盟連結）". Link text "X on Klook" → "在 Klook 預訂 X".
- Nav: "Articles" → "文章", "About" → "關於我們", "Privacy & Disclosure" → "隱私權與揭露", "Contact" → "聯絡我們", "← Back to articles" → "← 返回文章列表".
- "Short answer:" → "先說結論：". The `.meta` line: "由在日本鐵路公司工作的人撰寫". Keep "Photo: … on Unsplash" as is.
- zh/index.html lists every translated article; the first card has class "post-card featured".
- Translated so far (2026-10-23): japan-rail-passes-worth-it, narita-tokyo-tickets-passes, haneda-tokyo-tickets-passes, shinkansen-how-to-ride, ic-cards-suica-pasmo-icoca, jr-pass-calculator, welcome-suica-guide, contactless-credit-card-trains-japan, luggage-forwarding-japan, esim-wifi-powerbank-guide, lost-something-on-train-japan.
