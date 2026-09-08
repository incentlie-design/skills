import json
import tempfile
import unittest
from pathlib import Path

from task_adapters import ABSENT_REVISION, SQLiteTaskAdapter, WriteRequest


ROOT = Path(__file__).resolve().parents[1]


class ProjectTaskLoopTests(unittest.TestCase):
    def test_project_binding_runs_one_complete_local_loop(self):
        config = json.loads((ROOT / "project.yaml").read_text(encoding="utf-8"))
        task_system = config["task_system"]
        selected = task_system["selected_adapter"]
        issuance = task_system["number_issuance"]

        with tempfile.TemporaryDirectory() as directory:
            adapter = SQLiteTaskAdapter(
                Path(directory) / selected["config"]["database"],
                project_id=config["project_id"],
                task_space_id=config["task_space_id"],
                adapter_binding=selected["binding"],
                status_map=task_system["status_mapping"],
                number_prefix=issuance["prefix"],
                number_width=issuance["width"],
                number_start=issuance["start"],
            )
            adapter.initialize()
            created = adapter.create(
                WriteRequest(
                    adapter_binding=selected["binding"],
                    operation="create",
                    payload={
                        "binding_key": "raw-intake:project-task-adapter-bootstrap",
                        "fields": {"title": "Adapter bootstrap", "status": "ready"},
                    },
                    authorization_evidence={"owner": "user", "decision": "goal-r1"},
                    expected_revision=ABSENT_REVISION,
                )
            )
            transitioned = adapter.transition(
                created.snapshot.work_item_ref,
                WriteRequest(
                    adapter_binding=selected["binding"],
                    operation="transition",
                    payload={"status": "complete"},
                    authorization_evidence={"owner": "PIC", "decision": "tasks-r1"},
                    expected_revision=created.revision,
                ),
            )

            self.assertEqual(
                adapter.resolve("TASK-000001").work_item_ref,
                created.snapshot.work_item_ref,
            )
            self.assertEqual(transitioned.revision, "r2")
            self.assertEqual(transitioned.snapshot.canonical_fields["status"], "complete")
            self.assertEqual(
                [change.operation for change in adapter.changes(created.snapshot.work_item_ref, ABSENT_REVISION).changes],
                ["create", "transition"],
            )


if __name__ == "__main__":
    unittest.main()
