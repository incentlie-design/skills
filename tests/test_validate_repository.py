import importlib.util
import copy
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_repository", ROOT / "scripts/validate_repository.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class RepositoryValidationTests(unittest.TestCase):
    def test_current_repository_contract(self):
        report = validator.validate(ROOT)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["skills_checked"], 8)
        scenarios = validator.read_json(ROOT / "tests/routing_scenarios.json")["scenarios"]
        self.assertEqual(report["routing_scenarios_validated"], len(scenarios))
        self.assertEqual(report["behavior_cases_executed"], 0)

    def test_dependency_cycle_and_missing_are_rejected(self):
        errors = validator.dependency_errors({"a": ["b"], "b": ["a", "missing"]})
        self.assertTrue(any("cycle" in error for error in errors))
        self.assertTrue(any("missing dependency" in error for error in errors))

    def test_expected_dependency_dag_is_acyclic(self):
        self.assertEqual(validator.dependency_errors(validator.EXPECTED_DEPENDENCIES), [])

    def test_routing_allows_added_cases_and_unordered_or_empty_owner_sets(self):
        read_json = validator.read_json
        routing_path = ROOT / "tests/routing_scenarios.json"
        routing = copy.deepcopy(read_json(routing_path))
        for scenario in routing["scenarios"]:
            scenario["expected_route"].reverse()
        added = copy.deepcopy(routing["scenarios"][0])
        added.update(id="read-only-extra-case", expected_route=[])
        routing["scenarios"].append(added)
        with patch.object(validator, "read_json", side_effect=lambda path: routing if path == routing_path else read_json(path)):
            report = validator.validate(ROOT)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["routing_scenarios_validated"], len(routing["scenarios"]))

    def test_routing_still_rejects_missing_owner_coverage(self):
        read_json = validator.read_json
        routing_path = ROOT / "tests/routing_scenarios.json"
        routing = copy.deepcopy(read_json(routing_path))
        for scenario in routing["scenarios"]:
            scenario["expected_route"] = []
        with patch.object(validator, "read_json", side_effect=lambda path: routing if path == routing_path else read_json(path)):
            report = validator.validate(ROOT)
        self.assertIn("routing scenarios do not cover all five governance and decision Skills", report["errors"])

    def test_frontmatter_requires_one_name_and_description(self):
        parsed = validator.frontmatter("---\nname: eng-example-one\ndescription: bounded example\n---\nBody")
        self.assertEqual(parsed["name"], "eng-example-one")
        with self.assertRaises(ValueError):
            validator.frontmatter("---\nname: one\nname: two\ndescription: example\n---\n")

    def test_consolidated_cases_reject_empty_inputs_or_assertions(self):
        read_json = validator.read_json
        routing_path = ROOT / "tests/routing_scenarios.json"
        original = read_json(routing_path)
        for field, value in (("id", ""), ("request", " "), ("stop", None), ("expected_owner_actions", []), ("forbid", [])):
            with self.subTest(field=field):
                routing = copy.deepcopy(original)
                routing["scenarios"][0][field] = value
                with patch.object(validator, "read_json", side_effect=lambda path: routing if path == routing_path else read_json(path)):
                    report = validator.validate(ROOT)
                self.assertEqual(report["status"], "fail")
                self.assertLess(report["routing_scenarios_validated"], len(routing["scenarios"]))

    def test_consolidated_cases_reject_duplicate_ids_or_unknown_owners(self):
        read_json = validator.read_json
        routing_path = ROOT / "tests/routing_scenarios.json"
        original = read_json(routing_path)
        for invalid_owner in (False, True):
            with self.subTest(invalid_owner=invalid_owner):
                routing = copy.deepcopy(original)
                if invalid_owner:
                    routing["scenarios"][0]["expected_route"] = ["unknown-owner"]
                else:
                    routing["scenarios"].append(copy.deepcopy(routing["scenarios"][0]))
                with patch.object(validator, "read_json", side_effect=lambda path: routing if path == routing_path else read_json(path)):
                    report = validator.validate(ROOT)
                self.assertEqual(report["status"], "fail")


if __name__ == "__main__":
    unittest.main()
