"""Prepare a static upload directory; never uploads or deploys anything."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,urljoin
import hashlib,json,re,shutil,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'website';OUT=ROOT/'output/website-liveklaar'
sys.path.insert(0,str(SOURCE))
from site_config import page_name
OUT.mkdir(parents=True,exist_ok=True)
# Delete only the generated files from a previous run, never source files.
for p in OUT.iterdir():
 if p.is_dir():shutil.rmtree(p)
 else:p.unlink()
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
pages=[page_name(n.text) for n in ET.parse(SOURCE/'sitemap.xml').findall('s:url/s:loc',ns)]
for name in pages+['404.html','robots.txt','sitemap.xml','_redirects']:
 (OUT/name).parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(SOURCE/name,OUT/name)
for pattern in ['*.css','*.js']:
 for p in SOURCE.glob(pattern):shutil.copy2(p,OUT/p.name)
shutil.copytree(SOURCE/'assets',OUT/'assets')
# The superseded hero movie is retained in source/backups, not uploaded.
(OUT/'assets/experience-loop.mp4').unlink(missing_ok=True)
# Only the reviewed public copy belongs in downloadable JS data.
copy=json.loads((SOURCE/'public-project-copy.json').read_text())
for lang,name in [('nl','data.js'),('en','data.en.js')]:
 p=OUT/name;d=json.loads(p.read_text().removeprefix('const DATA = ').strip().removesuffix(';'))
 for project in d['projects']:
  project.update(copy[lang].get(project['id'],{}));project.pop('selection',None)
 p.write_text('const DATA = '+json.dumps(d,ensure_ascii=False)+';\n')
for p in OUT.rglob('*.html'):
 def version(m):
  f=OUT/m[2]
  return m[1]+'"'+m[2]+'?v='+hashlib.sha256(f.read_bytes()).hexdigest()[:10]+'"' if f.is_file() else m[0]
 p.write_text(re.sub(r'((?:src|href)=)"([^"?]+\.(?:js|css))(?:\?[^\"]*)?"',version,p.read_text()))
# Check the files after copying, including CSS imports and font/video sources.
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.images=[];self.base=''
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='base':self.base=a.get('href','')
  if 'id' in a:self.ids.append(a['id'])
  if t=='img':self.images.append(a)
  if t in ['a','link'] and a.get('href'):self.links.append(a['href'])
  if t in ['img','script','source','video']:
   for k in ['src','poster']:
    if a.get(k):self.links.append(a[k])
parsed={}
for p in OUT.rglob('*.html'):
 h=Page();h.feed(p.read_text());parsed[str(p.relative_to(OUT))]=h
errors=[]
for name,p in parsed.items():
 if len(p.ids)!=len(set(p.ids)):errors.append(name+': duplicate IDs')
 for im in p.images:
  if 'alt' not in im:errors.append(name+': image missing alt')
 for href in p.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  resolved=urlsplit(urljoin(urljoin('https://local.test/'+name,p.base),href))
  f=unquote(resolved.path).lstrip('/')
  if f.endswith('/'):f+='index.html'
  if not (OUT/f).is_file():errors.append(name+': missing '+href)
  elif u.fragment and f in parsed and u.fragment not in parsed[f].ids:errors.append(name+': missing anchor '+href)
for p in OUT.rglob('*.css'):
 for target in re.findall(r'url\([\'\"]?([^\)\'\"]+)',p.read_text()):
  if not urlsplit(target).scheme and not (p.parent/urlsplit(target).path).is_file():errors.append(str(p)+': missing CSS asset '+target)
assert not errors,'\n'.join(errors)
print(f'PASS: clean upload directory; {len(pages)} public pages, local links, anchors, duplicate IDs, alt attributes, CSS/font and video assets.')
(OUT/'.nojekyll').touch()
print(OUT)
