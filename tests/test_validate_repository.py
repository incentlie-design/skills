import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_repository", ROOT / "scripts/validate_repository.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class RepositoryValidationTests(unittest.TestCase):
    def test_current_repository_contract(self):
        report = validator.validate(ROOT)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["skills_checked"], 8)
        self.assertEqual(report["behavior_cases_defined"], 18)
        self.assertEqual(report["routing_scenarios_validated"], 5)
        self.assertEqual(report["behavior_cases_executed"], 0)

    def test_dependency_cycle_and_missing_are_rejected(self):
        errors = validator.dependency_errors({"a": ["b"], "b": ["a", "missing"]})
        self.assertTrue(any("cycle" in error for error in errors))
        self.assertTrue(any("missing dependency" in error for error in errors))

    def test_expected_dependency_dag_is_acyclic(self):
        self.assertEqual(validator.dependency_errors(validator.EXPECTED_DEPENDENCIES), [])

    def test_frontmatter_requires_one_name_and_description(self):
        parsed = validator.frontmatter("---\nname: eng-example-one\ndescription: bounded example\n---\nBody")
        self.assertEqual(parsed["name"], "eng-example-one")
        with self.assertRaises(ValueError):
            validator.frontmatter("---\nname: one\nname: two\ndescription: example\n---\n")


if __name__ == "__main__":
    unittest.main()
