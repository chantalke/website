#!/usr/bin/env bash
# Run the same build locally; publishing is performed by the GitHub Actions workflow.
set -euo pipefail
cd "$(dirname "$0")/.."
export SITE_URL="${SITE_URL:-https://chantalke.github.io/website}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" website/build_site.py
"$PYTHON_BIN" prepare_publish.py
for file in website/*.js; do node --check "$file"; done
printf '\nGitHub Pages files are ready in output/website-liveklaar/\n'
printf 'Commit and push to main to run the deployment workflow.\n'
