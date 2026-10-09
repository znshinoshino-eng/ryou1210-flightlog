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
