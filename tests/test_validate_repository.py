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
        self.assertEqual(report["engineering_skills_checked"], 10)
        self.assertGreaterEqual(report["content_skills_checked"], 1)
        self.assertEqual(
            report["skills_checked"],
            report["engineering_skills_checked"] + report["content_skills_checked"],
        )
        self.assertGreater(report["content_index_entries"], 0)
        self.assertLessEqual(report["content_index_entries"], 200)
        scenarios = validator.read_json(ROOT / "tests/routing_scenarios.json")["scenarios"]
        self.assertEqual(report["routing_scenarios_validated"], len(scenarios))
        examples = validator.read_json(ROOT / "tests/review_handoff_examples.json")["examples"]
        self.assertEqual(report["review_handoff_examples_validated"], len(examples))
        self.assertEqual(report["behavior_cases_executed"], 0)

    def test_review_handoff_examples_enforce_information_priority(self):
        payload = validator.read_json(ROOT / "tests/review_handoff_examples.json")
        errors, validated = validator.review_handoff_example_errors(payload)
        self.assertEqual(errors, [])
        self.assertEqual(validated, len(payload["examples"]))

        reordered = copy.deepcopy(payload)
        sections = reordered["examples"][1]["sections"]
        sections[3], sections[4] = sections[4], sections[3]
        errors, _ = validator.review_handoff_example_errors(reordered)
        self.assertTrue(any("precedes the required decision path" in error for error in errors))

    def test_review_handoff_examples_allow_short_clean_without_empty_ledger(self):
        payload = validator.read_json(ROOT / "tests/review_handoff_examples.json")
        clean = next(example for example in payload["examples"] if example["material_findings_count"] == 0)
        self.assertEqual(
            [section["kind"] for section in clean["sections"]],
            ["exact_subject", "conclusion", "required_action"],
        )

        invalid = copy.deepcopy(payload)
        invalid["examples"][0]["sections"].append({"kind": "decision_ledger", "content": ""})
        errors, _ = validator.review_handoff_example_errors(invalid)
        self.assertTrue(any("empty content" in error for error in errors))

        missing_action = copy.deepcopy(payload)
        missing_action["examples"][0]["sections"].pop()
        errors, _ = validator.review_handoff_example_errors(missing_action)
        self.assertTrue(any("needs a required decision or action" in error for error in errors))

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
        self.assertIn("routing scenarios do not cover all governance and advisory Skills", report["errors"])

    def test_frontmatter_requires_one_name_and_description(self):
        parsed = validator.frontmatter("---\nname: eng-example-one\ndescription: bounded example\n---\nBody")
        self.assertEqual(parsed["name"], "eng-example-one")
        with self.assertRaises(ValueError):
            validator.frontmatter("---\nname: one\nname: two\ndescription: example\n---\n")

    def test_frontmatter_rejects_unquoted_mapping_colon(self):
        with self.assertRaises(ValueError):
            validator.frontmatter(
                "---\nname: content-example\ndescription: visual identity: face and wardrobe\n---\nBody\n"
            )

    def test_frontmatter_accepts_quoted_mapping_colon(self):
        parsed = validator.frontmatter(
            '---\nname: content-example\ndescription: "visual identity: face and wardrobe"\n---\nBody\n'
        )
        self.assertEqual(parsed["description"], "visual identity: face and wardrobe")

    def test_content_io_catalog_covers_every_content_skill(self):
        report = validator.validate(ROOT)
        self.assertEqual(report["errors"], [])
        skills = validator.read_json(ROOT / "skills/content/io/skills.json")["skills"]
        roles = validator.read_json(ROOT / "skills/content/io/roles.json")["roles"]
        self.assertEqual(len(skills), report["content_skills_checked"])
        self.assertEqual(set(roles), {"story_director", "visual_director", "audio_director", "editor", "validator", "producer"})
        for alias in ("NovelAgent", "DirectorAgent"):
            self.assertTrue(any(alias in body.get("aliases", []) for body in roles.values()))

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
