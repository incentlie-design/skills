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

## RemoteSyncPlan

Project governance owns the decision about whether remote synchronization is needed, which project branch roles or named refs participate, and at what trigger or time. Record that decision separately from Git execution:

```json
{
  "schema_version": 1,
  "plan_ref": "remote-sync:window-2026-09",
  "work_item_ref": "tracker:42",
  "decision_revision": "project-r8",
  "target_remote": "origin",
  "target_visibility": "public-approved",
  "branches": [
    {
      "branch_role": "stable",
      "branch_ref": "main",
      "reason": "publish the verified stable promotion",
      "trigger": "stable-gates-pass",
      "retention": "durable"
    }
  ],
  "exposure_review_refs": ["review:public-tree@r3"],
  "decision_owner": "release-owner",
  "status": "approved"
}
```

Select branches only for a concrete cross-machine handoff, PR, remote CI/review, release, recovery, or publication outcome defined by the project profile. Stable publication can be a profile default; integration, contributor/session, archive, and release branches remain conditional on their named need. An archive whose visibility or exposure review is unresolved is not added to the approved set.

The plan names project-level intent and branch identity, not Git commands. Repository governance resolves each entry against the repository profile and exact local commit, compares the expected remote revision, obtains push authority, and records execution evidence. It may reject a stale, ambiguous, or unsafe plan, but it must not add branches or choose a new synchronization time. A plan revision invalidates downstream execution evidence for the changed entries.
