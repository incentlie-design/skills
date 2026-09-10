import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/engineering/eng-repo-governance/scripts/writer.py"


@unittest.skipUnless(os.name == "posix", "POSIX foreground lock")
class WriterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("commit", "--allow-empty", "-m", "base")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.git("switch", "-c", "governance/req-31-test")

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, text=True, stderr=subprocess.DEVNULL)

    def command(self, *command, branch="governance/req-31-test", base=None):
        return [sys.executable, str(SCRIPT), "--branch", branch, "--base", base or self.base,
                "--owner", "test-writer", "--", *command]

    def execute(self, *command, cwd=None, **kwargs):
        return subprocess.run(self.command(*command, **kwargs), cwd=cwd or self.repo,
                              capture_output=True, text=True)

    def test_expected_branch_runs_and_propagates_failure(self):
        result = self.execute(sys.executable, "-c", "raise SystemExit(7)")
        self.assertEqual(result.returncode, 7)
        self.assertEqual(self.execute(sys.executable, "-c", "pass").returncode, 0)

    def test_wrong_stable_detached_moving_and_nonancestor_bases_reject_before_write(self):
        command = [sys.executable, "-c", "open('must-not-exist','w').write('bad')"]
        self.assertEqual(self.execute(*command, branch="feature/wrong").returncode, 2)
        self.assertEqual(self.execute(*command, base="HEAD").returncode, 2)
        self.git("switch", "--orphan", "unrelated")
        self.git("commit", "--allow-empty", "-m", "unrelated")
        unrelated = self.git("rev-parse", "HEAD").strip()
        self.git("switch", "governance/req-31-test")
        self.assertEqual(self.execute(*command, base=unrelated).returncode, 2)
        self.git("switch", "main")
        self.assertEqual(self.execute(*command, branch="main").returncode, 2)
        self.git("checkout", "--detach")
        self.assertEqual(self.execute(*command).returncode, 2)
        self.assertFalse((self.repo / "must-not-exist").exists())

    def test_same_worktree_excludes_writer_while_other_worktree_runs(self):
        other = self.root / "other"
        self.git("worktree", "add", "-b", "feature/req-31-other", str(other), self.base)
        # Blocking stdin gives the test a live handle and a deterministic exit,
        # without a timed sleep or relying on stale lock-file contents.
        child = subprocess.Popen(self.command(sys.executable, "-u", "-c",
                                  "import sys; print('locked', flush=True); sys.stdin.read()"),
                                 cwd=self.repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True)
        try:
            self.assertEqual(child.stdout.readline().strip(), "locked")
            rejected = self.execute(sys.executable, "-c", "open('unexpected','w').close()")
            self.assertEqual(rejected.returncode, 2)
            self.assertFalse((self.repo / "unexpected").exists())
            self.assertEqual(self.execute(sys.executable, "-c", "pass", cwd=other,
                                         branch="feature/req-31-other").returncode, 0)
        finally:
            child.communicate("", timeout=10)
        self.assertEqual(child.returncode, 0)
        self.assertEqual(self.execute(sys.executable, "-c", "pass").returncode, 0)

    def test_subdirectory_is_rejected(self):
        nested = self.repo / "nested"
        nested.mkdir()
        self.assertEqual(self.execute(sys.executable, "-c", "pass", cwd=nested).returncode, 2)


if __name__ == "__main__":
    unittest.main()
