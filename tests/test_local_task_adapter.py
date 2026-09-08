import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from task_adapters import (
    ABSENT_REVISION,
    ConfigurationConflict,
    InvalidTransition,
    RevisionConflict,
    SQLiteTaskAdapter,
    TaskSink,
    TaskSource,
    WriteRequest,
)


STATUSES = {status: status for status in ("ready", "running", "blocked", "complete", "stopped")}
AUTHORIZATION = {"authority": "test-owner", "decision_ref": "test-r1"}


class LocalTaskAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.database = Path(self.temporary_directory.name) / "project" / "tasks.sqlite3"
        self.adapter = self.make_adapter()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def make_adapter(self, **overrides):
        arguments = {
            "database": self.database,
            "project_id": "skill-creator",
            "task_space_id": "skill-creator-local",
            "adapter_binding": "local-sqlite@skill-creator-local",
            "status_map": STATUSES,
        }
        arguments.update(overrides)
        return SQLiteTaskAdapter(**arguments)

    def request(self, operation, payload, expected_revision=ABSENT_REVISION):
        return WriteRequest(
            adapter_binding="local-sqlite@skill-creator-local",
            operation=operation,
            payload=payload,
            authorization_evidence=AUTHORIZATION,
            expected_revision=expected_revision,
        )

    def create(self, binding_key="intake-1", title="First task"):
        return self.adapter.create(
            self.request(
                "create",
                {"binding_key": binding_key, "fields": {"title": title, "status": "ready"}},
            )
        )

    def test_initialize_is_idempotent_and_binds_one_space(self):
        first = self.adapter.initialize()
        second = self.adapter.initialize()

        self.assertTrue(first.created)
        self.assertFalse(second.created)
        self.assertEqual(second.next_number, 1)
        self.assertIsInstance(self.adapter, TaskSource)
        self.assertIsInstance(self.adapter, TaskSink)

        conflicting = self.make_adapter(
            task_space_id="another-space",
            adapter_binding="local-sqlite@another-space",
        )
        with self.assertRaises(ConfigurationConflict):
            conflicting.initialize()

    def test_atomic_issuance_is_unique_under_concurrency(self):
        self.adapter.initialize()

        def issue(number):
            result = self.adapter.create(
                self.request(
                    "create",
                    {
                        "binding_key": f"intake-{number}",
                        "fields": {"title": f"Task {number}", "status": "ready"},
                    },
                )
            )
            return result.snapshot.source_evidence["external_id"]

        with ThreadPoolExecutor(max_workers=8) as pool:
            external_ids = list(pool.map(issue, range(16)))

        self.assertEqual(len(set(external_ids)), 16)
        self.assertEqual(
            set(external_ids), {f"TASK-{number:06d}" for number in range(1, 17)}
        )

    def test_duplicate_binding_returns_existing_task_without_write(self):
        self.adapter.initialize()
        created = self.create()
        duplicate = self.create(title="Must not overwrite")

        self.assertFalse(duplicate.applied)
        self.assertEqual(duplicate.outcome, "duplicate")
        self.assertEqual(duplicate.snapshot.work_item_ref, created.snapshot.work_item_ref)
        self.assertEqual(duplicate.revision, "r1")
        self.assertEqual(duplicate.snapshot.canonical_fields["title"], "First task")
        self.assertEqual(
            len(
                self.adapter.changes(
                    created.snapshot.work_item_ref, ABSENT_REVISION
                ).changes
            ),
            1,
        )

    def test_conflict_stops_and_carries_fresh_snapshot(self):
        self.adapter.initialize()
        created = self.create()
        work_item_ref = created.snapshot.work_item_ref
        updated = self.adapter.update(
            work_item_ref,
            self.request("update", {"fields": {"title": "Updated"}}, "r1"),
        )

        with self.assertRaises(RevisionConflict) as raised:
            self.adapter.transition(
                work_item_ref,
                self.request("transition", {"status": "running"}, "r1"),
            )

        self.assertEqual(raised.exception.current.revision, "r2")
        self.assertEqual(raised.exception.current.canonical_fields["title"], "Updated")
        self.assertEqual(updated.snapshot.canonical_fields["status"], "ready")
        self.assertEqual(self.adapter.fetch(work_item_ref).revision, "r2")

    def test_resolve_fetch_changes_comment_and_minimum_status_flow(self):
        self.adapter.initialize()
        created = self.create()
        work_item_ref = created.snapshot.work_item_ref
        external_id = created.snapshot.source_evidence["external_id"]

        resolved = self.adapter.resolve(external_id)
        running = self.adapter.transition(
            work_item_ref,
            self.request("transition", {"status": "running"}, resolved.revision),
        )
        commented = self.adapter.comment(
            work_item_ref,
            self.request("comment", {"body": "Ready for QA"}, running.revision),
        )
        complete = self.adapter.transition(
            work_item_ref,
            self.request("transition", {"status": "complete"}, commented.revision),
        )

        snapshot = self.adapter.fetch(work_item_ref)
        changes = self.adapter.changes(work_item_ref, "r1")
        self.assertEqual(resolved.work_item_ref, work_item_ref)
        self.assertEqual(snapshot.revision, "r4")
        self.assertEqual(snapshot.canonical_fields["status"], "complete")
        self.assertEqual(
            snapshot.canonical_fields["comments"][0]["body"], "Ready for QA"
        )
        self.assertEqual(
            [change.operation for change in changes.changes],
            ["transition", "comment", "transition"],
        )
        self.assertEqual(changes.current_revision, "r4")

        with self.assertRaises(InvalidTransition):
            self.adapter.transition(
                work_item_ref,
                self.request("transition", {"status": "invented"}, complete.revision),
            )
        self.assertEqual(self.adapter.fetch(work_item_ref).revision, "r4")


if __name__ == "__main__":
    unittest.main()
