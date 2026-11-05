"""Rebuild languages, problem pages, speaker/cases, HTML snapshots and SEO metadata."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
for script in ['build_locales.py','build_challenges.py','build_seo.py','verify_site.py']:
    subprocess.run([sys.executable,str(root/script)],check=True,cwd=root)
