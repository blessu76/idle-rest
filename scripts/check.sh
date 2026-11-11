#!/bin/bash
# Green gate for idle-rest — run before every commit. Exit 0 = green.
#   scripts/check.sh   # kit pin + sources + unit tests + "build is up to date" (temp copy) + sitemap
# Needs the pinned private kit once per clone:  python3 scripts/kit_lock.py sync --kit ~/Developer/ipe_web_kit
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== 0/5 kit"; python3 scripts/kit_lock.py check
echo "== 1/5 sources"; python3 scripts/build_pages.py --check; python3 scripts/build_journal.py --check
echo "== 2/5 unit tests"; python3 -m unittest discover -s tests -q
echo "== 3/5 build is up to date"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
rsync -a --exclude='.git' ./ "$tmp/"
python3 scripts/build_journal.py --root "$tmp" >/dev/null
if ! diff -r -q --exclude='.git' --exclude='__pycache__' --exclude='scripts' --exclude='tests' --exclude='vendor' --exclude='.github' . "$tmp" >/dev/null 2>&1; then
  diff -r -q --exclude='.git' --exclude='__pycache__' --exclude='scripts' --exclude='tests' --exclude='vendor' --exclude='.github' . "$tmp" | head -10
  echo "generated files are stale — run: python3 scripts/build_journal.py"; exit 1
fi
echo "== 4/5 sitemap"; python3 scripts/check_sitemap.py
echo "GREEN"
