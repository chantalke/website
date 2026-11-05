"""Rebuild the English data and entry pages using the standard Python library."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
data = json.loads((root / 'data.js').read_text().removeprefix('const DATA = ').strip().removesuffix(';'))
descriptions = {
75: "Volunteering for the European Positive Psychology Conference.",
76: "Chair role for the Positive Psychology in Practice conference.",
74: "Bringing direction, clarity and coordination to an ERP transition affecting multiple departments and core processes. Analysed the existing ERP environment and processes as a whole, making bottlenecks, inefficiencies and information flows visible.",
1:'Following a pilot with one artwork, I built the full delivery structure for Future Village: a cultural and social programme where young people create large art installations with professional artists.',
2:'A game about fixed and collaborative scheduling. Employees take on different roles to experience the consequences of decisions and competing interests.',
3:'An evening for healthcare professionals who wanted more than a speaker. Three physical experience rooms exploring Positive Health made the influence of waiting, attention and small gestures tangible.',
4:'A week-long blended game designed to reach healthcare trainees in a different way and sustain their involvement. Together with my business partner, I created the story, assignments, puzzles and competition format. Trainees completed assignments independently throughout the week.',
5:'Designed and facilitated a two-day serious game about diversity and inclusion for the Ministry of Justice and Security through Startup in Residence. Participants reflected on their own behaviour and assumptions.',
6:'A personal development journey inspired by the Divine Comedy, combining storytelling, reflection and physical and digital experiences.',
7:'A LEGO game supporting Office 365 adoption. Participants need to organise and share information effectively to complete a building challenge.',
8:'Making processes visible by playing them together. A LEGO simulation in which employees explore bottlenecks in procurement as a starting point for process improvement.',
10:'An exhibition-floor experience with audio-guided missions, promoting an innovation network in the rail sector.',
11:'In-depth interviews with employees, from concrete workers to directors, exploring workplace happiness, engagement and needs.',
12:'Bringing focus, structure and effectiveness to the management team of a rapidly growing organisation. Designed and guided a change programme, strengthened collaboration and ownership, and structured project management and decision-making. Coached leaders on prioritisation, follow-through and completion, creating space for team development and strategic thinking alongside operational demands.',
13:'Facilitated assessments as a starting point for self-awareness, team development and collaboration. The development-focused approach centres on active participation and reflection: exploring strengths, motivations and development opportunities as a basis for the next step.',
14:'Co-developed BE, BALANCE and BOOST programmes for self-awareness, balance and professional growth.',
15:'An internal community helping employees collaborate, take ownership and launch their own initiatives.',
16:'Sessions on self-organisation and skills-based collaboration, connecting people’s talents with work.',
17:'A one-day internal hackathon at MEE Plus. Coached teams worked on projects with support from finance, legal, communications and IT experts. Management could make same-day decisions on resources and implementation.',
18:'Managed a community and organised meetups and co-creation sessions in Utrecht and Amsterdam, including Tech Tuesday and Biohacking.',
19:'Co-hosted three Maven Meetups: People Skills, Hufters & Helden, and Mag ik jullie aandacht? at NEMO Amsterdam, with Wouter Eggink on disruptive design.',
20:'Secret surprise evenings in Utrecht and Amsterdam. Guests discovered their destination and activities only shortly before the experience unfolded.',
21:'A month-long game of tag for adults, using social media as part of the game. Featured on Studio MAX Live.',
22:'Helped entrepreneurs take bolder steps through in-depth interviews, inspiration sessions, workshops and action-focused experiences.',
23:'Concepts, challenges and experiences that bring curiosity, energy and action into everyday life.',
24:'An independent experiment exploring curiosity, breaking routines and trying new experiences.',
25:'A playful challenge to break habits and invite more spontaneous experiences.',
26:'A prepaid credits model gave organisations quick access to a range of independent experts, allowing them to bring in the expertise they needed to accelerate innovation.',
27:'Creative professionals work on challenges for charities during an eight-hour event.',
28:'A singles event centred on connection: getting to know one another in a different way, beyond the usual introductions.',
29:'A facilitated session on creativity and the art of living, inspired by The Artist’s Way.',
30:'Collaborating while the rules change. This active session for energy-sector managers centred on Switchball: a game in which rules, goals and even teams can shift. A playful way to explore adaptability and collaboration.',
31:'Gathered perspectives on healthcare technology from clients, employees and parents, translating them into a multi-year plan.',
32:'A project to improve effectiveness and efficiency in long-term elderly care.',
33:'An interactive game helping government departments get to know one another.',
34:'An experience encouraging young rail-sector professionals to explore innovation.',
35:'An interactive experience about sustainable travel within an energy company.',
36:'Established and supported a community for greater self-organisation in healthcare.',
37:'Connected work with people’s talents through a platform supporting self-organisation.',
40:'Supported working groups in resolving bottlenecks and making practical progress.',
41:'Developed activities for more effective, interactive meetings.',
42:'Structured Lean improvement challenges and supported aftersales improvement processes.',
43:'Designed and organised sustainable activities and environmentally focused company outings.',
44:'Designed and organised a sustainable company outing for a pharmaceutical client.',
45:'An event and advisory project focused on increasing residents’ zest for life.',
46:'Organised outdoor events for customers, suppliers and employees.',
47:'Organised professional networking teams at exhibitions and events to stimulate new connections and knowledge sharing.',
48:'Organised professional development for youth facilitators.',
49:'School workshops on talent development and career choices, aimed at reducing early school leaving.',
50:'Supported sports activities bringing together mainstream and special education.',
51:'Organised creative sessions and co-creation to encourage ideas and collaboration.',
52:'Connected visitors and facilitated interaction at a knowledge-sharing event.',
53:'Moderated an event about digital recruitment.',
54:'Encouraged connection and interaction between event participants.',
55:'Guided visitors through an escape room about privacy and data use.',
56:'Hosted immersive games and escape experiences.',
57:'Guided visitors through an escape room in Amsterdam.',
58:'Delivered social media strategy training for coaches and entrepreneurs.',
59:'A workshop about overcoming fear and taking action.',
60:'A practical workshop on networking skills.',
61:'A job application workshop with a playful approach.',
62:'Worked with behavioural and communication profiles to support teams.',
63:'Individual coaching focused on social skills.',
64:'Supported concept development for a new market proposition.',
65:'Facilitated sessions and prepared an advisory report on sustainable employability.',
66:'A private family game exploring the history of Balk.',
67:'Co-founded and chaired the brewery for four years and three months.',
68:'Designed a game to help colleagues get to know each other. The planned delivery was cancelled because of COVID-19.',
69:'Developed a community game as part of self-organisation projects.',
70:'Talent development training for young people.',
71:'Advised on the development of a market concept.',
72:'Involved in an orienteering experience in the Ardennes. The specific role and dates have not been confirmed.',
73:'An interactive game in which participants join either the fictional innovative company Look Blue or the struggling Droom en Vreesman, exploring how people and organisations can keep developing and innovating. Played at Permanent Beta Day in 2018 and playtested with twenty Saxion students.'}
terms = {
'Jaar te bevestigen':'Year to be confirmed','Jaar onbekend':'Year unknown','Datum niet opgegeven':'Date not specified','Voor of tijdens COVID-19; datum onbekend':'Before or during COVID-19; date unknown','E2i-periode; datum onbekend':'During the Lighthouse e2i period; date unknown','actief rond 2019':'active around 2019','Jaar onbekend':'Year unknown','jaarlijst':'annual overview','waarschijnlijk':'approximate','periode onbekend':'period unknown','Maatschappelijke innovatie':'Social innovation','Immersive experiences':'Immersive experiences','Transformational experiences':'Transformational experiences','Onderzoek & organisatie':'Research & organisations','Organisatieverandering':'Organisational change','Teamontwikkeling':'Team development','Passieprojecten':'Passion projects','Eigen initiatieven':'Independent initiatives','Innovatie & ondernemerschap':'Innovation & entrepreneurship',
'Projectleider':'Project lead','Ontwerp en facilitatie':'Design & facilitation','Experience designer en facilitator':'Experience designer & facilitator','Game / blended experience designer':'Game & blended experience designer','Game designer en facilitator':'Game designer & facilitator','Onderzoeker / consultant':'Researcher & consultant','Organisatieconsultant':'Organisational consultant','Assessor en facilitator':'Assessor & facilitator','Concept- en programmaontwikkeling':'Concept & programme development','Consultant / implementatiecoach':'Consultant & implementation coach','Facilitator / projectondersteuning':'Facilitator & project support','Organisator':'Organiser','Game / concept maker':'Game & concept designer','Conceptmaker':'Concept designer','(Mede-)organisator':'(Co-)organiser','Concept / organisator':'Concept designer & organiser','Workshopfacilitator':'Workshop facilitator','Strategisch adviseur':'Strategic adviser','Procesverbeteraar':'Process improvement consultant','Hackathonfacilitator':'Hackathon facilitator','Eventorganisator':'Event organiser','Eventorganisator / adviseur':'Event organiser & adviser','Eventmanager':'Event manager','Begeleider':'Facilitator','Facilitator / organisator':'Facilitator & organiser','Host / verbinder':'Host & connector','Trainer / assessor':'Trainer & assessor','Conceptontwikkelaar':'Concept developer','Facilitator / adviseur':'Facilitator & adviser','Game-ontwerp':'Game design','Medeoprichter en voorzitter':'Co-founder & chair','Ontwikkeling game':'Game development','Rol te checken':'Role to be confirmed','Workshopontwerp / facilitatie – rol nader te specificeren':'Workshop design & facilitation; exact role to be confirmed','Jaar te bevestigen':'Year to be confirmed',
'Eigen initiatief':'Independent initiative','Eigen onderneming':'Independent venture','Eigen evenement':'Independent event','Maatschappelijk evenement':'Social impact event','Diverse teams':'Various teams','Diverse opdrachtgevers':'Various clients','Individuele cliënten':'Individual clients','Opdrachtgever':'Client','Privéproject voor familie':'Private family project','Onbekend':'Unknown','Inclusief sportproject':'Inclusive sports project','Zorginstelling':'Healthcare organisation','Ouderenzorgorganisatie':'Elderly care organisation','Overheidsinstantie':'Government organisation','Energiebedrijf':'Energy company','Opdrachtgever in energiesector':'Energy-sector client','Jongerennetwerk railsector':'Young professionals’ rail network','Farmaceutische opdrachtgever':'Pharmaceutical client','Aftersalesafdeling':'Aftersales department','Adviestraject':'Advisory project','Escape room in Amsterdam':'Escape room in Amsterdam','Diverse opleidings- en netwerkevents':'Various learning and networking events','Coachingorganisatie / opdrachtgevers':'Coaching organisations & clients','Rol nader te specificeren':'Role to be specified',
'jan':'Jan','feb':'Feb','mrt':'Mar','apr':'Apr','mei':'May','jun':'Jun','jul':'Jul','aug':'Aug','sep':'Sep','okt':'Oct','nov':'Nov','dec':'Dec',
'Podcast':'Podcast','Persoonlijk interview':'Personal interview','Video / interview':'Video interview','Radio-interview':'Radio interview','Televisie':'Television','Interview / artikel':'Interview / article','Pers':'Press','Video':'Video','TV / project':'TV / project','Projectpers':'Project coverage','Fotografie':'Photography','Evenementverslag':'Event report','Vakpublicatie':'Industry publication','Partnerartikel':'Partner article','Aftersmovie':'Aftermovie','Projectinterview':'Project interview','Eigen artikel':'Article','Programma':'Programme','Conferentie':'Conference','Eigen post':'Post','Eigen publicatie':'Author','Persoonlijke bijdrage geciteerd':'Personal contribution quoted','Vermelding spreker':'Speaker listing','Bijdrage aan programma':'Programme contribution','Vermelding als chair/opening':'Listed as chair / opening speaker','Projectportfolio':'Project portfolio',
'Gastspreker / deelnemer programma':'Guest speaker / programme participant','Deelnemer / bijdragen aan gesprek':'Participant / contributor to the discussion','Medeorganisator':'Co-organiser','Spreker':'Speaker','Workshopgever':'Workshop facilitator','Workshopgever met Ondernemen met Ballen':'Workshop facilitator with Ondernemen met Ballen','Talk / presentator':'Speaker / presenter','Co-host (met Kim)':'Co-host (with Kim)','Co-founder':'Co-founder','Conferentie Utrecht':'Conference in Utrecht','Evenement':'Event','Opleiding':'Professional development','HBO':'Bachelor-level vocational education','Vrijetijdsmanagement':'Leisure Management','Psychologie':'Psychology','Impactmeting / maatschappelijke impact':'Impact measurement / social impact','Experience design / embodied learning':'Experience design / embodied learning'}
def tr(s):
    if s in terms:
        return terms[s]
    for a,b in sorted(terms.items(), key=lambda x: -len(x[0])):
        # Replace whole phrases, not parts of proper names.
        if len(a)>4:
            import re
            s=re.sub(r'(?<!\w)'+re.escape(a)+r'(?!\w)',b,s)
    for a,b in {'jan':'Jan','feb':'Feb','mrt':'Mar','apr':'Apr','mei':'May','jun':'Jun','jul':'Jul','aug':'Aug','sep':'Sep','okt':'Oct','nov':'Nov','dec':'Dec'}.items():
        import re
        s=re.sub(r'\b'+a+r'\b',b,s)
    return s

tag_translations=json.loads((root/'tag-translations.json').read_text())
for p in data['projects']:
    for photo in p.get('images',[]):photo['alt']=photo.pop('alt_en',photo['alt'])
    p['tags']=[tag_translations[t] for t in p.get('tags',[])]
    if p.get('primary_topic'):p['primary_topic']=tag_translations[p['primary_topic']]
    p['description']=descriptions[int(p['id'][1:])]
    for key in ['year','role','category','client']:
        p[key]=tr(p[key])
    p.pop('selection',None)

english_titles={
75: "European Positive Psychology Conference (ECPP)",
76: "Positive Psychology in Practice — conference chair",
74: "ERP transition — making processes visible",
1:'Future Village',2:'Plan je Rot — collaborative scheduling game',3:'Positive Health Experience — three rooms',4:'The Nightingale Society — healthcare innovation game',5:'Diversity & Inclusion — a two-day serious game',6:'Changetrek — Walk Your Own Path',7:'Office 365 LEGO game',8:'Order-to-Pay LEGO game',10:'RailTech — young innovators exhibition game',11:'Binden & Boeien — workplace happiness interviews',12:'Alfen — focus, structure and collaboration',13:'Team development & assessments',14:'Be in Balance to Boost',15:'Pluryn employee community',16:'Part-up — implementing self-organisation',17:'MEE Plus — Doe Mee Dag hackathon',18:'Permanent Beta — community & meetups',19:'Maven Meetups — people skills',20:'Wundernacht — creative events & surprise evenings',21:'TIKKIE — a month-long game of tag',22:'Ondernemen met Ballen',23:'Do You Feel Alive',24:'Do You Feel Alive Experiment — Pinterest',25:'Anti-Routine Challenge',26:'Innovatiekoers',27:'8 Uur Overwerken voor het Goede Doel — creative charity event',28:'Ik Jij Wijn — a singles event',29:'The Artist’s Way — creative session',30:'Switchball',31:'Healthcare technology — vision & multi-year plan',32:'Improving efficiency in long-term elderly care',33:'Getting-to-know-you game for government departments',34:'Jonge Veranderaars — festival experience',35:'Adventure or an ordinary working day — sustainable travel',36:'Self-organising healthcare community',37:'Skills-based self-organisation platform',40:'Working-group facilitation & team away days',41:'Making meetings more interactive',42:'Lean aftersales improvement',43:'Terra Futura / Terra Green Tour',44:'Green Tour — Stryker',45:'Levenslust for Life',46:'Bever Zwerfsport — improving the partner day',47:'PB Connect — networking teams',48:'Jimmies — train the trainer',49:'Young Ambition — talent & career workshops',50:'Buitengewone Sportdagen — inclusive sports days',51:'Intelligence Lab Ceasar — creative sessions',52:'Zorg voor Kennis — event hosting',53:'Digitaal Werven — event moderation',54:'Videologic — hostmanship',55:'Google Backstage — privacy escape room',56:'Sherlocked / Better Plays — experience hosting',57:'The Architect — escape room Amsterdam',58:'Social media strategy training',59:'Feel the Fear and Do It Anyway — online course',60:'Networking skills workshop',61:'Job applications and other challenges',62:'Mapstell and DISC profiles — training',63:'Personal social-skills coaching',64:'Developing a new market concept',65:'Think tank — sustainable employability',66:'Balk — family history game',67:'Brouwerij Nooitgedacht',68:'Getting-to-know-you game — DG Migration',69:'Part-up — community game',70:'Jonge Krijgers — talent training',71:'Mevrouw Markt — concept development',72:'Ardennes orienteering experience',73:'Droom en Vreesman vs. Look Blue'}
for p in data['projects']:
    p['title']=english_titles[int(p['id'][1:])]
    if p['id']=='P020':p['description']='Surprise events in Utrecht and Amsterdam where participants did not know the programme in advance. A creative event concept with unexpected encounters and memorable experiences.'
    if p['id']=='P075':p.update(role='Volunteer',category='Volunteering',year='Jun 2014–Jun 2018')
    if p['id']=='P076':p.update(role='Chair (volunteer)',category='Volunteering',year='Jun 2018–Jun 2019')
    if p['id']=='P071':p['description']='Advice and guidance on developing a new market concept for Mevrouw Markt in 2015.'
    if p['id']=='P061':p['client']='Zin in Werk / Terug naar Werk (Michiel; name to be confirmed)'
    if p['id']=='P060':p['description']='Practical networking training for DeBroekriem, also listed as Spreek je netwerk aan. Participants practise making active use of their network.'
    if p['id']=='P065':p['description']='Contributed to a think tank on sustainable employability for ZSW, through Factor Vijf, in 2015.'
    if p['id']=='P050':p.update(role='Volunteer facilitator',description='Volunteering as a facilitator of sports activities bringing together children from mainstream and special education.')
    if p['id']=='P027':p.update(role='Volunteer organiser',description='A hackathon in which creatives work together for eight hours on a challenge for a charity. Involved as a volunteer organiser.')
    if p['id']=='P067':p['role']='Co-founder and chair (volunteer)'
    if p['id']=='P044':p['description']='A sustainable company outing for Stryker, delivered through Terra Futura in 2016 under the name Green Tour.'
    if p['id']=='P046':p.update(role='Intern',description='An internship at Bever Zwerfsport focused on improving the partner day.')
    if p['id']=='P035':p['description']='A sustainable travel experience for Alliander, titled Adventure or an ordinary working day, in collaboration with Experience Experts.'
    if p['id']=='P057':p['description']='Hosting visitors at The Architect, the Sherlocked escape room in Amsterdam.'
    if p['id']=='P015':p['description']='An internal community at Pluryn encouraging collaboration, self-organisation and employee initiative. Part of my work on self-organising healthcare communities at Pluryn and Part-up, spanning advice and implementation support.'
    if p['id']=='P034':p['description']='An experience exploring the courage to innovate for young rail-sector professionals, at the Jonge Veranderaars festival in 2021.'
    if p['id']=='P032':p.update(year='2020–2021 (exact months unknown)',client='Accezz / elderly care organisation')
    if p['id']=='P068':p['description']='Developed a getting-to-know-you game for colleagues across departments within DG Migration in 2020. The game was not delivered because of COVID-19.'
    if p['id']=='P074':p.update(role='Process consultant — ERP transition support',year='Dec 2024–Jul 2025')
    if p['id']=='P020':p['category']='Surprise experiences'
    if p['id']=='P031':p.update(title='A vision for human-centred technology',category='Social innovation')
    if p['id']=='P016':p.update(title='Part-up — skills-based hiring & self-organisation',category='Social innovation')
    p['client']=p['client'].replace('koppeling checken','connection to be confirmed').replace('preciese context te bevestigen','exact context to be confirmed').replace('ander samenwerkingsverband','other partnership').replace('gemeente Utrecht','Municipality of Utrecht').replace('Gemeente Utrecht','Municipality of Utrecht')

talks=[
'The scheduling-game case and perspective-taking',
'How experience design can shift our perception of time and space',
'Finding the real challenge through learning experience design',
'Positive psychology, wellbeing and personal development',
'Play and the cultural sector',
'Courage and fear in entrepreneurship; seventeen interviews',
'Work, entrepreneurship and opportunity',
'Innovation through the Trojan horse metaphor',
'Human communication and social skills',
'Social and antisocial behaviour',
'Attention and disruptive design, with guest Wouter Eggink',
'Technology and experimentation',
'Biohacking and emerging technologies',
'Digital recruitment',
'Connecting visitors and sharing knowledge',
'Active networking and professional connection',
'An interactive workshop; topic and date to be confirmed',
'PechaKucha presentation about 8 Uur Overwerken voor het Goede Doel',
'Training on meeting people and making new connections',
'Training on making active use of your network',
'A workshop on dealing with failure']
talk_descriptions={f'S{i+1:03d}':description for i,description in enumerate(talks)}
network_host_description='Making events more valuable by facilitating contact between attendees and connecting people.'
talk_descriptions.update({'S006':'A talk on Feel the Fear and Do It Anyway, through Ondernemen met Ballen.','S025':'An interactive talk about play at work. Playing with time, space and perception, and exploring how experience design can address organisational challenges.','S016':'Facilitating introductions and professional connections at ING events.','S022':network_host_description,'S023':'Encouraging connection and interaction between event participants.','S024':network_host_description})
for row in data['talks']:
    row[5]=talk_descriptions[row[0]]
    row[3]=tr(row[3]);row[4]=tr(row[4])
    if row[0] in ['S016','S022']:row[4]='Host / networking facilitator'
    if row[0]=='S023':row[4]='Host / connection facilitator'
    if row[0] in ['S022','S024']:row[4]='Networking host'
network_project=next(p for p in data['projects'] if p['id']=='P047')
network_project.update(title='Networking team — Social Impact Day & Dag van de Ondernemer',role='Networking host',description=network_host_description)
media_descriptions=[
'Personal interview','Personal interview','A conversation about gamification','In the studio discussing Wundernacht and surprise evenings','The TIKKIE project featured on television','Interviewed as project lead','Coverage of Future Village','Project video; personal appearance not confirmed','Personal video interview','Project coverage; personal appearance not confirmed','Articles and a campaign about Future Village','Project photography','Listed as a speaker representing Kultlab','Personal contribution quoted','Personal contribution quoted','Personal contribution quoted','Named and pictured as the E2i contact','Footage of the experience designed by Chantal','Interview with a co-organiser about Wundernacht, rather than a personal interview','The venture featured; not a personal interview','Author','Author','Author','Author','Author','Author','Author','Author','Author','Author','Author','Listed as chair / opening speaker','Speaker listing','Speaker listing','Programme contribution','Projects and departure discussed']
media_description_by_id={f'M{i+1:03d}':description for i,description in enumerate(media_descriptions)}
media_description_by_id['M037']='On HR development, employee engagement, 360-degree feedback and continuous improvement.'
for row in data['media']:
    row[5]=media_description_by_id[row[0]];row[4]=tr(row[4]);row[3]=tr(row[3]);row[1]=tr(row[1])
work_descriptions={
'W021':'Work on effectiveness and efficiency in long-term elderly care',
'W022':'Volunteering for the European Positive Psychology Conference.',
'W023':'Facilitating sports activities bringing together children from mainstream and special education.',
'W024':'A hackathon in which creatives spend eight hours tackling a challenge for a charity.',
'W025':'Chair role for the Positive Psychology in Practice conference.',
'W001':'Project leadership for participatory art, youth programmes and events',
'W002':'Serious games, organisational change, assessments and team development',
'W003':'Experiences for healthcare professionals exploring innovation and Positive Health',
'W004':'Workshops and experiences for entrepreneurial courage',
'W005':'Experience design, innovation, project management, training and social entrepreneurship',
'W006':'Internal community building and employee ownership',
'W007':'Meetups, community relationships and co-creation',
'W008':'Self-organisation, implementation and skills-based collaboration',
'W009':'Hosting visitors in immersive experiences',
'W017':'Internship focused on improving the partner day',
'W018':'Networking teams, including ING and Social Impact Day',
'W019':'Workshops on talent development and career choices for school students',
'W020':'Co-founder and chair; involved in the brewery for four years and three months'}
for row in data['work']:
    row[7]=work_descriptions[row[0]];row[1]=tr(row[1]);row[5]=tr(row[5]).replace('locatiemanager','venue manager')
    if row[0] in ['W020','W022','W023','W024','W025']:row[6]='Volunteering'
    if row[0]=='W022':row[5]='Volunteer'
    if row[0]=='W024':row[5]='Organiser'
    if row[0]=='W025':row[5]='Chair'
    if row[0]=='W017':row[5]='Intern';row[6]='Internship'
    if row[0]=='W021':row[1]='2020–2021';row[5]='Organisational development in healthcare';row[6]='Employer';row[7]='Supported day-to-day work organisation at De Zijlen and Careyn. Analysed work processes and use of time, translating findings into practical changes to work plans.'
    if row[0]=='W005':row[1]='2012–present'
for row in data['education']:
    row[3]=tr(row[3]);row[4]=tr(row[4]);row[5]=tr(row[5])

next(row for row in data['media'] if row[0]=='M037')[2]='From HR 2.0 to HR 3.0'
next(row for row in data['media'] if row[0]=='M003')[5]='A conversation about gamification. Livestreamed on 5 November 2024.'
next(row for row in data['talks'] if row[0]=='S001')[5]='The scheduling-game case and perspective-taking. Livestreamed on 5 November 2024.'
next(row for row in data['talks'] if row[0]=='S025')[2]='Play at work'
next(row for row in data['talks'] if row[0]=='S005')[4]='Expert panel member'
demo_day=next(row for row in data['talks'] if row[0]=='S008')
demo_day[3]='Paard van Troje, The Hague'
demo_day[5]='Presentation about Ondernemen met Ballen at the Startup in Residence Demo Day.'
next(row for row in data['media'] if row[0]=='M035')[5]='Expert panel member'
next(row for row in data['media'] if row[0]=='M032')[5]='Listed as conference chairwoman'
next(p for p in data['projects'] if p['id']=='P001').update(year='2025–present',role='Project lead – development and delivery')
next(p for p in data['projects'] if p['id']=='P003')['role']='Concept, delivery and facilitation – together with my business partner'
next(p for p in data['projects'] if p['id']=='P004')['role']='Story, assignments, puzzles and competition format – together with my business partner'
next(p for p in data['projects'] if p['id']=='P005').update(description='A two-day experience for the Ministry of Justice and Security exploring inclusion in everyday behaviour. Afterwards, ten ambassadors wanted to take action within their departments.',role='Interviews, experience design and facilitation – Ondernemen met Ballen')
next(p for p in data['projects'] if p['id']=='P004')['description']='A week-long blended game for healthcare trainees, with a story, independent assignments, puzzles and a competition format. Co-developed with my business partner.'
next(p for p in data['projects'] if p['id']=='P006').update(description='A development journey exploring life decisions and personal patterns at work. In-person sessions, weekly letters and online group reflection formed a journey inspired by Dante.',role='Story, assignments, design, coaching and facilitation – with two collaborators')
next(p for p in data['projects'] if p['id']=='P020').update(description='The Utrecht branch of Wundernacht, an existing Amsterdam concept. A letter beforehand and messages along the way guided participants through an evening of surprises.',role='Organiser of the Utrecht branch')
next(p for p in data['projects'] if p['id']=='P031').update(description='How can technology support care while keeping it human? Across three evenings, we brought together the wishes and concerns of clients, staff and parents as the basis for a vision and multi-year plan.',role='Vision development and session facilitation')
next(p for p in data['projects'] if p['id']=='P002').update(description='A physical game exploring resistance to new scheduling methods. Using personas and a large board on the floor, employees discovered how each method affected their preferred shifts.',role='Game design and facilitation')
next(p for p in data['projects'] if p['id']=='P008').update(description='A LEGO simulation to kick off a procurement change programme. Different roles, partial information and recognisable bottlenecks helped employees discover the parallels with their own organisation.',role='Game design and facilitation')
next(p for p in data['projects'] if p['id']=='P012').update(description='A change programme for the management team of a rapidly growing organisation. Strengthened collaboration and ownership, structured decision-making and coached leaders, creating more space for strategy alongside day-to-day pressures.',role='Change programme and management team development')
next(p for p in data['projects'] if p['id']=='P016').update(title='Part-up – talent-based working & self-organisation',description='Advising organisations on self-organisation, facilitating sessions and helping employees work with Part-up. As an implementation coach, I supported use of the platform and the community around it.',role='Consultant and implementation coach')
next(p for p in data['projects'] if p['id']=='P032').update(title='Accezz – organisational development in healthcare',client='De Zijlen / Careyn, through Accezz',role='Organisational development',description='Supported day-to-day work organisation at De Zijlen and Careyn. Analysed work processes and use of time, translating findings into practical changes to work plans.')
(root/'data.en.js').write_text('const DATA = '+json.dumps(data,ensure_ascii=False)+';\n')
for name in ['index','media']:
    src=(root/f'{name}.html').read_text()
    src=src.replace('lang="nl"','lang="en"',1).replace('src="data.js','src="data.en.js')
    # Keep language-specific navigation stable, including the brand and media links.
    src=src.replace('media.html','media-en.html').replace('index.html','index-en.html').replace('spreker.html','speaker.html')
    src=src.replace('samenwerken.html','working-together.html')
    src=src.replace('href="playcards/"','href="playcards/en.html"')
    import re
    src=re.sub(r'href="(project-[^"?]+?)(?<!-en)\.html"',r'href="\1-en.html"',src)
    src=src.replace('alt="Deelnemers in een fysieke zorgexperience"','alt="Participants in a physical healthcare experience"')
    src=src.replace('https://wa.me/31619208308?text=Hoi%20Chantal%2C%20ik%20heb%20interesse%20in%20de%20ervaringsdag%20voor%20mezelf.','https://wa.me/31619208308?text=Hi%20Chantal%2C%20I%20am%20interested%20in%20the%20experience%20day.')
    src=src.replace('</head>','<script src="i18n-en.js" defer></script></head>')
    src=src.replace('href="index-en.html" lang="nl"','href="index.html" lang="nl"').replace('href="media-en.html" lang="nl"','href="media.html" lang="nl"')
    src=src.replace('lang="nl" aria-current="true"','lang="nl"').replace(f'href="{name}-en.html" lang="en"',f'href="{name}-en.html" lang="en" aria-current="true"')
    for nl,en in {'medewerkers-meekrijgen-in-verandering':'engaging-employees-in-change','samenwerking-tussen-afdelingen':'collaboration-between-teams','leren-door-ervaring':'experiential-learning','patronen-doorbreken':'breaking-patterns'}.items():
        src=src.replace(nl+'.html',en+'.html')
    # Pre-render translated text so the page is readable and indexable without JS.
    import re, html
    phrase_file=root/'translations.json'
    if phrase_file.exists():
        phrases=json.loads(phrase_file.read_text())
        def translate_text(m):
            text=html.unescape(m.group(1)); translated=phrases.get(text.strip())
            return '>'+html.escape(text.replace(text.strip(),translated),quote=False)+'<' if translated else m.group(0)
        src=re.sub(r'>([^<>]+)<',translate_text,src)
    src=src.replace('Chantal van Kempen — Concept, experience design & realisatie','Chantal van Kempen — Creative concepts, experience design & delivery').replace('Creatieve concepten, serious games, immersieve ervaringen en projectleiding. Chantal van Kempen brengt ideeën van eerste vraag tot realisatie.','Creative concepts, serious games, immersive experiences and project leadership. Chantal van Kempen takes ideas from the first question to delivery.')
    src=src.replace('<h1>','<h1 lang="en">')
    src=src.replace('Chantal van Kempen — Experience designer','Chantal van Kempen — Experiential learning & organisational change')
    src=src.replace('Chantal van Kempen — Spreker over verwondering & verbinding','Chantal van Kempen — Speaker on wonder & human connection')
    src=src.replace('Chantal van Kempen — spreker en experience designer. Talks over verwondering en verbinding, en ervaringen rond persoonlijke ontwikkeling, filosofie en mogelijke toekomsten.','Chantal van Kempen — speaker and experience designer. Talks on wonder and human connection, and experiences exploring personal development, philosophy and possible futures.')
    src=src.replace('subject=Uitnodiging%20als%20spreker','subject=Speaking%20invitation').replace('subject=Meedenken%20over%20ontwikkelingservaringen','subject=Exploring%20development%20experiences')
    src=src.replace('Chantal van Kempen — experience designer. Serious games, immersieve ervaringen en creatieve ontmoetingen die mensen in beweging brengen.','Experiential learning, serious games and facilitated experiences for collaboration, organisational change and personal development. Chantal van Kempen.')
    src=src.replace('Podcasts, interviews, talks en hosting van experience designer Chantal van Kempen.','Podcasts, interviews, talks and hosting with experience designer Chantal van Kempen.')
    (root/f'{name}-en.html').write_text(src)
