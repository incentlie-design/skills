"""Instance checks for the optional structured handoff; no runtime workflow is implied."""

import copy
import json
import unittest
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(Draft202012Validator, "optional jsonschema package is not installed")
class HandoffContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads((ROOT / "contracts/governance-handoff.schema.json").read_text())
        Draft202012Validator.check_schema(schema)
        cls.validator = Draft202012Validator(schema)

    def packet(self, **slices):
        return {"schema_version": 2, "handoff_id": "handoff:example", "slices": slices}

    def test_bounded_result_without_lifecycle_records(self):
        packet = self.packet(agent={"owner": "developer", "scope": ["src/parser.py"], "output_refs": ["artifact:parser-fix"]})
        self.validator.validate(packet)

    def test_project_decision_without_tracker_or_release(self):
        self.validator.validate(self.packet(project={"decision_ref": "request:scope-decision"}))

    def test_local_repo_evidence_without_integration_stages(self):
        repo = {"repo_id": "service", "base_commit": "a" * 40, "head_commit": "b" * 40, "write_scope": ["src/parser.py"]}
        self.validator.validate(self.packet(repo=repo))
        for field in ("base_commit", "head_commit"):
            incomplete = {key: value for key, value in repo.items() if key != field}
            with self.subTest(missing=field):
                self.assertFalse(self.validator.is_valid(self.packet(repo=incomplete)))

    def test_declared_budget_requires_unit_and_limit_not_invented_consumption(self):
        agent = {"owner": "reviewer", "scope": ["review"], "budget": {"unit": "minutes", "limit": 5}}
        self.validator.validate(self.packet(agent=agent))
        for budget in ({"limit": 5}, {"unit": "minutes"}, {"unit": "minutes", "limit": -1}, {"unit": "minutes", "limit": 5, "consumed": -1}):
            with self.subTest(budget=budget):
                self.assertFalse(self.validator.is_valid(self.packet(agent={**agent, "budget": budget})))

    def test_runtime_lifecycle_is_not_prescribed(self):
        self.validator.validate(self.packet(agent={"owner": "analyst", "scope": ["report"], "status": "partial-results"}))

    def test_missing_scope_or_owner_and_cross_slice_writes_are_rejected(self):
        for agent in ({"owner": "dev"}, {"scope": ["src/"]}, {"owner": "dev", "scope": []}, {"owner": "dev", "scope": ["src/"], "release_target": "production"}):
            with self.subTest(agent=agent):
                self.assertFalse(self.validator.is_valid(self.packet(agent=agent)))
        self.assertFalse(self.validator.is_valid(self.packet(runtime={"session_id": "s1"})))

    def test_workspace_tuple_requires_exact_state_fields(self):
        workspace = {"manifest_ref": "workspace:r1", "repo_refs": [{"repo_id": "api", "path": "repos/api", "remote": None, "role": "service", "default_ref": "main", "commit": "a" * 40}], "dependency_edges": []}
        self.validator.validate(self.packet(workspace=workspace))
        missing_commit = copy.deepcopy(workspace)
        del missing_commit["repo_refs"][0]["commit"]
        self.assertFalse(self.validator.is_valid(self.packet(workspace=missing_commit)))

    def test_legacy_packet_does_not_silently_change_meaning(self):
        packet = self.packet(agent={"owner": "dev", "scope": ["src/"]})
        packet["schema_version"] = 1
        self.assertFalse(self.validator.is_valid(packet))


if __name__ == "__main__":
    unittest.main()
