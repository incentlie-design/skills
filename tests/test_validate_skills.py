import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("validate_skills", Path(__file__).resolve().parents[1] / "scripts/validate_skills.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def test_frontmatter_quoted(self):
        self.assertEqual(validator.frontmatter('---\nname: meta-test-one\ndescription: "Input: local files"\n---\nBody')["description"], "Input: local files")

    def test_frontmatter_rejects_ambiguous_yaml(self):
        with self.assertRaises(ValueError):
            validator.frontmatter("---\nname: test\ndescription: input: files\n---")

    def test_duplicate_key_rejected(self):
        with self.assertRaises(ValueError):
            validator.frontmatter("---\nname: one\nname: two\ndescription: example\n---")

    def test_dependency_cycle_and_missing(self):
        errors = validator.dependency_errors([{"name": "a", "dependencies": ["b"]}, {"name": "b", "dependencies": ["a", "missing"]}])
        self.assertTrue(any("cycle" in e for e in errors))
        self.assertTrue(any("missing dependency" in e for e in errors))

    def test_dependency_dag(self):
        self.assertEqual(validator.dependency_errors([{"name": "a", "dependencies": []}, {"name": "b", "dependencies": ["a"]}]), [])

    def test_path_containment(self):
        self.assertFalse(validator.within(Path("/tmp/repo-other/file"), Path("/tmp/repo")))
        self.assertTrue(validator.within(Path("/tmp/repo/file"), Path("/tmp/repo")))


if __name__ == "__main__":
    unittest.main()
