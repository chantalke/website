"""Shared public URL configuration for custom domains and GitHub Pages subpaths."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json,os
ROOT=Path(__file__).resolve().parent
SITE_URL=os.environ.get('SITE_URL',json.loads((ROOT/'seo-config.json').read_text())['site_url']).strip().rstrip('/')
u=urlsplit(SITE_URL)
assert u.scheme=='https' and u.hostname and u.hostname not in ['localhost','127.0.0.1'], 'SITE_URL must be a public HTTPS URL'
assert not (u.query or u.fragment or u.username or u.password), 'SITE_URL cannot contain credentials, a query or a fragment'
def page_name(url):
    assert url.startswith(SITE_URL+'/'), f'URL outside this site: {url}'
    return unquote(url[len(SITE_URL)+1:]) or 'index.html'
