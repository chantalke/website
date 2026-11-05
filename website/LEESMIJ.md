# Lokale portfoliosite — Chantal van Kempen

Deze website is nog niet gepubliceerd. Voorbeeld: http://127.0.0.1:8765/.

## Bewerken en bouwen

`data.js` bevat de Nederlandse projecten en loopbaangegevens. `case-notes.js` bevat de uitgebreidere projectverhalen. `public-project-copy.json` vervangt interne onderzoeksformuleringen door beoordeelde openbare projectteksten. `aanbod-content.json` bevat de samenwerkingspagina’s. `index.html` en `media.html` bevatten de Nederlandse basispagina’s.

Vertalingen staan in `build_locales.py`, `translations.json`, `i18n-en.js` en de tweetalige projectnotities. Bewerk gegenereerde Engelse pagina’s niet rechtstreeks.

Vanuit de bovenliggende projectmap:

```sh
python3 website/build_site.py
python3 prepare_publish.py
```

Het eerste commando bouwt talen, vraagstukpagina’s, projectverhalen en SEO-metadata en controleert de links. Het tweede maakt `output/website-liveklaar/`, de afzonderlijke uploadmap zonder bouwscripts en interne documentatie. Beide commando’s publiceren niets. Python 3 en Node zijn nodig om opnieuw te bouwen; de uiteindelijke website is statisch en heeft geen serverapplicatie nodig.

## Vormgeving en bestanden

`style.css`, `experience.css` en `seo-pages.css` verzorgen de bestaande magazineachtige vormgeving. `app.js` bevat de filters, projectvensters en easter egg. `experience.js` bevat de themadeuren. `media.js` verzorgt het chronologische mediaoverzicht.

De lettertypes staan lokaal met hun licenties in `assets/fonts/`. De gebruikte projectfoto’s zijn eigen aangeleverde beelden, bewerkt binnen de website met een gedeelde kleurlaag. De actuele hero-video is `assets/experience-loop-v2.mp4`. De eerdere video en magazinevarianten blijven alleen als bron/alternatief bewaard en gaan niet mee in de uploadmap.

Het portfolio en het impactonderzoek zijn downloads onder `assets/`. De Engelse site vermeldt expliciet dat het portfolio en rapport Nederlands zijn. Externe video’s en podcasts openen via een link; er zijn geen automatisch ingesloten externe spelers of analytics toegevoegd. De e-mailknop biedt het adres aan om te kopiëren. WhatsApp opent alleen op initiatief van de bezoeker.

## Livegang

`seo-config.json` bevat het beoogde domein https://chantalvankempen.nl. De uploadmap heeft een sitemap, robots.txt, een 404-pagina en `_redirects`. Op hosting anders dan Netlify/Cloudflare Pages moet de redirect van /index.html naar / apart worden ingesteld. HTTPS, de echte 404-status, compressie, cacheheaders en Search Console moeten bij publicatie worden gecontroleerd.

De volledige controle en resterende hostingspunten staan in `../livegangcheck-2026-11-05.md`. De site heeft op 5 november 2026 de lokale controle voor alle 40 openbare pagina’s doorstaan. Dit is geen garantie op indexering of verkeer.
