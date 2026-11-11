"""The private ipe_web_kit is pinned by vendor/ipe_web_kit.lock (the source is not in this public repo).
The pin itself is always checked; checks against the installed kit run only when vendor/ipe_web_kit/ is installed
(scripts/check.sh requires it; the 19:00 publisher clone does not need it)."""
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import kit_lock  # noqa: E402

INSTALLED = (REPO / "vendor" / "ipe_web_kit" / "KIT_VERSION").is_file()


def run(root, *args):
    return subprocess.run([sys.executable, str(REPO / "scripts" / "kit_lock.py"), "--root", str(root), *args], capture_output=True, text=True)


class KitPin(unittest.TestCase):
    def test_lock_format(self):
        lock = kit_lock.read_lock(REPO)
        self.assertRegex(lock["tag"], r"^v\d+\.\d+\.\d+$")
        self.assertRegex(lock["commit"], r"^[0-9a-f]{40}$")
        self.assertRegex(lock["manifest_sha256"], r"^[0-9a-f]{64}$")

    def test_kit_source_is_not_tracked(self):
        out = subprocess.run(["git", "ls-files", "vendor"], capture_output=True, text=True, cwd=REPO)
        if out.returncode == 0:
            self.assertEqual([f for f in out.stdout.split() if f != "vendor/ipe_web_kit.lock"], [])

    def test_deploy_never_publishes_the_kit(self):
        wf = (REPO / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8")
        self.assertIn("--exclude='vendor'", wf)

    def test_missing_kit_gives_install_instructions(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "vendor").mkdir()
            shutil.copy(REPO / "vendor" / "ipe_web_kit.lock", Path(tmp) / "vendor")
            r = run(tmp, "check")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not installed", r.stderr)
        self.assertIn("scripts/kit_lock.py sync --kit", r.stderr)


@unittest.skipUnless(INSTALLED, "ipe_web_kit not installed (python3 scripts/kit_lock.py sync --kit ~/Developer/ipe_web_kit)")
class KitInstalled(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        (self.tmp / "vendor").mkdir()
        shutil.copy(REPO / "vendor" / "ipe_web_kit.lock", self.tmp / "vendor")
        shutil.copytree(REPO / "vendor" / "ipe_web_kit", self.tmp / "vendor" / "ipe_web_kit")

    def test_installed_kit_is_the_locked_one(self):
        self.assertEqual(kit_lock.problems(REPO), [])

    def test_other_kit_than_locked_fails(self):
        self.assertEqual(kit_lock.problems(self.tmp), [])
        lock = self.tmp / "vendor" / "ipe_web_kit.lock"
        orig = lock.read_text()
        lock.write_text(re.sub(r"commit=[0-9a-f]{40}", "commit=" + "0" * 40, orig))
        self.assertTrue([p for p in kit_lock.problems(self.tmp) if "differs from the lock" in p])
        lock.write_text(re.sub(r"manifest_sha256=\w+", "manifest_sha256=" + "0" * 64, orig))
        self.assertTrue([p for p in kit_lock.problems(self.tmp) if "manifest hash" in p])

    def test_edited_kit_file_fails(self):
        with open(self.tmp / "vendor" / "ipe_web_kit" / "seo.py", "a", encoding="utf-8") as f:
            f.write("\n# tampered\n")
        self.assertTrue([p for p in kit_lock.problems(self.tmp) if "changed after install" in p])

    def test_localtime_copy_is_the_kit_asset(self):
        """build_journal.py inlines scripts/vendor/ipe-localtime.js; it must stay byte-identical to the kit's ipe-localtime v2."""
        ours = (REPO / "scripts" / "vendor" / "ipe-localtime.js").read_bytes()
        kit = (REPO / "vendor" / "ipe_web_kit" / "assets" / "ipe-localtime.js").read_bytes()
        self.assertEqual(hashlib.sha256(ours).hexdigest(), hashlib.sha256(kit).hexdigest())


if __name__ == "__main__":
    unittest.main()
