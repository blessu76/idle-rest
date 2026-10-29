#!/usr/bin/env python3
"""Notify IndexNow (Bing, Naver, Yandex, ...) about new or changed URLs.

Run AFTER the site is published (the key file must already be live):

    python3 scripts/indexnow.py                 # every <loc> in sitemap.xml
    python3 scripts/indexnow.py URL [URL ...]   # only these URLs
    python3 scripts/indexnow.py --dry-run       # print the payload, send nothing
    python3 scripts/indexnow.py --today         # only <loc> whose <lastmod> is today (KST) — used by the deploy workflow (same as ipe-rest)
    python3 scripts/indexnow.py --changed-since REV   # only pages whose index.html changed between REV and HEAD (CI, after deploy)

The key is the repo-root file named <32 hex>.txt whose single line is the key
itself. It is a public file (not a secret). Standard library only.
"""
import argparse
import datetime
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = "https://api.indexnow.org/indexnow"
KEY_FILE_RE = re.compile(r"^([0-9a-f]{32})\.txt$")
LOC_TAG = "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"


def find_key(root):
    """Return the key whose <key>.txt file in `root` contains exactly that key."""
    for p in sorted(Path(root).iterdir()):
        m = KEY_FILE_RE.match(p.name)
        if m and p.read_text(encoding="utf-8").strip() == m.group(1):
            return m.group(1)
    raise SystemExit("no IndexNow key file (<32 hex>.txt containing its own name) in " + str(root))


def sitemap_urls(sitemap_path):
    """All <loc> values of a sitemap (xhtml:link alternates are not included)."""
    tree = ET.parse(sitemap_path)
    urls = [e.text.strip() for e in tree.iter(LOC_TAG) if e.text and e.text.strip()]
    return list(dict.fromkeys(urls))


BUILD_ONLY = ("content/", "scripts/", "tests/", "go/", ".github/")  # not published (or redirect pages, not for indexing)


def changed_urls(root, base, host=None):
    """Public URLs of the index.html pages that changed between git rev `base` and HEAD (noindex pages and build-only paths skipped).
    A rev that does not exist (first push, force-push) falls back to HEAD~1."""
    root = Path(root)
    def git(*args):
        return subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, text=True)
    if git("rev-parse", "--verify", "--quiet", base + "^{commit}").returncode != 0 or set(base) == {"0"}:
        base = "HEAD~1"
    r = git("diff", "--name-only", "--diff-filter=AM", base, "HEAD")
    if r.returncode != 0:
        raise SystemExit("git diff failed: " + r.stderr.strip())
    if host is None:
        host = (root / "CNAME").read_text(encoding="utf-8").split()[0]
    urls = []
    for name in r.stdout.split("\n"):
        if not (name == "index.html" or name.endswith("/index.html")) or name.startswith(BUILD_ONLY):
            continue
        head = (root / name).read_text(encoding="utf-8").split("</head>")[0]
        if re.search(r'<meta name="robots" content="[^"]*noindex', head):
            continue
        urls.append("https://%s/%s" % (host, name[:-len("index.html")]))
    return sorted(urls)


def sitemap_urls_modified(sitemap_path, day):
    """<loc> values whose <lastmod> starts with `day` (YYYY-MM-DD)."""
    out = []
    for u in ET.parse(sitemap_path).getroot():
        loc = u.find(LOC_TAG)
        mod = u.find(LOC_TAG.replace("}loc", "}lastmod"))
        if loc is not None and loc.text and mod is not None and (mod.text or "").strip().startswith(day):
            out.append(loc.text.strip())
    return list(dict.fromkeys(out))


def today_kst():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()


def build_payload(key, urls):
    if not urls:
        raise SystemExit("no URLs to submit")
    hosts = {urlsplit(u).netloc for u in urls}
    if len(hosts) != 1 or "" in hosts:
        raise SystemExit("all URLs must share one host, got: " + ", ".join(sorted(hosts)))
    host = hosts.pop()
    return {
        "host": host,
        "key": key,
        "keyLocation": "https://%s/%s.txt" % (host, key),
        "urlList": list(urls),
    }


def send(payload, endpoint=ENDPOINT, timeout=30):
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def key_status(url, timeout=15):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except OSError:
        return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*", help="URLs to submit (default: every <loc> in sitemap.xml)")
    ap.add_argument("--root", default=str(ROOT), help="site root (default: this repo)")
    ap.add_argument("--today", action="store_true", help="only sitemap URLs whose lastmod is today (KST); nothing to send = exit 0")
    ap.add_argument("--changed-since", metavar="REV", help="submit only the pages changed between git REV and HEAD")
    ap.add_argument("--wait-key", type=int, default=0, metavar="SEC", help="wait up to SEC seconds for the key file to be live first")
    ap.add_argument("--dry-run", action="store_true", help="print the payload, send nothing")
    a = ap.parse_args(argv)

    root = Path(a.root)
    if a.today:
        urls = sitemap_urls_modified(root / "sitemap.xml", today_kst())
        if not urls:
            print("IndexNow: no sitemap URL with lastmod %s — nothing to submit" % today_kst())
            return 0
    elif a.changed_since:
        urls = changed_urls(root, a.changed_since)
        if not urls:
            print("IndexNow: no changed pages")
            return 0
    else:
        urls = a.urls or sitemap_urls(root / "sitemap.xml")
    payload = build_payload(find_key(root), urls)
    if a.wait_key and not a.dry_run:
        deadline = time.time() + a.wait_key
        while key_status(payload["keyLocation"]) != 200 and time.time() < deadline:
            time.sleep(10)
    if a.dry_run:
        print("POST " + ENDPOINT)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    status = send(payload)
    print("IndexNow %s: HTTP %d (%d URLs)" % (payload["host"], status, len(urls)))
    if status in (200, 202):
        return 0
    print("200/202 = ok; 403 = key file not live yet / key mismatch; 422 = URL host mismatch; 429 = too many requests", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
