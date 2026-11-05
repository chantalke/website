# Agent instructions — Chantal van Kempen portfolio

These instructions apply to the entire repository. Read this file and `README.md` before making changes. The latest explicit instructions from Chantal take precedence over these defaults.

## Project and current state

- This is Chantal van Kempen's personal, bilingual Dutch/English portfolio website.
- Positioning: **creatief projectleider & conceptontwikkelaar** — creative concepts, people and realisation. Experience design is a distinctive expertise. Do not reposition her primarily around efficiency, ERP consulting or making schedules.
- Public repository: https://github.com/chantalke/website
- Live website: https://chantalke.github.io/website/
- `main` is the published branch. GitHub Actions builds and deploys every push to `main`.
- `https://chantalvankempen.nl` is the intended future custom domain. It is not connected by this repository. Do not change DNS or Pages domain settings without a request.
- There are currently 40 public pages, including both languages, project stories, speaking, collaboration, media and problem-oriented pages. This count can change when pages are deliberately added.
- The site is static HTML/CSS/JavaScript. Python and Node are build tools; there is no application backend, package installation or database required.

## Git is the incremental backup — mandatory

**Record every completed change to tracked project source in Git.** This includes content, translations, styling, scripts, approved assets, configuration and documentation. Do not finish an editing task with your completed changes left uncommitted.

1. Start with `git status --short`, inspect the current branch and preserve any existing user changes.
2. Work in small, coherent steps. Before a substantial experiment or redesign, commit the existing work you own first so there is a clear restore point. Do not create empty commits for read-only tasks.
3. Inspect the diff and run checks appropriate to the change. Stage only files belonging to your task; never blindly include unrelated user work.
4. Commit each completed logical step with a concise description of what changed. Use additional commits for later fixes. Do not squash away useful incremental history just for tidiness.
5. Push tested commits to the existing `origin` to keep the remote backup current, unless Chantal requests local-only work, a draft or no publication. Remember that a push to `main` also publishes the site. Respect explicit approval or branch requirements if the workflow changes.
6. After a push to `main`, check the GitHub Pages workflow result. If it fails, inspect the failure and fix it within scope; do not claim publication succeeded until verified.
7. End with `git status --short`. Report the commit SHA, whether it was pushed, and any remaining changes or blocked verification. Never silently discard changes to obtain a clean status.

Do not force-push, rewrite shared history, use destructive reset/clean commands, or delete branches/backups without an explicit request. Restore previous versions by making a new commit or reverting a selected commit. A commit is a restore point for tracked files, not a backup of everything on the computer; a push adds the remote copy.

Secrets, authentication tokens, `.env` files, private documents, temporary renders, caches and local backup archives must stay out of this public repository. This is an exception for excluded/private files, not a reason to leave actual website changes untracked. Check `.gitignore` when adding a new root-level source file: the root uses an allowlist.

## Preserve the established design and voice

- Keep the magazine-like layout: dark turquoise, warm cream, pink/coral accents, expressive typography, a little mystery and playfulness.
- Preserve the existing palette and shared photo treatment. Avoid unsolicited global redesigns or a return to loud colours. Make targeted adjustments unless a redesign is explicitly requested.
- Keep visible copy short. Put detail in project stories or existing accordions rather than adding long homepage sections.
- Make it clear when someone should call Chantal: an event, a learning/development experience, or a creative/social initiative that needs direction and delivery.
- Experiences are primarily physical and sometimes blended. Do not imply a primarily digital product offering.
- The hero uses the supplied video; the portrait belongs in the personal introduction and fades into the page background.
- The homepage project selection starts with immersive experiences. Keep each selected project in a single homepage filter; a full archive remains separately searchable.
- Preserve the themed doors, easter egg, video pause control, reduced-motion handling and persistent WhatsApp contact link.
- Do not invent project results, clients, dates, personal responsibilities, testimonials or completed programmes. Attribute joint work correctly. Distinguish ambitions and concepts in development from delivered work.
- There is no personal Instagram account to promote. Some historical project links may legitimately point to an organisation's account.
- Preserve accessible contrast, visible keyboard focus, meaningful image alternatives and usable mobile/tablet navigation.

## Edit the source of truth

| Concern | Main files |
| --- | --- |
| Dutch homepage and media structure | `website/index.html`, `website/media.html` |
| Projects, career, education, talks and media data | `website/data.js` |
| Approved public project wording | `website/public-project-copy.json` |
| Detailed bilingual project stories | `website/case-notes.js` |
| Project URLs and confirmed full dates | `website/project-routes.js`, `website/chronology.js` |
| Collaboration offer | `website/aanbod-content.json` |
| English data and page generation | `website/build_locales.py` |
| Static and dynamic translations | `website/translations.json`, `website/i18n-en.js`, translation JSON files |
| Problem-oriented pages | `website/build_challenges.py` |
| Project/speaker/collaboration pages, snapshots and SEO | `website/build_seo.py` |
| UI behaviour | `website/app.js`, `website/experience.js`, `website/media.js`, `website/contact-email.js` |
| Styling | `website/style.css`, `website/experience.css`, `website/seo-pages.css` |
| Publication URL and subpath support | `website/site_config.py`, `website/seo-config.json` |
| Build, verification and clean upload output | `website/build_site.py`, `website/verify_site.py`, `prepare_publish.py` |
| GitHub Pages deployment | `.github/workflows/pages.yml`, `scripts/deploy-pages.sh` |

Do not hand-edit generated English data or generated project/speaker/problem HTML as the only fix: the next build would overwrite it. Update the relevant builder, content file or translation, then run the complete build. Generated HTML and JS in `website/` are tracked; include the relevant generated changes in the commit. `output/` is generated and ignored.

Keep Dutch and English in sync. Proper names can remain in their original language. Dutch PDF downloads must be labelled as Dutch on the English site. Local fonts and their licences are under `website/assets/fonts/`.

## Validation and publication

Use Python 3.12 and Node.js 22, or compatible installed versions. No pip/npm dependencies are required.

```sh
python3 website/build_site.py
python3 prepare_publish.py
```

The full build checks local targets/anchors, canonical and reciprocal language metadata, headings and crawlable content. The packaging step checks the upload copy, images, CSS/font assets and video sources. Check changed JavaScript with `node --check path/to/file.js`.

For GitHub Pages-specific URL/subpath changes, also test a clean checkout or temporary copy without ignored local files:

```sh
SITE_URL=https://chantalke.github.io/website ./scripts/deploy-pages.sh
```

That script builds locally; it does not push or publish. It rewrites generated metadata for the chosen URL. If returning to a custom-domain local build, rebuild without `SITE_URL` before committing generated files. The Actions workflow supplies the actual Pages URL during deployment.

For layout/interaction changes, inspect relevant pages in a browser at mobile, tablet and desktop widths and exercise the affected controls. For documentation-only changes, review the text, links and `git diff --check`; a full visual regression is unnecessary.

Keep internal links/assets relative so `/website/` continues to work. GitHub Pages does not execute `_redirects`. Keep the custom 404 page and its asset/home links functional under the publication subpath. Do not add a `CNAME` or point metadata at a different host without understanding the requested deployment target.

No analytics, form backend or automatic external video embeds are currently used. Email opens a copy-address dialog; WhatsApp is a visitor-initiated link. Do not add tracking or start sending messages as part of routine website edits.
