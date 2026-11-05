# Chantal van Kempen — portfolio

Openbare bronrepository voor de tweetalige portfoliosite van Chantal van Kempen. De website is statisch: HTML, CSS, JavaScript, foto's, een achtergrondvideo en PDF-downloads.

## Lokaal bekijken

Vereist om opnieuw te bouwen: Python 3.12 en Node.js 22. Er zijn geen externe Python- of npm-pakketten nodig.

```sh
python3 website/build_site.py
python3 prepare_publish.py
python3 -m http.server 8765 --directory output/website-liveklaar
```

Open daarna http://localhost:8765/. Zonder opnieuw te bouwen kan ook de map `website` worden geserveerd.

## GitHub Pages

De workflow `.github/workflows/pages.yml` bouwt en controleert beide talen bij elke push naar `main`. Alleen de schone statische bestanden uit `output/website-liveklaar` worden gepubliceerd. De bronrepository en de gepubliceerde website zijn openbaar.

Een openbare repository werkt met GitHub Pages op GitHub Free. Een eventuele latere overstap naar een privérepository vereist voor Pages een geschikt betaald abonnement.

Eenmalig in GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**. Vervolgens start een push naar `main` of **Actions → Build and deploy portfolio to GitHub Pages → Run workflow** de publicatie.

De workflow leest het echte Pages-adres uit GitHub. Daardoor krijgen sitemap, canonicals, taalverwijzingen en de 404-pagina het juiste domein en eventuele subpad, bijvoorbeeld `https://chantalke.github.io/website/`. Alle gewone links en assets zijn relatief. Een eigen domein kan later in de Pages-instellingen worden ingesteld; deze repository verandert geen DNS.

Dezelfde Pages-build lokaal uitvoeren:

```sh
SITE_URL=https://chantalke.github.io/website ./scripts/deploy-pages.sh
```

Als `python3` anders heet, kan `PYTHON_BIN` worden ingesteld. De standaard URL zonder omgevingsvariabele staat in `website/seo-config.json` en is het latere eigen domein. De workflow gebruikt altijd het echte Pages-adres.

## Inhoud aanpassen

- `website/index.html`: Nederlandse homepage.
- `website/data.js`: projecten, werkervaring, opleiding en media.
- `website/case-notes.js`: tweetalige projectverhalen.
- `website/aanbod-content.json`: aanbod op de samenwerkingspagina's.
- `website/build_locales.py`, `translations.json`, `i18n-en.js`: Engelse vertalingen.
- `website/style.css`, `experience.css`, `seo-pages.css`: vormgeving.
- `website/assets/`: projectbeelden, lokale lettertypes met licenties, video en openbare downloads.

Na wijzigingen altijd `python3 website/build_site.py` uitvoeren. Bouw niet alleen de Engelse pagina opnieuw: de volledige build werkt ook de projectpagina's en vindbaarheidsgegevens bij.

## Privacy en versiebeheer

Losse cv-werkbestanden, backups, interne audits en notities worden niet opgenomen in Git. De gegenereerde uploadmap bevat geen bouwscripts of bron-JSON. Gebruik geen tokens of wachtwoorden in code of workflowbestanden; de workflow gebruikt GitHubs ingebouwde tijdelijke token met beperkte rechten.

De bestanden `_redirects` zijn voor Netlify/Cloudflare Pages. GitHub Pages voert die niet uit; alle siteverwijzingen werken ook zonder deze redirect. De eigen 404-pagina wordt door Pages gebruikt. GitHub verzorgt de hosting en HTTPS; de website bevat geen analytics of automatisch ingesloten externe mediaspelers.
