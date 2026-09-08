import json
import unittest
from pathlib import Path

from task_adapters import (
    TASK_ADAPTER_CONTRACT_VERSION,
    AdapterDependency,
    DependencyUnavailable,
    check_dependency,
    require_dependency,
)


ROOT = Path(__file__).resolve().parents[1]


class DummyAdapter:
    def resolve(self, external_id):
        return None

    def fetch(self, work_item_ref):
        return None

    def changes(self, work_item_ref, since_revision):
        return None

    def create(self, request):
        return None

    def update(self, work_item_ref, request):
        return None

    def transition(self, work_item_ref, request):
        return None

    def comment(self, work_item_ref, request):
        return None


class TaskAdapterDependencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((ROOT / "project.yaml").read_text(encoding="utf-8"))
        cls.selected = cls.config["task_system"]["selected_adapter"]

    def dependency(self, **changes):
        adapter = DummyAdapter()
        values = {
            "adapter_id": self.selected["adapter_id"],
            "binding": self.selected["binding"],
            "profile_ref": self.selected["profile_ref"],
            "contract_version": TASK_ADAPTER_CONTRACT_VERSION,
            "capabilities": frozenset(self.selected["required_capabilities"]),
            "source": adapter,
            "sink": adapter,
        }
        values.update(changes)
        return AdapterDependency(**values)

    def test_matching_environment_dependency_is_returned(self):
        dependency = self.dependency()
        self.assertTrue(check_dependency(self.config, dependency).ok)
        self.assertIs(require_dependency(self.config, dependency), dependency)

    def test_missing_dependency_reports_the_selected_runtime_profile(self):
        check = check_dependency(self.config, None)
        self.assertFalse(check.ok)
        self.assertTrue(any(self.selected["profile_ref"] in error for error in check.errors))
        with self.assertRaises(DependencyUnavailable):
            require_dependency(self.config, None)

    def test_identity_availability_and_capability_mismatches_are_reported(self):
        check = check_dependency(
            self.config,
            self.dependency(
                adapter_id="github-issues",
                binding="github-issues@other",
                profile_ref="runtime:other/github-issues",
                contract_version=2,
                capabilities=frozenset({"resolve"}),
                available=False,
                detail="profile is not configured",
                source=None,
                sink=None,
            ),
        )
        self.assertFalse(check.ok)
        self.assertTrue(any("adapter_id" in error for error in check.errors))
        self.assertTrue(any("contract_version" in error for error in check.errors))
        self.assertTrue(any("unavailable" in error for error in check.errors))
        self.assertTrue(any("missing capabilities" in error for error in check.errors))

    def test_declared_capabilities_require_structural_interfaces(self):
        check = check_dependency(self.config, self.dependency(source=None, sink=None))
        self.assertFalse(check.ok)
        self.assertTrue(any("TaskSource" in error for error in check.errors))
        self.assertTrue(any("TaskSink" in error for error in check.errors))

    def test_core_contains_no_provider_runtime(self):
        self.assertFalse((ROOT / "task_adapters/sqlite.py").exists())


if __name__ == "__main__":
    unittest.main()
