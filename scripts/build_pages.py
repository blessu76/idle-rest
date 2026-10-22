#!/usr/bin/env python3
"""Build the idle.ipe.rest trust pages (About / Contact / Privacy Policy) in 12 languages — stdlib only (Python 3.8+).

Source   content/pages/<lang>/<slug>.html     lang: en ko ja zh es fr de pt ru ar hi id · slug: about contact privacy
         header lines  title: desc: h1: sub: [ai:]   then a line "---", then the HTML body.
         en + ko are the human-written originals (no ai: line). The other 10 are AI translations: they must carry an
         ai: line (shown at the very top, with links to the originals through {{ORIGINALS}}).
         Placeholders {{OPERATOR}} {{EMAIL}} {{EFFECTIVE}} {{REPLY_DAYS}} {{ABOUT}} {{CONTACT}} {{PRIVACY}} {{JOURNAL}}
         {{SOCIAL_LI}} {{SOCIAL_LINKS}} are filled from this file — never write the operator or e-mail in a source file.
Writes   /<lang>/<slug>/index.html            36 pages — canonical = itself, hreflang 12 + x-default (absolute URLs),
                                              language <select> top right (idle.js), no bottom language list
         /<slug>/index.html                   x-default: English text + a no-JS list of the 12 language pages;
                                              old ?lang=xx goes to /xx/<slug>/; the browser language is only *suggested*
         sitemap.xml                          between <!-- pages:start --> / <!-- pages:end -->
         llms.txt                             between <!-- pages:llms:start --> / <!-- pages:llms:end -->

    python3 scripts/build_pages.py           # build (build_journal.py also calls this)
    python3 scripts/build_pages.py --check   # validate the sources only (translations must mirror the English structure)
Running it twice produces identical files (idempotent).
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_journal as bj  # noqa: E402

SITE = bj.SITE
OPERATOR = "Davy Kim (ipe Studio)"
EMAIL = "ipe.haven@gmail.com"
EFFECTIVE = "2026-10-20"
REPLY_DAYS = 10
PAGES_UPDATED = "2026-10-23"  # sitemap lastmod of the 39 page URLs; bump when any content/pages text changes
SLUGS = ("about", "contact", "privacy")
SRC = Path("content") / "pages"
HEADER_KEYS = ("title", "desc", "h1", "sub", "ai")
PLACEHOLDER = re.compile(r"\{\{([A-Z_]+)\}\}")
SCHEMA = {"about": "AboutPage", "contact": "ContactPage", "privacy": "WebPage"}

SOCIAL = (
    ("YouTube", "https://www.youtube.com/@ipe-rest"),
    ("Instagram", "https://www.instagram.com/ipe.rest"),
    ("SoundCloud", "https://soundcloud.com/ipe-rest"),
)
SOCIAL_LI = "\n".join('<li><a href="%s" rel="noopener">%s</a></li>' % (u, n) for n, u in SOCIAL)
SOCIAL_LINKS = ", ".join('<a href="%s" rel="noopener">%s</a>' % (u, n) for n, u in SOCIAL)

HINT_JS = """<script>
(function () {
  var SLUG = %s, NAMES = %s;
  try { var q = new URLSearchParams(location.search).get('lang'); if (q && Object.prototype.hasOwnProperty.call(NAMES, q)) { location.replace('/' + q + '/' + SLUG + '/' + location.hash); return; } } catch (e) {}
  // suggest (never force) the visitor's language: stored choice first, then the browser's list
  var hint = document.getElementById('langHint');
  if (!hint) return;
  var off = false; try { off = sessionStorage.getItem('ipe_hint_off') === '1'; } catch (e) {}
  var pick = null, stored = null;
  try { stored = localStorage.getItem('ipe_lang'); } catch (e) {}
  if (stored && Object.prototype.hasOwnProperty.call(NAMES, stored)) pick = stored;
  else { try { var list = navigator.languages || [navigator.language || '']; for (var i = 0; i < list.length && !pick; i++) { var c = String(list[i]).toLowerCase().split('-')[0]; if (Object.prototype.hasOwnProperty.call(NAMES, c)) pick = c; } } catch (e) {} }
  if (pick && pick !== 'en' && !off) {
    hint.innerHTML = '<a href="/' + pick + '/' + SLUG + '/" hreflang="' + pick + '" lang="' + pick + '">' + NAMES[pick] + ' <span aria-hidden="true">→</span></a><button type="button" aria-label="×">×</button>';
    hint.hidden = false;
    hint.querySelector('button').addEventListener('click', function () { hint.hidden = true; try { sessionStorage.setItem('ipe_hint_off', '1'); } catch (e) {} });
  }
})();
</script>
"""

TAG = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*)>")
HREF = re.compile(r'\shref="([^"]*)"')
CLS = re.compile(r'\sclass="([^"]*)"')
NUMBERED = re.compile(r"^\s*(\d+)\.")


def page_path(lang, slug):
    """site path of a page: /<lang>/<slug>/ ; lang=None -> the x-default /<slug>/."""
    return "/%s/%s/" % (lang, slug) if lang else "/%s/" % slug


def page_url(lang, slug):
    return SITE + page_path(lang, slug)


def strip_tags(s):
    return TAG.sub("", s)


# ---------------------------------------------------------------- sources
def parse_source(path):
    """-> ({title, desc, h1, sub, [ai]}, body). ValueError on a malformed file."""
    text = path.read_text(encoding="utf-8")
    head, sep, body = text.partition("\n---\n")
    if not sep:
        raise ValueError("no '---' line between the header and the body")
    meta = {}
    for ln in head.splitlines():
        if not ln.strip():
            continue
        k, c, v = ln.partition(":")
        k = k.strip()
        if not c or k not in HEADER_KEYS:
            raise ValueError("bad header line: %r (allowed: %s)" % (ln[:40], ", ".join(HEADER_KEYS)))
        if k in meta:
            raise ValueError("duplicate header: " + k)
        meta[k] = v.strip()
    for k in ("title", "desc", "h1", "sub"):
        if not meta.get(k):
            raise ValueError("missing header: " + k)
    return meta, body.strip("\n") + "\n"


def skeleton(body):
    """what a translation must keep: the tag sequence (+ class), every href, every placeholder, numbered h2 prefixes."""
    tags = [("/" if m.group(1) else "") + m.group(2).lower() + ("." + c.group(1) if (c := CLS.search(m.group(3))) and not m.group(1) else "")
            for m in TAG.finditer(body)]
    hrefs = [m.group(1) for t in TAG.finditer(body) for m in HREF.finditer(t.group(3))]
    ph = sorted(PLACEHOLDER.findall(body))
    nums = [NUMBERED.match(strip_tags(m.group(1))).group(1) if NUMBERED.match(strip_tags(m.group(1))) else ""
            for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", body, re.S)]
    return tags, hrefs, ph, nums


def load(root):
    """-> ({(lang, slug): (meta, body)}, [errors]). Checks every file; translations must mirror the English one."""
    pages, errs = {}, []
    for lang in bj.LANGS:
        for slug in SLUGS:
            f = root / SRC / lang / (slug + ".html")
            where = "content/pages/%s/%s.html" % (lang, slug)
            if not f.is_file():
                errs.append("%s: missing" % where)
                continue
            try:
                meta, body = parse_source(f)
            except ValueError as ex:
                errs.append("%s: %s" % (where, ex))
                continue
            pages[(lang, slug)] = (meta, body)
            raw = f.read_text(encoding="utf-8")
            for lit in (EMAIL, "Davy Kim", "ipe Studio"):
                if lit in raw:
                    errs.append("%s: write {{OPERATOR}}/{{EMAIL}}, not %r" % (where, lit))
            for ph in PLACEHOLDER.findall(raw):
                if ph not in PH_NAMES:
                    errs.append("%s: unknown placeholder {{%s}}" % (where, ph))
            if lang in bj.MAIN_LANGS:
                if "ai" in meta:
                    errs.append("%s: an original (en/ko) must not carry an ai: line" % where)
            else:
                ai = meta.get("ai", "")
                if not ai:
                    errs.append("%s: AI translation needs an ai: line" % where)
                else:
                    for need in ("{{ORIGINALS}}", "English", "한국어"):
                        if need not in ai:
                            errs.append("%s: ai: line must contain %s" % (where, need))
    for slug in SLUGS:
        base = pages.get(("en", slug))
        if not base:
            continue
        want = skeleton(base[1])
        for lang in bj.LANGS:
            if lang == "en" or (lang, slug) not in pages:
                continue
            got = skeleton(pages[(lang, slug)][1])
            where = "content/pages/%s/%s.html" % (lang, slug)
            hdr = lambda m: sorted(PLACEHOLDER.findall(" ".join(m[k] for k in ("title", "desc", "h1", "sub"))))
            checks = list(zip(("tags", "links", "placeholders", "numbered sections"), want, got))
            checks.append(("header placeholders", hdr(base[0]), hdr(pages[(lang, slug)][0])))
            for label, a, b in checks:
                if a != b:
                    errs.append("%s: %s differ from English (add/remove nothing — translate sentence for sentence)" % (where, label))
    return pages, errs


PH_NAMES = {"OPERATOR", "EMAIL", "EFFECTIVE", "REPLY_DAYS", "ABOUT", "CONTACT", "PRIVACY", "JOURNAL", "SOCIAL_LI", "SOCIAL_LINKS", "ORIGINALS"}


# ---------------------------------------------------------------- render
def fill(text, lang, slug, plain):
    """replace placeholders. plain=True for attribute/meta text (no markup); lang=None is the x-default page."""
    rtl = bool(lang) and bj.LANGS[lang]["dir"] == "rtl"
    pre = ("/" + lang) if lang else ""
    # rtl: the ISO date stays left-to-right (LRI … PDI)
    vals = {"EMAIL": EMAIL, "EFFECTIVE": "\u2066%s\u2069" % EFFECTIVE if rtl else EFFECTIVE, "REPLY_DAYS": str(REPLY_DAYS),
            "OPERATOR": OPERATOR if plain or not rtl else '<bdi class="ltr">%s</bdi>' % OPERATOR,
            "ABOUT": pre + "/about/", "CONTACT": pre + "/contact/", "PRIVACY": pre + "/privacy/",
            "JOURNAL": bj.jhome(lang) if lang else "/journal/",
            "SOCIAL_LI": SOCIAL_LI, "SOCIAL_LINKS": SOCIAL_LINKS}
    if rtl and not plain:  # e-mail addresses read left-to-right inside Arabic text
        text = text.replace('<a href="mailto:{{EMAIL}}">', '<a href="mailto:{{EMAIL}}" class="ltr">')
    return PLACEHOLDER.sub(lambda m: vals.get(m.group(1), m.group(0)), text)


def originals(slug):
    return " · ".join('<a href="%s" hreflang="%s" lang="%s">%s</a>' % (page_path(l, slug), l, l, bj.esc(n))
                      for l, n in (("en", "English"), ("ko", "한국어")))


def render(pages, lang, slug):
    """lang=None -> the x-default /<slug>/ (English text + language list)."""
    src_lang = lang or "en"
    meta, body = pages[(src_lang, slug)]
    plain = lambda s: fill(s, lang, slug, True)
    title, desc = plain(meta["title"]), plain(meta["desc"])
    canonical = page_url(lang, slug)
    alts = "".join('<link rel="alternate" hreflang="%s" href="%s">\n' % (l, page_url(l, slug)) for l in bj.LANGS)
    alts += '<link rel="alternate" hreflang="x-default" href="%s">\n' % page_url(None, slug)
    ldobj = {
        "@context": "https://schema.org", "@type": SCHEMA[slug], "name": title, "url": canonical, "inLanguage": src_lang,
        "isPartOf": {"@type": "WebSite", "name": "idle() — the music of ipe()", "url": SITE + "/"},
        "publisher": {"@type": "Organization", "name": "ipe()", "url": "https://ipe.rest/"},
    }
    out = bj.head(title, desc, canonical, src_lang, False, extra=bj.ld(ldobj), hint="edit content/pages/*/*.html and rebuild",
                  alternates=alts, locales=list(bj.LANGS), gen="generated by scripts/build_pages.py")
    out += bj.header(src_lang, current=slug, targets={l: page_path(l, slug) for l in bj.LANGS})
    if lang is None:
        out += '<div class="lang-hint" id="langHint" hidden></div>\n'
    out += '<main id="main" class="shell">\n<div class="doc">\n'
    if "ai" in meta:
        ai = bj.esc(plain(meta["ai"])).replace("{{ORIGINALS}}", originals(slug))
        out += '<p class="ai-note"><span class="ai-badge">AI</span> %s</p>\n' % ai
    out += '<div class="page-head">\n  <h1>%s</h1>\n  <p>%s</p>\n</div>\n' % (bj.esc(plain(meta["h1"])), bj.esc(plain(meta["sub"])))
    if lang is None:
        out += '<nav class="lang-pick" aria-label="%s">\n  <p class="lang-pick-label">%s</p>\n  <ul class="lang-grid">\n' % (
            bj.esc(bj.ui("en")["other_langs"]), bj.esc(bj.ui("en")["other_langs"]))
        out += "".join('    <li><a class="lang-card" href="%s" hreflang="%s" lang="%s">%s</a></li>\n' % (
            page_path(l, slug), l, l, bj.esc(bj.LANGS[l]["name"])) for l in bj.LANGS)
        out += "  </ul>\n</nav>\n"
    out += '<div class="prose">\n%s</div>\n</div>\n</main>\n' % fill(body, lang, slug, False)
    foot = bj.footer(src_lang, default=lang is None)
    if lang is None:
        names = json.dumps({l: bj.LANGS[l]["name"] for l in bj.LANGS}, ensure_ascii=False)
        foot = foot.replace('<script src="/assets/idle.js', HINT_JS % (json.dumps(slug), names) + '<script src="/assets/idle.js', 1)
    return out + foot


def sitemap_block():
    rows = []
    for slug in SLUGS:
        links = "".join('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>\n' % (l, page_url(l, slug)) for l in bj.LANGS)
        links += '    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>\n' % page_url(None, slug)
        for lang in (None,) + tuple(bj.LANGS):
            rows.append("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>%s</priority>\n%s  </url>"
                        % (page_url(lang, slug), PAGES_UPDATED, "0.6" if lang in (None, "en", "ko") else "0.5", links))
    return "\n".join(rows) + "\n"


def llms_block():
    label = {"about": "About (operator and how the music is made)", "contact": "Contact", "privacy": "Privacy Policy"}
    lines = []
    for slug in SLUGS:
        langs = " · ".join("%s: %s" % (bj.LANGS[l]["name"], page_url(l, slug)) for l in bj.LANGS)
        lines.append("- %s: %s — in 12 languages (English and Korean are the originals; the other ten are AI translations, the originals prevail): %s"
                     % (label[slug], page_url(None, slug), langs))
    return "\n".join(lines) + "\n"


def build(root, list_langs=None):
    """write the 39 pages + the sitemap/llms blocks. root: Path of the site."""
    root = Path(root)
    pages, errs = load(root)
    if errs:
        print("pages: errors\n  " + "\n  ".join(errs), file=sys.stderr)
        raise SystemExit(1)
    # build_journal may be running as __main__ — share its state explicitly (see also the sys.modules alias there)
    bj.ROOT = root
    if list_langs is not None:
        bj.LIST_LANGS = set(list_langs)
    tpl = root / "content" / "home" / "template.html"
    m = re.search(r'<html[^>]*\sdata-ads="(on|off)"', (tpl if tpl.exists() else root / "index.html").read_text(encoding="utf-8"))
    bj.ADS_ATTR = m.group(1) if m else "off"
    n = 0
    for slug in SLUGS:
        for lang in (None,) + tuple(bj.LANGS):
            d = root / (lang or "") / slug
            d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(render(pages, lang, slug), encoding="utf-8")
            n += 1
    sm = root / "sitemap.xml"
    sm.write_text(bj.replace_between(sm.read_text(encoding="utf-8"), r"<!-- pages:start[^>]*-->", "  <!-- pages:end -->",
                                     sitemap_block(), "sitemap.xml"), encoding="utf-8")
    llms = root / "llms.txt"
    llms.write_text(bj.replace_between(llms.read_text(encoding="utf-8"), r"<!-- pages:llms:start[^>]*-->",
                                       "<!-- pages:llms:end -->", llms_block(), "llms.txt"), encoding="utf-8")
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="site root (default: this repo)")
    ap.add_argument("--check", action="store_true", help="validate the sources only, write nothing")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    if a.check:
        pages, errs = load(root)
        if errs:
            print("pages: %d problem(s)\n  " % len(errs) + "\n  ".join(errs), file=sys.stderr)
            return 1
        print("pages: OK — %d source file(s)" % len(pages))
        return 0
    import check_sitemap  # standalone run: the journal link of a page goes to that language's list only if the list exists
    langs = {p["lang"] for p in check_sitemap.published_posts(root)}
    print("pages: built %d page(s)" % build(root, langs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
