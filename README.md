# Chantal van Kempen — portfolio website

Dit is de openbare bronrepository van de persoonlijke portfoliosite van **Chantal van Kempen, creatief projectleider en conceptontwikkelaar**. De site laat zien waarvoor je Chantal kunt inschakelen: interactieve talks en ervaringen, serious games en creatieve of maatschappelijke projecten van idee tot uitvoering.

De website is volledig beschikbaar in Nederlands en Engels, met een projectarchief, uitgebreidere projectverhalen, een mediaoverzicht, een persoonlijke introductie en contactmogelijkheden. De vormgeving is magazineachtig, met donker turquoise, crème, roze accenten, projectfotografie, een achtergrondvideo en een easter egg.

- **Website:** https://chantalke.github.io/website/
- **Repository:** https://github.com/chantalke/website
- **Deploymentstatus:** https://github.com/chantalke/website/actions/workflows/pages.yml
- **Instructies voor agents en toekomstige bewerkers:** [AGENTS.md](AGENTS.md)

Het beoogde toekomstige eigen domein is `chantalvankempen.nl`. De huidige publicatie staat op GitHub Pages; deze repository wijzigt geen DNS.

## Wat staat in deze map?

| Bestand of map | Doel |
| --- | --- |
| `AGENTS.md` | Projectcontext, ontwerpafspraken, bronnen, controles en verplichte Git-werkwijze voor agents. |
| `website/` | Websitebron, gegenereerde webpagina's, content, vertalingen en bouwscripts. |
| `website/assets/` | Goedgekeurde foto's, video, lokale lettertypes met licenties en openbare PDF-downloads. |
| `prepare_publish.py` | Maakt en controleert de schone uploadmap met alleen openbare webbestanden. |
| `scripts/deploy-pages.sh` | Voert de GitHub Pages-build lokaal uit. Publiceert zelf niets. |
| `.github/workflows/pages.yml` | Bouwt, controleert en publiceert automatisch bij een push naar `main`. |
| `.gitignore` | Houdt tijdelijke, privé- en gegenereerde werkbestanden buiten de repository. |

De lokale werkmap kan daarnaast `output/`, `backups/`, `tmp/`, `previews/`, cv-werkbestanden en onderzoeksnotities bevatten. Die zijn bewust niet allemaal onderdeel van de Git-repository. Een nieuwe clone bevat de bronbestanden die nodig zijn om de website opnieuw te bouwen.

## Playcards

De tweetalige speelkaarten staan op `/playcards/` en `/playcards/en.html`. De 50 opdrachten en de introductie zijn overgezet van [de oorspronkelijke Playcards](https://playcards.chantalvankempen.nl/). `website/playcards-content.json` bevat de overgenomen Engelse tekst en Nederlandse vertaling; `source_card` verwijst naar het nummer van de oorspronkelijke SVG. De kaartteksten zijn getranscribeerd; de oude afbeeldingen worden niet meer geladen.

`website/build_playcards.py` bouwt beide pagina’s als onderdeel van de volledige build. Opmaak en interactie staan in `website/playcards.css` en `website/playcards.js`. De stapel wordt zonder herhaling geschud; terugbladeren blijft mogelijk. Alle kaarten zijn ook beschikbaar als uitklapbare tekstversie.

## Techniek

De website is statisch: HTML, CSS en JavaScript. Er is geen framework, database, formulierbackend of serverapplicatie nodig. Python en Node worden alleen gebruikt om de webbestanden te bouwen en controleren. Er zijn geen pip- of npm-pakketten nodig.

Voor het opnieuw bouwen: **Python 3.12** en **Node.js 22**, of compatibele versies. Lettertypes worden lokaal geladen. Video's en podcasts op externe platforms openen via links; er zijn geen automatisch ingesloten externe spelers of analytics toegevoegd.

## Lokaal bekijken

Vanuit de hoofdmap van deze repository:

```sh
python3 website/build_site.py
python3 prepare_publish.py
python3 -m http.server 8765 --directory output/website-liveklaar
```

Open http://localhost:8765/. Stop de lokale server met `Ctrl+C`.

De eerste opdracht bouwt beide talen, de project- en aanbodpagina's, de zoekmachinegegevens en de sitemap. Daarna controleert hij links en metadata. De tweede opdracht maakt `output/website-liveklaar/` en controleert de bestanden in die uploadkopie. Deze opdrachten publiceren niets.

Als je alleen de bestaande bronpagina's wilt bekijken, kun je ook `python3 -m http.server 8765 --directory website` gebruiken. Bouw opnieuw na inhoudelijke wijzigingen, zodat de Engelse en gegenereerde pagina's bijgewerkt zijn.

## Waar pas je inhoud aan?

| Onderdeel | Bron |
| --- | --- |
| Nederlandse homepage | `website/index.html` |
| Nederlandse mediapagina | `website/media.html` |
| Projecten, opdrachten, opleiding, talks en media | `website/data.js` |
| Beoordeelde openbare projectteksten | `website/public-project-copy.json` |
| Uitgebreidere projectverhalen in beide talen | `website/case-notes.js` |
| Aanbod op Samenwerken / Working together | `website/aanbod-content.json` |
| Engelse data en paginaopbouw | `website/build_locales.py` |
| Vertaling van vaste en dynamische interface-tekst | `website/translations.json`, `website/i18n-en.js` en overige vertaal-JSON |
| Project-, spreker- en samenwerkingspagina's en SEO | `website/build_seo.py` |
| Probleemgerichte pagina's | `website/build_challenges.py` |
| Kleuren, typografie, layout en mobiele weergave | `website/style.css`, `website/experience.css`, `website/seo-pages.css` |
| Filters, projectvensters en easter egg | `website/app.js` |
| Themavragen | `website/experience.js` |
| Chronologisch mediaoverzicht | `website/media.js`, `website/chronology.js` |
| E-mailadres kopiëren | `website/contact-email.js` |

Bewerk de bron van een gegenereerde pagina, niet alleen de gegenereerde uitvoer. `data.en.js`, Engelse HTML en project-/spreker-/aanbodpagina's kunnen bij de volgende build worden overschreven. Na een wijziging altijd de volledige build draaien en relevante gegenereerde bestanden mee committen. Houd Nederlands en Engels gelijk bijgewerkt.

## Git: incrementele backup van alle projectwijzigingen

**Alle afgeronde wijzigingen aan de website en bijbehorende projectbestanden worden vastgelegd in Git.** Maak kleine, begrijpelijke commits per afgeronde stap. Zo kunnen we terugvinden wat veranderde en terug naar een eerdere versie zonder het hele project opnieuw op te bouwen.

De normale werkwijze:

1. Bekijk eerst `git status` en behoud eventueel bestaand werk van anderen.
2. Voer een afgebakende wijziging uit en controleer het resultaat.
3. Bekijk `git diff` en voeg alleen de bestanden van die wijziging toe.
4. Commit met een duidelijke omschrijving.
5. Push naar de bestaande remote voor de kopie op GitHub. Een push naar `main` publiceert ook de website.
6. Controleer de Actions-workflow en laat geen afgerond eigen werk onbedoeld ongecommit achter.

Voorbeeld:

```sh
git status --short
git diff
# Voeg hier de specifieke gewijzigde bestanden toe:
git add AGENTS.md README.md .gitignore
git commit -m "Document project context and version-control workflow"
git push origin main
```

Een lokale commit bewaart de versie lokaal; pas na een push staat die ook op GitHub. Niet-gecommitteerde of genegeerde bestanden vallen niet onder deze backup. Houd secrets en privébestanden altijd buiten de publieke geschiedenis.

### Terug naar een eerdere versie

Bekijk eerdere stappen met `git log --oneline`. Gebruik `git show <commit>` om een wijziging te bekijken. Draai een specifieke gepubliceerde wijziging terug met `git revert <commit>`: dat maakt een nieuwe herstelcommit en behoudt de bestaande geschiedenis. Controleer en push die herstelcommit om ook de live website bij te werken. Gebruik geen force-push of destructieve reset om routinewijzigingen terug te draaien.

## Automatische publicatie met GitHub Pages

De repository en de website zijn openbaar. GitHub Pages is ingesteld op **GitHub Actions**. Bij iedere push naar `main` voert `.github/workflows/pages.yml` deze stappen uit:

1. De bron ophalen en Python en Node klaarzetten.
2. Het echte GitHub Pages-adres uitlezen.
3. Beide talen bouwen en de website en JavaScript controleren.
4. Alleen de schone uploadmap als artifact aanbieden.
5. Die gecontroleerde bestanden publiceren op GitHub Pages.

Je kunt dezelfde workflow handmatig starten via **Actions → Build and deploy portfolio to GitHub Pages → Run workflow**. Een mislukte build wordt niet als een geslaagde publicatie gerapporteerd; bekijk de foutmelding in de betreffende run.

De workflow gebruikt het echte Pages-adres voor sitemap, canonicals, taalverwijzingen en de 404-pagina. Relatieve links en assets ondersteunen het subpad `/website/`. De eigen 404-pagina wordt door Pages gebruikt. `_redirects` is bedoeld voor andere hosts zoals Netlify/Cloudflare Pages en wordt door GitHub Pages niet uitgevoerd.

## Een Pages-build lokaal testen

```sh
SITE_URL=https://chantalke.github.io/website ./scripts/deploy-pages.sh
```

Dit bouwt en controleert lokaal; het script commit, pusht en publiceert niet. Als Python anders heet, kun je `PYTHON_BIN` instellen. Node moet beschikbaar zijn in je `PATH`.

`SITE_URL` overschrijft voor die build het standaarddomein uit `website/seo-config.json`. De workflow stelt deze variabele automatisch in. Bouw na een lokale subpadtest zonder `SITE_URL` opnieuw als je terug wilt naar de standaard metadata in de bronbestanden. Verander een domein of DNS alleen bewust en op verzoek.

## Controles bij wijzigingen

- `python3 website/build_site.py`: interne links, ankers, titels, headings, sitemap en wederkerige taalverwijzingen.
- `python3 prepare_publish.py`: de uploadkopie, afbeeldingsalternatieven, dubbele IDs, lokale CSS/font- en videobestanden.
- `node --check website/app.js`: syntaxcontrole van een gewijzigd JavaScript-bestand; pas de bestandsnaam aan waar nodig.
- `git diff --check`: onbedoelde whitespaceproblemen.
- Browsercontrole bij visuele of interactieve wijzigingen: mobiel, tablet, desktop en de relevante Nederlandse én Engelse route.

Een documentatiewijziging vraagt geen volledig visueel onderzoek. Een gewijzigde build of publicatie-URL vraagt wel een test vanuit een schone checkout, zodat de build niet afhankelijk wordt van lokale genegeerde bestanden.

## Openbare en privébestanden

De bronrepository is openbaar. Voeg geen tokens, wachtwoorden, `.env`-bestanden, privé-cv's, ongecontroleerde documenten of interne notities toe. De workflow gebruikt GitHubs ingebouwde tijdelijke token met beperkte rechten. Goedgekeurde portfolio- en impactrapportdownloads onder `website/assets/` zijn onderdeel van de openbare website.

`output/website-liveklaar/` bevat geen Python-bouwscripts, bron-JSON of interne documentatie. De oudere magazinevarianten en vervangen hero-video blijven eventueel lokaal bewaard en worden niet meegestuurd.

Let op: `.gitignore` gebruikt voor de hoofdmap een **allowlist**. Voeg een nieuwe hoofdmap of een nieuw bronbestand expliciet toe aan die lijst als het onderdeel van het project moet worden. Het is niet de bedoeling dat echte projectwijzigingen daardoor onopgemerkt buiten de Git-backup blijven.
