"""Check links, reciprocal language/canonical metadata and crawlable key content."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,xml.etree.ElementTree as ET

root=Path(__file__).resolve().parent
from site_config import SITE_URL as base, page_name
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.links=[];self.assets=[];self.canonical=[];self.alternates={};self.h1=0;self.lang=None;self.robots='';self.title=False;self.description=False;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        if tag=='html':self.lang=a.get('lang')
        if tag=='a':self.links.append(a.get('href',''))
        if tag in ['script','img'] and a.get('src'):self.assets.append(a['src'])
        if tag=='link' and a.get('rel')=='stylesheet':self.assets.append(a['href'])
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
        if tag=='link' and a.get('hreflang'):self.alternates[a['hreflang']]=a['href']
        if tag=='h1':self.h1+=1
        if tag=='title':self.title=True
        if tag=='meta' and a.get('name')=='description':self.description=bool(a.get('content'))
        if tag=='meta' and a.get('name')=='robots':self.robots=a.get('content','')

texts={p.name:p.read_text() for p in root.glob('*.html')}
pages={name:Page(text) for name,text in texts.items()};errors=[]
for name,page in pages.items():
    for link in page.links+page.assets:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=unquote(u.path) or name
        if not (root/target).is_file():errors.append(f'{name}: missing local target {link}')
        elif u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append(f'{name}: missing anchor {link}')
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[n.text for n in ET.parse(root/'sitemap.xml').findall('s:url/s:loc',ns)]
assert len(urls)==len(set(urls)), 'Duplicate sitemap URL'
for url in urls:
    name=page_name(url);page=pages[name]
    if page.canonical!=[url]:errors.append(f'{name}: canonical mismatch')
    if page.h1!=1 or not page.title or not page.description:errors.append(f'{name}: heading/title/description missing or duplicate')
    if 'noindex' in page.robots:errors.append(f'{name}: public page has noindex')
    if page.lang not in ['nl','en']:errors.append(f'{name}: language missing')
    if page.alternates.get(page.lang)!=url:errors.append(f'{name}: missing self-language alternate')
    if set(page.alternates)!={'nl','en','x-default'}:errors.append(f'{name}: incomplete language alternates')
    for lang,target in page.alternates.items():
        if not target.startswith(base+'/'):errors.append(f'{name}: non-production alternate {target}');continue
        altfile=page_name(target)
        if altfile not in pages or pages[altfile].alternates!=page.alternates:errors.append(f'{name}: language links not reciprocal')
    for script in re.findall(r'<script type="application/ld\+json" data-seo="identity">(.*?)</script>',texts[name],re.S):json.loads(script)
for name in ['index-magazine.html','index-magazine-en.html','404.html']:
    if name not in pages:continue
    if 'noindex' not in pages[name].robots:errors.append(f'{name}: should not be indexed')
for name in ['index.html','index-en.html']:
    if len([u for u in pages[name].links if u.startswith('project-')])<8:errors.append(f'{name}: selected cases not in HTML')
for name in ['media.html','media-en.html']:
    if len(re.findall(r'<article class="record">',texts[name]))<20:errors.append(f'{name}: media HTML snapshot missing')
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(urls)} sitemap pages; all local links/assets/anchors; reciprocal language tags; canonical and identity metadata; crawlable portfolio/media; noindex alternatives.')
