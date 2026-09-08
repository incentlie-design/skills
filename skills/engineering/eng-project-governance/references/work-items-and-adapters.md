# Work items and task-system adapters

Read this reference when creating or resolving canonical project state, or before any task-system write.

## Canonical WorkItem

```json
{
  "schema_version": 1,
  "work_item_ref": "tracker:42",
  "system_of_record": {
    "adapter_id": "tracker-primary",
    "external_id": "42",
    "revision": "etag-7"
  },
  "source_refs": [
    {"adapter_id": "notes-mirror", "external_id": "launch-note", "relation": "mirror"}
  ],
  "goal_revision": "goal-r2",
  "architecture_revision": "arch-r4",
  "task_revision": "tasks-r6",
  "acceptance_criteria": ["AC-001: observable outcome"],
  "dependencies": ["tracker:17"],
  "milestones": ["candidate-ready"],
  "candidate_refs": ["candidate:api@0123456"],
  "release_target": "window-2026-09",
  "status": "ready"
}
```

One WorkItem has exactly one `system_of_record`. Other references are evidence, relationships, imports, or mirrors and never gain write authority by being listed. A system-of-record migration is an explicit project decision with source and target revisions; it is not a silent adapter switch.

The project profile supplies status vocabulary or mapping, release-selection owner, gate names, and milestone policy. The Skill records decisions without imposing one vendor's states.

## Adapter contract

A `TaskSource` is read-only:

- `resolve(external_id) -> work_item_ref, revision`
- `fetch(work_item_ref) -> canonical fields, revision, source evidence`
- `changes(work_item_ref, since_revision) -> changed fields, current revision`

A `TaskSink` may expose `create`, `update`, `transition`, or `comment`. Every write request includes adapter binding, operation, payload, explicit authorization evidence, and `expected_revision`. The result records the new revision or a conflict. On conflict, re-read through `TaskSource`, assess impact, and request a new decision; never retry as a blind overwrite.

Adapters may be provided for local SQLite, Multica, GitHub Issues, GitLab Issues, Jira, or another Skill, plugin, or connector. Availability does not imply permission. Local files may serve as a source or sink only when the project profile declares them the system of record.

## Revision and release rules

Changes to goal, architecture, task DAG, acceptance criteria, candidate set, or release target create a new owned revision and mark dependent decisions/evidence stale unless an impact record says otherwise. Artifact authors and reviewers retain their own correctness authority; this Skill only records references and gate decisions.

Candidate selection answers what enters a target and when. Repository governance performs the resulting Git operations. A pipeline gate reports evidence against exact refs; closing a WorkItem still requires current acceptance and unresolved-risk decisions.
