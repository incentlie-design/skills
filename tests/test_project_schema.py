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

    def test_adapter_binding_must_be_the_unique_system_of_record(self):
        report = self.validate_changed(
            lambda config: config["task_system"]["system_of_record"].update(
                adapter_binding="other@space"
            )
        )
        self.assertTrue(any("one selected adapter binding" in error for error in report["errors"]))

    def test_unknown_and_sensitive_connection_fields_are_rejected(self):
        report = self.validate_changed(
            lambda config: config["task_system"]["selected_adapter"]["config"].update(
                api_token="not-a-real-token"
            )
        )
        self.assertTrue(any("unexpected property api_token" in error for error in report["errors"]))
        self.assertTrue(any("fields are forbidden" in error for error in report["errors"]))

    def test_database_must_be_project_relative(self):
        report = self.validate_changed(
            lambda config: config["task_system"]["selected_adapter"]["config"].update(
                database="../tasks.sqlite3"
            )
        )
        self.assertTrue(any("project-relative" in error for error in report["errors"]))

    def test_version_and_minimum_status_profile_are_enforced(self):
        def change(config):
            config["schema_version"] = 2
            del config["task_system"]["status_mapping"]["blocked"]

        report = self.validate_changed(change)
        self.assertTrue(any("schema_version" in error for error in report["errors"]))
        self.assertTrue(any("missing required property blocked" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
