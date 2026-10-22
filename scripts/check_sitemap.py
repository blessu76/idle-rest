#!/usr/bin/env python3
"""Check sitemap.xml against the published journal posts — stdlib only (Python 3.8+). Exit 1 on any problem.

  python3 scripts/check_sitemap.py            # offline checks
  python3 scripts/check_sitemap.py --live     # + every sitemap URL answers HTTP 200 (run after deploy)

Offline checks:
  1. sitemap.xml is valid XML.
  2. Every published (non-draft) journal URL is listed: /journal/ (hub), /journal/<lang>/ for each language that has a post,
     and every post page (content/journal/<lang>/<slug>.md). Nothing journal-ish is listed that is not published
     (redirect stubs for old URLs must NOT be listed).
  3. Home: / (x-default) and /<lang>/ for all 12 languages are listed (static pages, no ?lang=).
  4. Pages: /about/ /contact/ /privacy/ (x-default) and /<lang>/<slug>/ for all 12 languages are listed (3 x 13 = 39 URLs).
  5. Every <loc> maps to a file on disk (index.html of that path).
  6. hreflang (every <url> that has alternates): lists itself + x-default; every hreflang target is itself a <loc> in the sitemap;
     references are reciprocal (if A lists B under lang L, B lists A under A's lang).
"""
import argparse
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_journal as bj  # noqa: E402
import build_pages as bp  # noqa: E402

NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}


def published_posts(root):
    posts = []
    src = root / "content" / "journal"
    for f in sorted(src.glob("*/*.md")) if src.is_dir() else []:
        if f.name.lower() == "readme.md":
            continue
        p = bj.parse_post(f)
        if not p["draft"]:
            posts.append(p)
    return posts


def check(root):
    errs = []
    try:
        tree = ET.parse(root / "sitemap.xml")
    except (ET.ParseError, OSError) as ex:
        return ["sitemap.xml: %s" % ex], []
    urls = {}
    for u in tree.getroot().findall("s:url", NS):
        loc = (u.findtext("s:loc", namespaces=NS) or "").strip()
        urls[loc] = [(l.get("hreflang"), l.get("href")) for l in u.findall("x:link", NS)]
    try:
        posts = published_posts(root)
    except ValueError as ex:
        return ["journal sources: %s" % ex], list(urls)
    want = {bj.SITE + "/journal/"} if posts else set()
    want.add(bj.SITE + "/")  # home: x-default + one static page per language
    want.update("%s/%s/" % (bj.SITE, l) for l in bj.LANGS)
    for slug in bp.SLUGS:  # trust pages: x-default + one per language
        want.update(bp.page_url(l, slug) for l in (None,) + tuple(bj.LANGS))
    for p in posts:
        want.add(bj.post_url(p))
        want.add(bj.SITE + bj.lang_path(p["lang"]))
    for u in sorted(want - set(urls)):
        errs.append("missing from sitemap: %s" % u)
    for u in sorted(urls):
        if not u.startswith(bj.SITE + "/"):
            errs.append("not an idle.ipe.rest URL: %s" % u)
        elif not (root / u[len(bj.SITE) + 1:] / "index.html").is_file():
            errs.append("no file for sitemap URL (expected %sindex.html): %s" % (u[len(bj.SITE) + 1:], u))
    for u in sorted(u for u in urls if "/journal/" in u and u not in want):
        errs.append("in sitemap but not a published journal page: %s" % u)
    for loc, links in urls.items():
        if not links:  # a page without alternates (single language) needs no hreflang
            continue
        langs = [l for l, _ in links]
        if len(set(langs)) != len(langs):
            errs.append("%s: duplicate hreflang" % loc)
        if "x-default" not in langs:
            errs.append("%s: no x-default" % loc)
        mine = [l for l, h in links if h == loc and l != "x-default"]
        defaults = (bj.SITE + "/journal/", bj.SITE + "/") + tuple(bp.page_url(None, s) for s in bp.SLUGS)
        if not mine and loc not in defaults:  # hub, root and the x-default trust pages are only the x-default of their language pages
            errs.append("%s: does not list itself in hreflang" % loc)
        for lang, href in links:
            if href not in urls:
                errs.append("%s: hreflang %s -> %s is not in the sitemap" % (loc, lang, href))
            elif lang != "x-default" and href != loc and mine and (mine[0], loc) not in urls[href]:
                errs.append("%s: hreflang %s -> %s is not reciprocal (it does not list %s as %s)" % (loc, lang, href, loc, mine[0]))
    return errs, list(urls)


def live(urls):
    errs = []
    for u in urls:
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "check_sitemap/1"}), timeout=20) as r:
                if r.status != 200:
                    errs.append("HTTP %s: %s" % (r.status, u))
        except Exception as ex:  # noqa: BLE001 — any failure is a failed check
            errs.append("%s: %s" % (u, ex))
    return errs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--live", action="store_true", help="also GET every sitemap URL and require HTTP 200")
    a = ap.parse_args()
    errs, urls = check(Path(a.root).resolve())
    if a.live and not errs:
        errs += live(urls)
    if errs:
        print("sitemap: %d problem(s)\n  " % len(errs) + "\n  ".join(errs), file=sys.stderr)
        return 1
    print("sitemap: OK — %d URL(s)%s" % (len(urls), ", all HTTP 200" if a.live else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
