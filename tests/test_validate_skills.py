import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("validate_skills", Path(__file__).resolve().parents[1] / "scripts/validate_skills.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def test_drama_category_round_trip(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            name = "drama-example-writing"
            folder = root / "skills" / "drama" / name
            (folder / "tests").mkdir(parents=True)
            (folder / "SKILL.md").write_text(
                f'---\nname: {name}\ndescription: "Bounded drama fixture"\n---\nFixture.',
                encoding="utf-8")
            (folder / "skill.json").write_text(json.dumps({
                "schema_version": 1, "name": name, "version": "0.1.0",
                "category": "drama", "status": "draft", "summary": "fixture",
                "owners": ["fixture"], "tags": ["fixture"], "dependencies": [],
                "input_contract": "fixture input", "output_contract": "fixture output"
            }), encoding="utf-8")
            (folder / "tests/cases.json").write_text(json.dumps([
                {"id": kind, "kind": kind, "prompt": "fixture prompt",
                 "expect": ["observable result"]}
                for kind in ("happy", "missing_input", "boundary")
            ]), encoding="utf-8")
            (root / "registry.json").write_text(json.dumps({
                "schema_version": 1, "skills": [{
                    "name": name, "category": "drama",
                    "path": f"skills/drama/{name}", "dependencies": []
                }]
            }), encoding="utf-8")
            for doc in ("AGENTS.md", "README.md"):
                (root / doc).write_text(name, encoding="utf-8")
            report = validator.validate(root)
            self.assertEqual(report["errors"], [])
            self.assertEqual(report["skills_checked"], 1)
            self.assertEqual(report["behavior_cases_executed"], 0)

    def test_existing_category_prefixes_unchanged(self):
        self.assertEqual(
            {key: validator.PREFIXES[key] for key in
             ("meta", "personal", "engineering", "product", "content")},
            {"meta": "meta", "personal": "personal", "engineering": "eng",
             "product": "product", "content": "content"})

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

    def test_revision_is_not_commit_state_or_boolean(self):
        self.assertEqual(validator.revision_errors({"artifact_revision": 1, "base_commit": "uncommitted"}, "fixture"), [])
        for value in ("uncommitted", "r1", "1", True, 0):
            self.assertEqual(len(validator.revision_errors({"nested": [{"reviewed_revision": value}]}, "fixture")), 1)


if __name__ == "__main__":
    unittest.main()
