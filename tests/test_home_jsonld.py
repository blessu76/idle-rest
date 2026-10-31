"""Consistency of the hand-written music JSON-LD on the home page — run: python3 -m unittest discover -s tests"""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
YT = re.compile(r"^https://youtu\.be/([A-Za-z0-9_-]{11})$")


def blocks(path):
    html = (REPO / path).read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        out.append(json.loads(m.group(1)))
    return out


class HomeMusicJsonLd(unittest.TestCase):
    def setUp(self):
        data = blocks("index.html")
        self.album = next((b for b in data if b.get("@type") == "MusicAlbum"), None)
        self.singles = next((b for b in data if b.get("@type") == "ItemList"), None)
        self.assertIsNotNone(self.album, "홈에 MusicAlbum JSON-LD 없음")
        self.assertIsNotNone(self.singles, "홈에 싱글 ItemList JSON-LD 없음")
        self.assertGreater(len(self.album["track"]), 0, "앨범 track 이 비어 있음")
        self.assertGreater(len(self.singles["itemListElement"]), 0, "싱글 itemListElement 가 비어 있음")
        self.album_urls = [t["url"] for t in self.album["track"]]
        self.single_urls = [i["item"]["url"] for i in self.singles["itemListElement"]]

    def test_num_tracks_matches_track_list(self):
        self.assertEqual(self.album["numTracks"], len(self.album["track"]))

    def test_positions_run_from_one_without_gaps(self):
        self.assertEqual([t["position"] for t in self.album["track"]], list(range(1, len(self.album["track"]) + 1)))
        self.assertEqual([i["position"] for i in self.singles["itemListElement"]],
                         list(range(1, len(self.singles["itemListElement"]) + 1)))

    def test_youtube_ids_are_well_formed_and_unique(self):
        urls = self.album_urls + self.single_urls
        ids = []
        for u in urls:
            m = YT.match(u)
            self.assertIsNotNone(m, u)
            ids.append(m.group(1))
        self.assertEqual(len(ids), len(set(ids)), "duplicate youtu.be id")

    def test_singles_do_not_overlap_album_tracks(self):
        self.assertFalse(set(self.single_urls) & set(self.album_urls))


if __name__ == "__main__":
    unittest.main()
