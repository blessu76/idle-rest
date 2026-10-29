"""SEO guide v1 checks on the generated site (repo files) — run: python3 -m unittest discover -s tests"""
import collections
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import build_journal as bj  # noqa: E402


def page_meta(path):
    t = path.read_text(encoding="utf-8")
    g = lambda rx: (re.search(rx, t) or [None, None])[1]
    return t, g(r"<title>(.*?)</title>"), g(r'<meta name="description" content="(.*?)">'), g(r'<html lang="(.*?)"'), g(r'<meta name="robots" content="(.*?)">')


class SeoSite(unittest.TestCase):
    def test_no_duplicate_title_or_description_within_a_language(self):
        seen = collections.defaultdict(list)
        for p in REPO.rglob("index.html"):
            rel = p.relative_to(REPO).parts
            if rel[0] in ("content", "scripts", "tests", "go", ".git"):
                continue
            t, title, desc, lang, robots = page_meta(p)
            if robots and "noindex" in robots:
                continue
            seen[("title", lang, title)].append(str(p.relative_to(REPO)))
            seen[("desc", lang, desc)].append(str(p.relative_to(REPO)))
        dup = {k[:2] + (k[2][:60],): v for k, v in seen.items() if len(v) > 1}
        self.assertEqual(dup, {})

    def test_every_post_links_to_other_posts_of_its_language(self):
        by_lang = collections.Counter()
        for p in (REPO / "journal").glob("*/*/index.html"):
            if p.parent.parent.name in ("page",):
                continue
            t = p.read_text(encoding="utf-8")
            if '<article class="article">' not in t or "noindex" in t.split("</head>")[0]:
                continue
            lang = re.search(r'<html lang="(.*?)"', t).group(1)
            by_lang[lang] += 1
            block = t.split('class="post-more"')
            self.assertEqual(len(block), 2, p)
            links = re.findall(r'href="(/(?:[a-z]{2}/)?journal/(?:[a-z]{2}/)?[^"/]+/)"', block[1].split("</nav>")[0])
            self.assertGreaterEqual(len(links), 3 if by_lang[lang] > 1 else 0, p)
            self.assertNotIn(p.parent.relative_to(REPO).as_posix() + "/", [l.strip("/") + "/" for l in links], p)

    def test_neighbours_and_related_are_same_language_newest_first(self):
        mk = lambda s, d: {"slug": s, "lang": "en", "_date": d}
        posts = [mk("e", 5), mk("d", 4), mk("c", 3), mk("b", 2), mk("a", 1)]
        posts.append({"slug": "x", "lang": "ko", "_date": 9})
        older, newer, rel = bj.post_neighbours(posts[2], posts)
        self.assertEqual((older["slug"], newer["slug"]), ("b", "d"))
        self.assertEqual([q["slug"] for q in rel], ["e", "a"])
        older, newer, rel = bj.post_neighbours(posts[0], posts)
        self.assertEqual((older["slug"], newer, [q["slug"] for q in rel]), ("d", None, ["c", "b", "a"]))

    def test_related_headings_cover_all_languages(self):
        self.assertEqual(set(bj.RELATED), set(bj.LANGS))
