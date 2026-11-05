"""Generate crawlable content and production metadata; never deploys anything."""
from pathlib import Path
from html import escape as esc
import json, re, shutil, subprocess
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
from site_config import SITE_URL as BASE
assert urlsplit(BASE).scheme=='https' and urlsplit(BASE).hostname not in ['localhost','127.0.0.1'], 'Use the intended public HTTPS domain'
DATA={lang:json.loads((ROOT/name).read_text().removeprefix('const DATA = ').strip().removesuffix(';')) for lang,name in [('nl','data.js'),('en','data.en.js')]}
PUBLIC_PROJECT_COPY=json.loads((ROOT/'public-project-copy.json').read_text())
(ROOT/'public-project-copy.js').write_text('const PUBLIC_PROJECT_COPY = '+json.dumps(PUBLIC_PROJECT_COPY,ensure_ascii=False)+';\n')
for lang,data in DATA.items():
    for project in data['projects']:project.update(PUBLIC_PROJECT_COPY[lang].get(project['id'],{}))
NODE=shutil.which('node') or str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node')
def js_value(file,expression):
    script='const fs=require("fs"),vm=require("vm");process.stdout.write(JSON.stringify(vm.runInNewContext(fs.readFileSync(process.argv[1],"utf8")+";"+process.argv[2])));'
    return json.loads(subprocess.check_output([NODE,'-e',script,str(ROOT/file),expression],text=True))
NOTES=js_value('case-notes.js','CASE_NOTES')
ROUTES=js_value('project-routes.js','PROJECT_ROUTES')
DATES=js_value('chronology.js','CONFIRMED_DATES')
SELECTED=['P001','P002','P003','P004','P005','P006','P008','P020','P031','P016','P007']
WORDS=['FUTURE<br>VILLAGE','PLAN<br>JE ROT','FEEL<br>HEALTH','THE NIGHTINGALE<br>SOCIETY','BEYOND<br>ASSUMPTIONS','LOOP JE<br>EIGEN PAD','MAKE IT<br>VISIBLE.','WUNDER<br>NACHT','HUMAN<br>TECH','TALENT<br>IN MOTION','OFFICE<br>365']
GROUPS={'nl':['Sociale innovatie','Serious games','Immersieve ervaringen','Immersieve ervaringen','Immersieve ervaringen','Immersieve ervaringen','Serious games','Immersieve ervaringen','Sociale innovatie','Sociale innovatie','Serious games'],'en':['Social innovation','Serious games','Immersive experiences','Immersive experiences','Immersive experiences','Immersive experiences','Serious games','Immersive experiences','Social innovation','Social innovation','Serious games']}
PAIRS=[('index.html','index-en.html'),('media.html','media-en.html'),('spreker.html','speaker.html'),('medewerkers-meekrijgen-in-verandering.html','engaging-employees-in-change.html'),('samenwerking-tussen-afdelingen.html','collaboration-between-teams.html'),('leren-door-ervaring.html','experiential-learning.html'),('patronen-doorbreken.html','breaking-patterns.html')]
PAIRS += [('playcards/index.html','playcards/en.html')]
PAIRS += [(f'project-{slug}.html',f'project-{slug}-en.html') for slug in ROUTES.values()]
def absolute(file):return BASE+'/' if file=='index.html' else BASE+'/playcards/' if file=='playcards/index.html' else BASE+'/'+file
def case_url(id,lang):return f'project-{ROUTES[id]}'+('-en' if lang=='en' else '')+'.html'
def external(url,label):
    return f'<a href="{esc(url,quote=True)}" target="_blank" rel="noopener noreferrer">{esc(label)} ↗</a>' if url.startswith(('http://','https://')) else ''
def date_label(id,year,lang):
    date=DATES.get(id)
    if not date:return year or ('Date unknown' if lang=='en' else 'Datum onbekend')
    y,m,d=date.split('-');return f'{int(d)} {(["jan","feb","mrt","apr","mei","jun","jul","aug","sep","okt","nov","dec"] if lang=="nl" else ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])[int(m)-1]} {y}'
def order_key(id,year):
    match=re.search(r'\b(?:19|20)\d{2}\b',str(year));return (int(match[0]) if match else 0,DATES.get(id,''))
def slot(source,id,content):
    start=f'<!--seo:{id}:start-->';end=f'<!--seo:{id}:end-->'
    if start in source:return re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:start+content+end,source,flags=re.S)
    pattern=r'(<div\b[^>]*\bid="'+re.escape(id)+r'"[^>]*>)\s*</div>'
    result,n=re.subn(pattern,lambda m:m[1]+start+content+end+'</div>',source,count=1)
    assert n==1,f'Missing prerender slot: {id}'
    return result
def photo_html(photo,cover=False):
    return f'<img src="{esc(photo["src"])}" width="{photo["width"]}" height="{photo["height"]}" alt="{esc(photo["alt"],quote=True)}" loading="lazy" decoding="async" class="{"project-photo" if cover else "gallery-photo"}{" photo-lowlight" if photo.get("tone")=="lowlight" else ""}">'
def photo_gallery(p):
    return '<div class="project-gallery">'+''.join('<figure>'+photo_html(im)+(f'<figcaption>© {esc(im["credit"])}</figcaption>' if im.get('credit') else '')+'</figure>' for im in p.get('images',[]))+'</div>' if p.get('images') else ''
def project_tags(p,limit=None):
    tags=p.get('tags',[])[:limit]
    return '<ul class="project-tags">'+''.join(f'<li>{esc(t)}</li>' for t in tags)+'</ul>' if tags else ''
def logo():return (ROOT/'assets/cosmic-mark.svg').read_text().strip().replace('<svg ','<svg class="cosmic-mark" aria-hidden="true" focusable="false" ',1)
def shell(lang,title,description,body,other):
    en=lang=='en';home='index-en.html' if en else 'index.html';speaker='speaker.html' if en else 'spreker.html';media='media-en.html' if en else 'media.html'
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(description,quote=True)}"><link rel="stylesheet" href="style.css?v=seo-1"><link rel="stylesheet" href="experience.css?v=seo-1"><link rel="stylesheet" href="seo-pages.css?v=seo-1"></head><body class="experience-v2"><a class="skip" href="#main">{'Skip to content' if en else 'Naar de inhoud'}</a><header><a class="brand" href="{home}">Chantal<br>van Kempen<span class="brand-symbol">{logo()}</span></a><nav aria-label="{'Main navigation' if en else 'Hoofdnavigatie'}"><a href="{speaker}">{'Speaking' if en else 'Spreken'}</a><a href="{home}#werk">{'Work' if en else 'Werk'}</a><a href="{media}">Media</a><a class="nav-contact" href="https://wa.me/31619208308" target="_blank" rel="noopener noreferrer">WhatsApp ↗</a><span class="language-switch"><a href="{other if en else speaker}" lang="nl">NL</a><span>/</span><a href="{speaker if en else other}" lang="en">EN</a></span></nav></header><main id="main">{body}</main><footer><span>Chantal van Kempen · {'Creative concept developer & project leader' if en else 'Creatief conceptontwikkelaar & projectleider'}</span><a href="{home}">{'Back to my world' if en else 'Terug naar mijn wereld'} ↗</a><a href="tel:+31619208308">+31 6 1920 8308</a></footer></body></html>'''

# Nine real case studies, with content that exists independently of the homepage dialog.
for id,slug in ROUTES.items():
    for lang in ['nl','en']:
        en=lang=='en';p=next(p for p in DATA[lang]['projects'] if p['id']==id)
        note=NOTES.get(id);url=case_url(id,lang);other=case_url(id,'nl' if en else 'en');home='index-en.html' if en else 'index.html'
        i=SELECTED.index(id) if id in SELECTED else 6
        sections=note[lang] if note else ([['The challenge','How can employees explore bottlenecks in procurement together?'],['The experience',p['description']],['My contribution',p['role']+' — '+p['client']]] if en else [['De vraag','Hoe laat je medewerkers samen knelpunten in het inkoopproces onderzoeken?'],['De ervaring',p['description']],['Mijn bijdrage',p['role']+' — '+p['client']]])
        body=f'<article class="project-story"><div class="story-heading"><p class="eyebrow">PROJECT / {esc(p["category"])}</p><h1>{esc(p["title"])}</h1><p class="story-intro">{esc(p["description"])}</p><dl class="story-facts"><div><dt>{"Client / partner" if en else "Opdrachtgever / partner"}</dt><dd>{esc(p["client"])}</dd></div><div><dt>{"My role" if en else "Mijn rol"}</dt><dd>{esc(p["role"])}</dd></div><div><dt>{"Period" if en else "Periode"}</dt><dd>{esc(p["year"])}</dd></div></dl></div><div class="art art-{i} story-art" aria-hidden="true"><span class="art-word">{WORDS[i] if id in SELECTED else (("FOCUS.<br>COLLABORATION." if en else "FOCUS.<br>SAMENWERKING.") if id=="P012" else "BUILD.<br>EXPLORE.")}</span></div><div class="story-copy">'
        
        if p.get('images'):
            body=re.sub(r'<div class="art art-\d+ story-art".*?</div>',lambda _: f'<div class="art photo-art photo-art-{i}{" artwork-cover" if p.get("cover_artwork") else ""} story-art">'+photo_html(p['images'][0],True)+f'<span class="art-word">{WORDS[i] if id in SELECTED else esc(p["title"])}</span></div>',body,count=1,flags=re.S)
        body+=project_tags(p)+photo_gallery(p)

        body+=''.join(f'<section><h2>{esc(h)}</h2><p>{esc(t)}</p></section>' for h,t in sections)
        for doc in p.get('documents',[]):
            heading='Read the impact report' if en else 'Bekijk het impactonderzoek'
            title=doc['title_en'] if en else doc['title']
            meta=f'{doc["author"]} · {"13 January 2026" if en else "13 januari 2026"} · PDF · {doc["pages"]} {"pages" if en else "pagina’s"} · 10 MB · {"Dutch" if en else "Nederlands"}'
            method='Based on 44 interviews, observations and creative research activities. The study describes experiences during the programme; longer-term effects were not established.' if en else 'Gebaseerd op 44 interviews, observaties en creatieve meetvormen. Het onderzoek beschrijft ervaringen tijdens het programma; effecten op langere termijn zijn niet vastgesteld.'
            body+=f'<section class="impact-report"><p class="eyebrow">{esc(doc["author"])}</p><h2>{heading}</h2><p class="small">{esc(meta)}</p><p>{method}</p><div class="report-actions"><a class="pill" href="{esc(doc["href"])}" target="_blank" rel="noopener noreferrer">{title} ↗</a><a class="text-link" href="{esc(doc["href"])}" download>{"Download report" if en else "Download rapport"} ↓</a></div></section>'
        if note and note.get('video'):body+=external(note['video'],'Watch the original project video' if en else 'Bekijk de oorspronkelijke projectvideo')
        if p['url']:body+='<p>'+external(p['url'],(('Organisation website' if en else 'Website organisatie') if p.get('url_kind')=='organisation' else ('Background about this initiative' if en else 'Achtergrond bij dit initiatief') if p.get('url_kind')=='background' else ('Related project source' if en else 'Bron bij dit project')))+'</p>'
        if id in ['P001','P012','P031','P016']:
            invitation='An ambition to build on?' if en else 'Een ambitie die je wilt realiseren?'
            invitation_text='Tell me what you want to build. We can explore how I can contribute through concept development, facilitation or creative project leadership.' if en else 'Vertel me wat je wilt opbouwen. Samen kijken we hoe ik kan bijdragen met conceptontwikkeling, begeleiding of creatieve projectleiding.'
        else:
            invitation='An experience for your audience or programme?' if en else 'Een ervaring voor jouw publiek of programma?'
            invitation_text='Tell me what you want people to explore or experience. Together we can find a format that fits.' if en else 'Vertel me wat je mensen wilt laten onderzoeken of ervaren. Samen vinden we een vorm die past.'
        body+=f'<aside class="story-next"><h2>{invitation}</h2><p>{invitation_text}</p><a class="pill" href="https://wa.me/31619208308" target="_blank" rel="noopener noreferrer">WhatsApp ↗</a></aside><a href="{home}#werk">{"Explore more work" if en else "Bekijk meer werk"} ↗</a></div></article>'
        page=shell(lang,p['title']+' | Chantal van Kempen',p['description'],body,other)
        # Use the case counterpart, not the speaker page, in each language switch.
        page=page.replace(f'href="{"speaker.html" if en else "spreker.html"}" lang="{lang}"',f'href="{url}" lang="{lang}" aria-current="true"')
        (ROOT/url).write_text(page)

SPEAKER={
'nl':{'title':'Spreker over verwondering & verbinding | Chantal van Kempen','description':'Een interactieve talk over verwondering, menselijk contact en anders kijken. Ontdek Chantal van Kempen als spreker en bespreek je bijeenkomst.','heading':'Een ander perspectief. Een ervaring die je zelf onderzoekt.','intro':'Ik ben Chantal van Kempen: spreker en experience designer. Ik verbind psychologie, spel en verbeelding in talks die uitnodigen tot aandacht, nieuwsgierigheid en ontmoeting.','audience':'Voor conferentieprogrammeurs, culturele organisaties, communities en teams die een onderwerp samen willen onderzoeken. Denk aan een bijeenkomst over menselijke verbinding, leren of de manier waarop we naar de toekomst kijken.','topics':[['Verwondering & ineffable','Wat missen we als we alles willen uitleggen? Over ervaringen die moeilijk in woorden te vangen zijn, aandacht en anders waarnemen.'],['Verbinding & sociale cohesie','Wanneer wordt een vreemde iemand van ons? Over ontmoeting, erbij horen en ruimte maken voor verschillende perspectieven.'],['Mogelijke toekomsten & filosofie','Wat als jouw werkelijkheid niet de enige is? Een uitnodiging om aannames te onderzoeken en mogelijke toekomsten te verkennen.']],'process':[['Jouw vraag','We bespreken het publiek, de aanleiding en wat je met de bijeenkomst wilt openen.'],['De vorm','We onderzoeken of een keynote, interactieve talk of begeleid gesprek past. Inhoud, taal, duur en praktische voorwaarden stemmen we samen af.'],['De ontmoeting','Verhalen en kleine uitnodigingen kunnen deelnemers zelf laten onderzoeken. Een reflectie verbindt de ervaring aan hun eigen context.']],'evidence':'Eerdere podia','evidenceintro':'Mijn eerdere optredens omvatten spreken, roundtable-hosting en een expertpanel. Hieronder staat steeds mijn eigen rol.','invitation':'Welke vraag wil jij openen?','cta':'Bespreek een talk ↗','note':'De genoemde thema’s zijn mogelijke vertrekpunten; we kiezen samen de inhoud. Het afzonderlijke concept voor diepgaande ontwikkelingservaringen is nog in ontwikkeling.'},
'en':{'title':'Speaker on wonder & human connection | Chantal van Kempen','description':'An interactive talk on wonder, human connection and seeing differently. Explore Chantal van Kempen’s speaking work and discuss your event.','heading':'A different perspective. An experience to explore for yourself.','intro':'I’m Chantal van Kempen, a speaker and experience designer. I bring psychology, play and imagination into talks that invite attention, curiosity and human connection.','audience':'For conference organisers, cultural organisations, communities and teams exploring a question together. This could be an event about human connection, learning or the way we imagine the future.','topics':[['Wonder & the ineffable','What do we miss when we try to explain everything? Exploring experiences beyond words, attention and seeing differently.'],['Connection & social cohesion','When does a stranger become one of us? On encounters, belonging and making room for different perspectives.'],['Possible futures & philosophy','What if your reality is not the only one? An invitation to question assumptions and explore possible futures.']],'process':[['Your question','We discuss your audience, the occasion and what you want to open up through the event.'],['The format','We explore whether a keynote, interactive talk or facilitated conversation fits. We agree on content, language, duration and practical requirements together.'],['The encounter','Stories and small invitations can let participants explore for themselves. Reflection connects the experience to their own context.']],'evidence':'Previous appearances','evidenceintro':'My previous appearances include speaking, roundtable hosting and an expert panel. Each entry states my actual role.','invitation':'What question would you like to open up?','cta':'Discuss a talk ↗','note':'These themes are possible starting points; we shape the content together. The separate concept for immersive development experiences is still in development.'}}

SPEAKER_OVERRIDES = {
'nl': {'heading':'Een talk die raakt. Of een ervaring die je bijblijft.', 'intro':'Voor een publiek dat meer wil dan luisteren. Ik verbind psychologie, spel en verbeelding in interactieve talks en gezamenlijke ervaringen rond verwondering, menselijk gedrag en anders kijken.', 'audience':'Voor programmamakers van conferenties, culturele evenementen en bijeenkomsten van organisaties. Je zoekt een spreker die mensen aan het denken zet, of juist een ervaring die deelnemers samen een nieuw perspectief laat onderzoeken.', 'cta':'Bespreek je evenement ↗', 'note':'We spreken inhoud, taal, duur, groepsgrootte, toegankelijkheid en praktische voorwaarden vooraf af.', 'process':[['De aanleiding','Wie komt er, wat speelt er en waarmee wil je je publiek naar huis laten gaan?'],['De vorm','Een keynote, een interactieve talk of een gezamenlijke ervaring. We kiezen een vorm die past bij je programma, ruimte en publiek.'],['De vertaling','We verbinden wat deelnemers meemaken aan hun eigen werk of leven, met ruimte voor gesprek en reflectie.']]},
'en': {'heading':'A talk that moves you. Or an experience that stays.', 'intro':'For an audience ready to do more than listen. I bring psychology, play and imagination into interactive talks and shared experiences exploring wonder, human behaviour and different perspectives.', 'audience':'For programme makers at conferences, cultural events and organisational gatherings. You are looking for a speaker who sparks thought, or an experience where participants explore a new perspective together.', 'cta':'Discuss your event ↗', 'note':'We agree on content, language, duration, group size, accessibility and practical requirements in advance.', 'process':[['The occasion','Who is coming, what matters to them and what would you like them to take away?'],['The format','A keynote, an interactive talk or a shared experience. We choose a format that fits your programme, space and audience.'],['The connection','We connect what participants experience to their own work or lives, with space for conversation and reflection.']]}}
for language, changes in SPEAKER_OVERRIDES.items(): SPEAKER[language].update(changes)
for lang,c in SPEAKER.items():
    en=lang=='en';name='speaker.html' if en else 'spreker.html';other='spreker.html' if en else 'speaker.html'
    body=f'<article class="speaker-page"><section class="speaker-opening"><div><p class="eyebrow">CHANTAL VAN KEMPEN / {"SPEAKING" if en else "SPREKEN"}</p><h1>{esc(c["heading"])}</h1><p>{esc(c["intro"])}</p><a class="pill" href="#booking">{c["cta"]}</a></div><figure class="speaker-stage-photo"><img src="assets/gamification-europe-2024.webp" width="1080" height="810" alt="{"Chantal speaking at Gamification Europe in 2024" if en else "Chantal als spreker bij Gamification Europe in 2024"}" fetchpriority="high"><figcaption>Gamification Europe · 2024</figcaption></figure></section><section class="speaker-content"><div class="format-choice"><section><h2>{"A talk" if en else "Een talk"}</h2><p>{"Stories, sharp questions and small experiments. For an audience that wants to think along and see differently." if en else "Verhalen, scherpe vragen en kleine experimenten. Voor een publiek dat wil meedenken en anders wil kijken."}</p></section><section><h2>{"A shared experience" if en else "Een gezamenlijke ervaring"}</h2><p>{"Participants explore a question through play or an assignment, followed by conversation and reflection. See the Positive Health Experience for an example of my approach." if en else "Deelnemers onderzoeken een vraag via spel of een opdracht, gevolgd door gesprek en reflectie. Bekijk de zorgexperience als voorbeeld van mijn aanpak."}</p><a href="project-positive-health-experience{"-en" if en else ""}.html">{"Explore the experience" if en else "Bekijk de ervaring"} ↗</a></section></div><h2>{"For your audience" if en else "Voor jouw publiek"}</h2><p>{esc(c["audience"])}</p><h2>{"Themes to explore" if en else "Thema’s om te onderzoeken"}</h2><div class="speaker-topics">'
    body+=''.join(f'<section><h3>{esc(h)}</h3><p>{esc(t)}</p></section>' for h,t in c['topics'])+'</div>'
    body+=f'<h2>{"How we work together" if en else "Zo werken we samen"}</h2><ol>'+''.join(f'<li><h3>{h}</h3><p>{t}</p></li>' for h,t in c['process'])+'</ol>'
    body+=f'<h2 id="eerdere-podia">{c["evidence"]}</h2><p>{c["evidenceintro"]}</p>'
    talks=[r for r in DATA[lang]['talks'] if r[0] in ['S001','S002','S003','S004','S005']]
    talks.sort(key=lambda r:order_key(r[0],r[1]),reverse=True)
    for t in talks:body+=f'<article class="record"><span class="date">{esc(date_label(t[0],t[1],lang))}</span><div><p>{esc(t[3])} · {esc(t[4])}</p><h3>{esc(t[2])}</h3><p>{esc(t[5])}</p></div>{external(t[7],"Source" if en else "Bron")}</article>'
    body+=f'<p><a href="{"media-en.html" if en else "media.html"}">{"All talks, interviews and podcasts" if en else "Alle talks, interviews en podcasts"} ↗</a></p><aside class="story-next" id="booking"><h2>{c["invitation"]}</h2><p>{"Tell me about your event, audience and the question you’re exploring." if en else "Vertel me over je bijeenkomst, publiek en de vraag die je wilt onderzoeken."}</p><a class="pill" href="https://wa.me/31619208308" target="_blank" rel="noopener noreferrer">WhatsApp ↗</a><p><a href="mailto:chantalke@gmail.com">chantalke@gmail.com</a> · <a href="tel:+31619208308">+31 6 1920 8308</a></p><p class="small">{c["note"]}</p></aside></section></article>'
    (ROOT/name).write_text(shell(lang,c['title'],c['description'],body,other))

# Prerender the same portfolio and archive data that the browser enhancements use.
for lang in ['nl','en']:
    en=lang=='en';name='index-en.html' if en else 'index.html';source=(ROOT/name).read_text();data=DATA[lang]
    projects=''
    for i,id in enumerate(SELECTED):
        if id not in ['P003','P004','P005','P006','P020']:continue
        p=next(p for p in data['projects'] if p['id']==id)
        art=(f'<div class="art photo-art photo-art-{i}{" artwork-cover" if p.get("cover_artwork") else ""}">'+photo_html(p['images'][0],True)+f'<span class="art-word">{WORDS[i]}</span><span class="art-label">{esc(GROUPS[lang][i].upper())} / {i+1:02}</span></div>') if p.get('images') else f'<div class="art art-{i}"><span class="art-label">{esc(GROUPS[lang][i].upper())} / {i+1:02}</span><span class="art-word">{WORDS[i]}</span></div>'
        projects+=f'<article class="project-tile"><a class="project" href="{case_url(id,lang)}">{art}<div class="project-meta"><span>{esc(p["client"])}</span><span>{esc(p["year"])}</span></div><h3>{esc(p["title"])}</h3><p>{esc(p["description"])}</p><span class="project-read">{"View project" if en else "Project bekijken"} ↗</span></a><button class="case-preview" data-id="{id}">{"Quick preview" if en else "Korte indruk"} ↗</button></article>'
    source=slot(source,'projects',projects)
    archive=''
    for p in data['projects']:
        heading=f'<a href="{case_url(p["id"],lang)}">{esc(p["title"])}</a>' if p['id'] in ROUTES else esc(p['title'])
        archive+=f'<article class="record"><span class="date">{esc(p["start"] or "—")}</span><div><h3>{heading}</h3><p>{esc(' · '.join(v for v in [p["client"],p["category"]] if v))}</p><details><summary>{"Project context" if en else "Projectcontext"}</summary><p>{esc(p["description"])}</p><p>{esc(p["role"])}</p>{project_tags(p)}</details></div></article>'
    source=slot(source,'archive-list',archive)
    # Normal links supplement the short visual home; no extra long homepage copy.
    hub=f'<nav class="question-links" aria-label="{"Explore challenges" if en else "Verken vraagstukken"}"><span>{"Explore a question" if en else "Verken een vraag"}</span>'
    for nl,eng in PAIRS[3:7]:
        file=eng if en else nl; text={'engaging-employees-in-change.html':'Engaging people in change','collaboration-between-teams.html':'Collaboration between teams','experiential-learning.html':'Learning through experience','breaking-patterns.html':'Breaking familiar patterns','medewerkers-meekrijgen-in-verandering.html':'Mensen betrekken bij verandering','samenwerking-tussen-afdelingen.html':'Samenwerking tussen afdelingen','leren-door-ervaring.html':'Leren door ervaring','patronen-doorbreken.html':'Patronen doorbreken'}[file]
        hub+=f'<a href="{file}">{text} ↗</a>'
    hub+='</nav>'
    source=re.sub(r'<!--seo:question-links:start-->.*?<!--seo:question-links:end-->','',source,flags=re.S)
    source=source.replace('</main>','<!--seo:question-links:start-->'+hub+'<!--seo:question-links:end--></main>')
    source=source.replace('href="#spreken">Speaking','href="speaker.html">Speaking').replace('href="#spreken">Spreken','href="spreker.html">Spreken')
    source=source.replace('href="spreker.html">Ontdek mijn talks','href="spreker.html">Ontdek mijn talks')
    if en:source=source.replace('href="speaker.html">Ontdek mijn talks','href="speaker.html">Explore my talks')
    (ROOT/name).write_text(source)

for lang in ['nl','en']:
    en=lang=='en';name='media-en.html' if en else 'media.html';source=(ROOT/name).read_text();items=[]
    for m in DATA[lang]['media']:items.append(dict(id=m[0],year=m[1],title=m[2],platform=m[3],role=m[4],description=m[5],url=m[7]))
    for t in DATA[lang]['talks']:items.append(dict(id=t[0],year=t[1],title=t[2],platform=t[3],role=t[4],description=t[5],url=t[7]))
    items.sort(key=lambda x:order_key(x['id'],x['year']),reverse=True);output='';last=None
    for item in items:
        match=re.search(r'\b(?:19|20)\d{2}\b',str(item['year']));year=match[0] if match else ('Date unknown' if en else 'Datum nog onbekend')
        if year!=last:output+=f'<h2 class="timeline-year">{year}</h2>';last=year
        output+=f'<article class="record"><span class="date">{esc(date_label(item["id"],item["year"],lang))}</span><div><p class="eyebrow">{esc(item["role"])} · {esc(item["platform"])}</p><h3>{esc(item["title"])}</h3><p>{esc(item["description"])}</p></div>{external(item["url"],"View" if en else "Bekijken")}</article>'
    (ROOT/name).write_text(slot(source,'media-results',output))

# Keep the homepage focused; detailed ways to work together have their own page.
offering_content=json.loads((ROOT/'aanbod-content.json').read_text())
PAIRS.append(('samenwerken.html','working-together.html'))
for lang,body in offering_content.items():
    en=lang=='en';file='working-together.html' if en else 'samenwerken.html';other='samenwerken.html' if en else 'working-together.html'
    title='Working together | Chantal van Kempen' if en else 'Samenwerken | Chantal van Kempen'
    intro='A talk, a shared experience or creative leadership. Explore what fits your question.' if en else 'Een talk, een gezamenlijke ervaring of creatieve leiding. Ontdek wat bij jouw vraag past.'
    heading='What would you like to spark?' if en else 'Wat wil jij losmaken?'
    opening=f'<section class="section offering-intro"><p class="eyebrow">CHANTAL VAN KEMPEN</p><h1>{heading}</h1><p>{intro}</p><nav class="offering-links"><a href="{"speaker.html" if en else "spreker.html"}">{"For your event" if en else "Voor je evenement"} ↗</a><a href="#verdieping">{"Learning & development" if en else "Leren & ontwikkeling"} ↓</a><a href="#realisatie">{"Creative project leadership" if en else "Creatieve projectleiding"} ↓</a><a href="#voor-jezelf">{"For yourself" if en else "Voor jezelf"} ↓</a></nav></section>'
    page=shell(lang,title,intro,opening+body,other)
    page=re.sub(r'<a href="[^"]+" lang="nl">NL</a>',f'<a href="samenwerken.html" lang="nl">NL</a>',page)
    page=re.sub(r'<a href="[^"]+" lang="en">EN</a>',f'<a href="working-together.html" lang="en">EN</a>',page)
    (ROOT/file).write_text(page)

# Finalise canonical, language, share and identity metadata on intended public pages.
for nl,enfile in PAIRS:
    for lang,file in [('nl',nl),('en',enfile)]:
        p=ROOT/file;source=p.read_text();source=source.replace('#vraagstukken','#routes')
        # Keep the same four main routes and language switch on all public pages.
        en = lang == 'en'
        home = 'index-en.html' if en else 'index.html'
        navigation = f'<nav aria-label="{"Main navigation" if en else "Hoofdnavigatie"}"><a href="{"speaker.html" if en else "spreker.html"}">{"Speaking" if en else "Spreken"}</a><a href="{"working-together.html" if en else "samenwerken.html"}">{"Working together" if en else "Samenwerken"}</a><a href="{home}#werk">{"Work" if en else "Werk"}</a><a href="{"media-en.html" if en else "media.html"}">Media</a><a class="nav-contact" href="{home}#contact">{"Let’s connect" if en else "Laten we kennismaken"} ↗</a><span class="language-switch" aria-label="{"Choose language" if en else "Taal kiezen"}"><a href="{nl}" lang="nl"{" aria-current=\"true\"" if not en else ""}>NL</a><span>/</span><a href="{enfile}" lang="en"{" aria-current=\"true\"" if en else ""}>EN</a></span></nav>'
        source = re.sub(r'(<header>.*?)<nav\b.*?</nav>', lambda m: m[1]+navigation, source, count=1, flags=re.S)
        # A direct visitor-initiated WhatsApp conversation, available on every page.
        source=re.sub(r'<a class="whatsapp-chat"[^>]*>.*?</a>','',source,flags=re.S)
        chat_label='Chat on WhatsApp' if lang=='en' else 'Chat via WhatsApp'
        chat_icon='<svg class="whatsapp-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M21 11.5a9 9 0 0 1-13.4 7.9L3 21l1.6-4.6A9 9 0 1 1 21 11.5Z"/><path d="M8.2 7.5c-.8 1.1-.2 3.2 1.5 4.9s3.8 2.3 4.9 1.5l1-1-2.3-1.3-.8.8a7 7 0 0 1-2.6-2.6l.8-.8-1.3-2.3Z"/></svg>'
        chat_link=f'<a class="whatsapp-chat" href="https://wa.me/31619208308" target="_blank" rel="noopener noreferrer">{chat_icon}<span>{chat_label}</span> ↗</a>'
        source=source.replace('</footer>',chat_link+'</footer>')
        source=re.sub(r'<script src="public-project-copy.js[^"]*" defer></script>','',source)
        source=re.sub(r'(<script src="app.js[^"]*" defer></script>)',r'<script src="public-project-copy.js" defer></script>\1',source)
        source=re.sub(r'<script src="handdrawn-arrows.js[^"]*" defer></script>','',source)
        source=source.replace('</head>','<script src="handdrawn-arrows.js" defer></script></head>')
        source=re.sub(r'<script src="contact-email.js[^"]*" defer></script>','',source)
        source=source.replace('</head>','<script src="contact-email.js" defer></script></head>')
        source=re.sub(r'<link\b[^>]*rel="(?:canonical|alternate)"[^>]*>','',source)
        source=re.sub(r'<meta\b[^>]*(?:property="og:[^"]+"|name="twitter:[^"]+")[^>]*>','',source)
        source=re.sub(r'<script type="application/ld\+json" data-seo="identity">.*?</script>','',source,flags=re.S)
        title=re.search(r'<title>(.*?)</title>',source,re.S)[1]
        description=re.search(r'<meta name="description" content="([^"]*)"',source)[1]
        from html import unescape
        title,description=unescape(title),unescape(description)
        identity={'@context':'https://schema.org','@graph':[{'@type':'Person','@id':BASE+'/#person','name':'Chantal van Kempen','url':BASE+'/','jobTitle':['Creative project leader','Concept developer','Experience designer','Speaker'],'telephone':'+31619208308','email':'chantalke@gmail.com','sameAs':['https://www.linkedin.com/in/chantalvankempen/']}]}
        if file in ['index.html','index-en.html']:identity['@graph'].append({'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'Chantal van Kempen','inLanguage':['nl','en']})
        head=f'<link rel="canonical" href="{absolute(file)}"><link rel="alternate" hreflang="nl" href="{absolute(nl)}"><link rel="alternate" hreflang="en" href="{absolute(enfile)}"><link rel="alternate" hreflang="x-default" href="{absolute(nl)}">'
        for key,value in {'type':'website','title':title,'description':description,'url':absolute(file),'image':BASE+'/assets/chantal.jpg','image:alt':('Chantal van Kempen on stage' if en else 'Chantal van Kempen op het podium'),'locale':'en_GB' if lang=='en' else 'nl_NL','site_name':'Chantal van Kempen'}.items():head+=f'<meta property="og:{key}" content="{esc(value,quote=True)}">'
        head+='<script type="application/ld+json" data-seo="identity">'+json.dumps(identity,ensure_ascii=False).replace('</',r'<\/')+'</script>'
        if 'seo-pages.css' not in source:head+='<link rel="stylesheet" href="seo-pages.css?v=seo-1">'
        source=source.replace('</head>',head+'</head>')
        # English alternative text belongs in source HTML, not just the JS translation layer.
        if lang=='en':source=source.replace('alt="Chantal op het podium, met een mand vol gekleurde ballen"','alt="Chantal on stage, holding a basket of colourful balls"')
        # File-content versions prevent the local preview retaining older scripts/styles.
        import hashlib
        def version_asset(match):
            file=match[2];asset=ROOT/file
            if not asset.is_file():return match[0]
            version=hashlib.sha256(asset.read_bytes()).hexdigest()[:10]
            return match[1]+'"'+file+'?v='+version+'"'
        source=re.sub(r'((?:src|href)=)"([^"?]+\.(?:js|css))(?:\?[^\"]*)?"',version_asset,source)
        p.write_text(source)

for name in ['index-magazine.html','index-magazine-en.html']:
    p=ROOT/name
    if not p.exists():continue
    s=p.read_text();s=re.sub(r'<meta name="robots"[^>]*>','',s);p.write_text(s.replace('</head>','<meta name="robots" content="noindex,follow"></head>'))
ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
ns='{http://www.sitemaps.org/schemas/sitemap/0.9}';sitemap=ET.Element(ns+'urlset')
for pair in PAIRS:
    for file in pair:ET.SubElement(ET.SubElement(sitemap,ns+'url'),ns+'loc').text=absolute(file)
ET.ElementTree(sitemap).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'/sitemap.xml\n')
(ROOT/'_redirects').write_text('# Supported by Cloudflare Pages / Netlify; configure equivalent rules on other hosts.\n/index.html / 301\n')
(ROOT/'404.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | Chantal van Kempen</title><link rel="stylesheet" href="{BASE}/style.css"></head><body><main class="section article"><p class="eyebrow">404 / A DIFFERENT DOOR</p><h1>This page isn’t here.</h1><p><a href="{BASE}/">Naar de Nederlandse website ↗</a></p><p><a href="{BASE}/index-en.html">Explore the English website ↗</a></p></main></body></html>')
print(f'Prepared {len(PAIRS)*2} public pages for {BASE}; no deployment performed.')
