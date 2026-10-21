#!/usr/bin/env python3
"""Build the idle.ipe.rest home page as 12 static language pages — stdlib only (Python 3.8+).

Source   content/home/template.html   English markup with data-i18n / data-i18n-aria hooks and {{PLACEHOLDERS}}
         content/home/i18n.json       strings per language (missing keys fall back to English)
Writes   /<lang>/index.html           en ko ja zh es fr de pt ru ar hi id — html lang/dir, own title·description·og:locale,
                                      canonical = itself, hreflang 12 + x-default
         /index.html                  x-default: English content, canonical "/" , plus a *non-forcing* language hint
                                      (no automatic redirect for crawlers or people; old ?lang=xx links go to /xx/)
         sitemap.xml                  between <!-- home:start --> / <!-- home:end -->
         llms.txt                     between <!-- home:llms:start --> / <!-- home:llms:end -->

It is called by scripts/build_journal.py (one command builds journal + home); the journal cards on each page come from
the published posts (the page language's posts, else the English ones).
"""
import html
import json
import re
from pathlib import Path

import build_journal as bj

SITE = bj.SITE
HOME_UPDATED = "2026-10-22"  # bump when template/i18n copy changes (sitemap lastmod = max(this, newest post date))
TEMPLATE = Path("content") / "home" / "template.html"
STRINGS = Path("content") / "home" / "i18n.json"
LANG_ATTR = re.compile(r'(<(?P<tag>[a-zA-Z0-9]+)(?P<attrs>[^>]*?\sdata-i18n="(?P<key>[^"]+)"[^>]*)>)(?P<inner>.*?)(</(?P=tag)>)', re.S)
ARIA_ATTR = re.compile(r'<[a-zA-Z0-9]+[^>]*?\sdata-i18n-aria="([^"]+)"[^>]*>')
KO_HREF = re.compile(r'(<a\b[^>]*?)\shref="[^"]*"([^>]*?)\sdata-en-href="([^"]*)"\s+data-ko-href="([^"]*)"([^>]*>)')
NAV_SCRIPT = """<script>
(function () {
  var sel = document.getElementById('lang');
  if (sel) sel.addEventListener('change', function () {
    try { localStorage.setItem('ipe_lang', this.value); } catch (e) {}
    location.href = '/' + this.value + '/';
  });
%s})();
</script>"""
HINT_JS = """  // root only: suggest (never force) the visitor's language — stored choice first, then the browser's list
  var hint = document.getElementById('langHint');
  var NAMES = %s;
  if (hint) {
    var off = false; try { off = sessionStorage.getItem('ipe_hint_off') === '1'; } catch (e) {}
    var pick = null, stored = null;
    try { stored = localStorage.getItem('ipe_lang'); } catch (e) {}
    if (stored && NAMES[stored]) pick = stored;
    else { try { var list = navigator.languages || [navigator.language || '']; for (var i = 0; i < list.length && !pick; i++) { var c = String(list[i]).toLowerCase().split('-')[0]; if (NAMES[c]) pick = c; } } catch (e) {} }
    if (pick && pick !== 'en' && !off) {
      hint.innerHTML = '<a href="/' + pick + '/" hreflang="' + pick + '" lang="' + pick + '">' + NAMES[pick] + ' <span aria-hidden="true">→</span></a><button type="button" aria-label="×">×</button>';
      hint.hidden = false;
      hint.querySelector('button').addEventListener('click', function () { hint.hidden = true; try { sessionStorage.setItem('ipe_hint_off', '1'); } catch (e) {} });
    }
  }
"""
LEGACY_JS = ("<script>(function(){try{var l=new URLSearchParams(location.search).get('lang');"
             "if(l&&/^(%s)$/.test(l))location.replace('/'+l+'/'+location.hash);}catch(e){}})();</script>\n")


def esc(s):
    return html.escape(str(s), quote=True)


def lang_url(lang):
    return "%s/%s/" % (SITE, lang)


def card_posts(lang, posts):
    """journal cards on a home page: that language's posts; none yet -> the English originals (else Korean)."""
    own = [p for p in posts if p["lang"] == lang]
    return (own or [p for p in posts if p["lang"] == "en"] or [p for p in posts if p["lang"] == "ko"])[:3]


def render_page(tpl, strings, lang, root, posts):
    d = dict(strings["en"], **strings[lang])
    canonical = SITE + "/" if root else lang_url(lang)
    out = tpl

    def i18n(m):
        val = d.get(m.group("key"))
        if val is None:
            return m.group(0)
        if "data-i18n-inline" in m.group("attrs"):
            val = re.sub(r"\s*<br\s*/?>\s*", "" if lang in ("ja", "zh") else " ", str(val))
        return m.group(1) + str(val) + m.group(6)
    out = LANG_ATTR.sub(i18n, out)

    def aria(m):
        v = d.get(m.group(1))
        if v is None:
            return m.group(0)
        tag = m.group(0)
        if 'aria-label="' in tag:
            return re.sub(r'aria-label="[^"]*"', lambda _: 'aria-label="%s"' % esc(v), tag, count=1)
        return tag[:-1] + ' aria-label="%s">' % esc(v)
    out = ARIA_ATTR.sub(aria, out)
    out = KO_HREF.sub(lambda m: '%s href="%s"%s data-en-href="%s" data-ko-href="%s"%s' % (
        m.group(1), m.group(4) if lang == "ko" else m.group(3), m.group(2), m.group(3), m.group(4), m.group(5)), out)

    cards = card_posts(lang, posts)
    jl = bj.jhome(lang)
    out = bj.replace_between(out, r"<!-- journal:home:start[^>]*-->", "<!-- journal:home:end -->",
                             bj.render_home_cards(cards) if cards else "", "home template")
    out, n = re.subn(r'(<section class="section" id="journal"[^>]*?)( hidden)?>',
                     lambda m: m.group(1) + ("" if cards else " hidden") + ">", out, count=1)
    if n != 1:
        raise SystemExit('home template: <section id="journal"> not found')

    hreflang = "\n".join('<link rel="alternate" hreflang="%s" href="%s">' % (l, lang_url(l)) for l in bj.LANGS)
    hreflang += '\n<link rel="alternate" hreflang="x-default" href="%s/">' % SITE
    og = '<meta property="og:locale" content="%s">' % bj.LANGS[lang]["og"] + "".join(
        '\n<meta property="og:locale:alternate" content="%s">' % bj.LANGS[l]["og"] for l in bj.LANGS if l != lang)
    options = "\n".join('            <option value="%s"%s>%s</option>' % (l, " selected" if l == lang else "", l.upper()) for l in bj.LANGS)
    langs_nav = '    <nav class="lang-list" aria-label="%s"><span>%s</span><ul>%s</ul></nav>' % (
        esc(d["aria_language"]), esc(d["aria_language"]),
        "".join('<li><a href="/%s/" hreflang="%s" lang="%s"%s>%s</a></li>' % (l, l, l, ' aria-current="page"' if l == lang else "", esc(bj.LANGS[l]["name"])) for l in bj.LANGS))
    page_dict = {k: d[k] for k in ("aria_play_yt", "aria_theme_to_dark", "aria_theme_to_light") if k in d}
    page_script = ("<script>window.__PAGE=%s;window.__applyAria=function(el){var v=window.__PAGE.dict[el.getAttribute('data-i18n-aria')];"
                   "if(v!=null)el.setAttribute('aria-label',v);};</script>" % json.dumps({"lang": lang, "dict": page_dict}, ensure_ascii=False))
    names = json.dumps({l: bj.LANGS[l]["name"] for l in bj.LANGS}, ensure_ascii=False)
    subs = {
        "LANG": lang, "DIR": bj.LANGS[lang]["dir"], "CANONICAL": esc(canonical), "HREFLANG": hreflang, "OG_LOCALE": og,
        "LANG_OPTIONS": options, "LANG_LIST": langs_nav, "JOURNAL_HREF": jl,
        "LEGACY_SCRIPT": LEGACY_JS % "|".join(bj.LANGS), "PAGE_SCRIPT": page_script,
        "LANG_HINT": '<div class="lang-hint" id="langHint" hidden></div>\n' if root else "",
        "NAV_SCRIPT": NAV_SCRIPT % (HINT_JS % names if root else ""),
        "meta_title": esc(d["meta_title"]), "meta_desc": esc(d["meta_desc"]),
    }
    out = re.sub(r"\{\{(\w+)\}\}", lambda m: subs[m.group(1)], out)
    # structured data follows the page: WebSite.inLanguage = this language, album url = this page
    out = re.sub(r'("inLanguage": )\[[^\]]*\]', lambda m: m.group(1) + json.dumps(lang), out, count=1)
    out = out.replace('"@type": "MusicAlbum",\n  "name": "dear(you); vol.1",\n  "alternateName": "dear you",\n  "url": "%s/"' % SITE,
                      '"@type": "MusicAlbum",\n  "name": "dear(you); vol.1",\n  "alternateName": "dear you",\n  "url": "%s"' % canonical)
    return out


def sitemap_block(posts):
    last = max([HOME_UPDATED] + [p.get("updated") or p["_date"].isoformat() for p in posts])
    links = "".join('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>\n' % (l, lang_url(l)) for l in bj.LANGS)
    links += '    <xhtml:link rel="alternate" hreflang="x-default" href="%s/"/>\n' % SITE
    img = "    <image:image>\n      <image:loc>%s/og-image.png</image:loc>\n    </image:image>\n" % SITE
    rows = ["  <url>\n    <loc>%s/</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n%s%s  </url>" % (SITE, last, links, img)]
    for l in bj.LANGS:
        rows.append("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>%s</priority>\n%s%s  </url>"
                    % (lang_url(l), last, "0.9" if l in bj.MAIN_LANGS else "0.8", links, img))
    return "\n".join(rows) + "\n"


def llms_block():
    lines = ["## Home page in 12 languages (static pages, one URL per language)"]
    lines += ["- [%s](%s)" % (bj.LANGS[l]["name"], lang_url(l)) for l in bj.LANGS]
    return "\n".join(lines) + "\n"


def build(root, posts, list_langs):
    """write /index.html + /<lang>/index.html, sitemap home block, llms home block. root: Path of the site."""
    bj.LIST_LANGS = set(list_langs)  # (this module imports build_journal under its own name — share the state explicitly)
    tpl = (root / TEMPLATE).read_text(encoding="utf-8")
    strings = json.loads((root / STRINGS).read_text(encoding="utf-8"))
    missing = [l for l in bj.LANGS if l not in strings]
    if missing:
        raise SystemExit("home i18n.json lacks: " + " ".join(missing))
    written = []
    pages = [(None, True)] + [(l, False) for l in bj.LANGS]
    for lang, is_root in pages:
        page = render_page(tpl, strings, lang or "en", is_root, posts)
        path = root / "index.html" if is_root else root / lang / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page, encoding="utf-8")
        written.append(path)
    sm = root / "sitemap.xml"
    sm.write_text(bj.replace_between(sm.read_text(encoding="utf-8"), r"<!-- home:start[^>]*-->", "  <!-- home:end -->",
                                     sitemap_block(posts), "sitemap.xml"), encoding="utf-8")
    llms = root / "llms.txt"
    llms.write_text(bj.replace_between(llms.read_text(encoding="utf-8"), r"<!-- home:llms:start[^>]*-->",
                                       "<!-- home:llms:end -->", llms_block(), "llms.txt"), encoding="utf-8")
    return written
