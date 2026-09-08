import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_project", ROOT / "scripts/validate_project.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ProjectSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((ROOT / "project.yaml").read_text(encoding="utf-8"))

    def validate_changed(self, change):
        config = copy.deepcopy(self.config)
        change(config)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "project.yaml"
            path.write_text(json.dumps(config), encoding="utf-8")
            return validator.validate(ROOT, config_path=path)

    def test_canonical_project_binding_passes(self):
        report = validator.validate(ROOT)
        self.assertEqual(report["errors"], [])
        self.assertFalse((ROOT / "project.ymal").exists())

    def test_github_issues_uses_the_same_provider_neutral_schema(self):
        def select_github(config):
            config["task_space_id"] = "skill-creator-github"
            selected = config["task_system"]["selected_adapter"]
            selected.update(
                adapter_id="github-issues",
                binding="github-issues@skill-creator-github",
                profile_ref="runtime:skill-creator/github-issues",
            )
            config["task_system"]["system_of_record"]["adapter_binding"] = selected["binding"]

        report = self.validate_changed(select_github)
        self.assertEqual(report["errors"], [])

    def test_adapter_binding_must_be_the_unique_system_of_record(self):
        report = self.validate_changed(
            lambda config: config["task_system"]["system_of_record"].update(
                adapter_binding="other@space"
            )
        )
        self.assertTrue(any("one selected adapter binding" in error for error in report["errors"]))

    def test_provider_configuration_and_sensitive_fields_are_rejected(self):
        report = self.validate_changed(
            lambda config: config["task_system"]["selected_adapter"].update(
                config={"database": ".project/tasks.sqlite3", "api_token": "not-a-real-token"}
            )
        )
        self.assertTrue(any("unexpected property config" in error for error in report["errors"]))
        self.assertTrue(any("fields are forbidden" in error for error in report["errors"]))

    def test_profile_contract_and_source_capabilities_are_enforced(self):
        def change(config):
            selected = config["task_system"]["selected_adapter"]
            selected["profile_ref"] = "local-profile"
            selected["contract_version"] = 2
            selected["required_capabilities"].remove("resolve")
            selected["required_capabilities"].append("fetch")

        report = self.validate_changed(change)
        self.assertTrue(any("profile_ref" in error for error in report["errors"]))
        self.assertTrue(any("contract_version" in error for error in report["errors"]))
        self.assertTrue(any("items must be unique" in error for error in report["errors"]))
        self.assertTrue(any("requires ['resolve']" in error for error in report["errors"]))

    def test_schema_version_and_minimum_status_profile_are_enforced(self):
        def change(config):
            config["schema_version"] = 1
            del config["task_system"]["status_mapping"]["blocked"]

        report = self.validate_changed(change)
        self.assertTrue(any("schema_version" in error for error in report["errors"]))
        self.assertTrue(any("missing required property blocked" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
