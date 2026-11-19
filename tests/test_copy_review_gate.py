"""Live content must carry the Iris copy review (the gate that let two 'pending' posts through)."""
import datetime as dt
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
FROM = dt.date(2026, 11, 14)


def meta(path):
    m = re.match(r"---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    return dict(l.split(": ", 1) for l in m.group(1).splitlines() if ": " in l)


class LiveContentReviewed(unittest.TestCase):
    def test_every_published_post_from_nov_14_is_iris_reviewed(self):
        bad = []
        for f in sorted((ROOT / "content/journal").glob("*/*.md")):
            m = meta(f)
            if m.get("draft") == "true" or dt.date.fromisoformat(m["date"]) < FROM:
                continue
            if m.get("copy_review") != "iris":
                bad.append("%s: copy_review=%s" % (f.relative_to(ROOT), m.get("copy_review")))
            try:
                dt.date.fromisoformat(m.get("copy_review_date", ""))
            except ValueError:
                bad.append("%s: copy_review_date missing" % f.relative_to(ROOT))
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
