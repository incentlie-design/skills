# Work items and task-system adapters

Read this reference when creating or resolving canonical project state, or before any task-system write.

## Canonical WorkItem

The following is a release-oriented example, not a startup form. Keep fields needed by the requested canonical operation and provider contract. Ordinary analysis or implementation does not require this record; do not fabricate architecture revisions, milestones, or a release target.

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

A `TaskSink` may expose `create`, `update`, `transition`, or `comment`. Every write request includes adapter binding, operation, payload, explicit authorization evidence, and `expected_revision`. For create, use the SDK’s `ABSENT_REVISION`; do not invent an existing object revision. The result records the new revision or a conflict. On conflict, re-read through `TaskSource`, assess impact, and request a new decision; never retry as a blind overwrite.

Adapters may be provided for local SQLite, Multica, GitHub Issues, GitLab Issues, Jira, or another Skill, plugin, or connector. Availability does not imply permission. Local files may serve as a source or sink only when the project profile declares them the system of record.

A provider read-before-write check is not necessarily atomic compare-and-set. When the transport lacks conditional writes, require a known single writer, re-read immediately before saving, verify afterward, and disclose the race boundary. An action requiring atomic conflict exclusion stays blocked if that guarantee is unavailable; never label a browser save as transactional CAS.

## Provider operation mapping

`project.yaml` selects an adapter id, stable binding, provider target, and adapter-contract version. Resolve each canonical operation through the selected mapping below; do not switch providers because another tool happens to be available.

| Canonical operation | `sqlite` SDK | `github-issues` plugin | `gitlab-issues` plugin |
| --- | --- | --- | --- |
| `resolve` | `TaskSource.resolve` | `search_issues`, then `issue_read(method=get)` | `list_work_items(types=[ISSUE])`, then `get_work_item` |
| `fetch` | `TaskSource.fetch` | `issue_read(method=get)` | `get_work_item` |
| `changes` | `TaskSource.changes` | `issue_read(method=get)` and `issue_read(method=get_comments)` | `get_work_item(include=[notes])` |
| `create` | `TaskSink.create` | `issue_write(method=create)` | `save_work_item(type_name=Issue)` |
| `update` | `TaskSink.update` | `issue_write(method=update)` | `save_work_item` with `work_item_iid` |
| `transition` | `TaskSink.transition` | `issue_write(method=update, state=...)` | `save_work_item(state=opened|closed)` |
| `comment` | `TaskSink.comment` | `add_issue_comment` | `save_note` |

The machine-readable copy and read-only `check_tools` helper are in [`task_adapters.mappings`](../../../../task_adapters/mappings.py). Provider tool names are matched within the selected plugin namespace. Before an operation, check that its mapped tools are exposed in the current environment. If not, report the missing mapped tool. An already available, authorized CLI, API or browser for the same canonical provider/target may perform the action if its actual revision/concurrency semantics meet the task; state the transport explicitly and verify the result. This is not a system-of-record migration and does not make `check_tools` pass. If no suitable transport exists, stop that operation and dependent work. Do not provision a client, install/authenticate a plugin, or create a local mirror merely to satisfy routing.

Plugin installation, authentication, accounts, and permissions remain in the Codex environment. SQLite storage location and initialization remain in its external SDK implementation. `project.yaml` contains neither. Project governance still owns which source is canonical, whether a mirror is desired, its direction, and any system-of-record migration decision.

## Revision and release rules

When an owned goal, architecture, task, acceptance, candidate, or release decision changes, preserve its relevant revision and assess which downstream inputs or evidence are affected. Do not suspend unrelated work or require a new project approval for every upstream edit. Evidence for a changed subject cannot be presented as current without rechecking or justified reuse. Artifact authors and reviewers retain their own correctness authority; this Skill records references and gate decisions.

Keep three dependency meanings distinct:

| Meaning | Project record | Repository consequence |
| --- | --- | --- |
| Definition/input | Exact source revision or immutable artifact locator | Consumers read the selected bytes. Git ancestry is optional unless the content itself must ship in that branch. |
| Code | Exact candidate that another candidate executes, imports, or extends | Repository governance preserves the required ancestry or declared combine order. |
| Promotion | Required decision, gate, or delivery ordering | Blocks the affected promotion action without rewriting contributor history. |

An exact proposal may be selected for explicitly authorized early analysis, feasibility work, or reversible implementation. This selection does not assert acceptance. The project derives promotability from the canonical decision and current evidence instead of synchronizing a `draft`, `speculative`, or `ready` flag across tasks, branches, and Sessions.

Use the next revision for a material change to the same goal, scope, acceptance, dependency, risk, or authority. Use a child WorkItem when a future slice can be assigned, accepted, deferred, or cancelled independently. Evidence-only edits and newly discovered future work do not automatically revise the current delivery.

Candidate selection answers what enters a target and when. Repository governance performs the resulting Git operations. A pipeline gate reports evidence against exact refs; closing a WorkItem still requires current acceptance and unresolved-risk decisions.

## RemoteSyncPlan

Project governance owns the decision about whether remote synchronization is needed, which project branch roles or named refs participate, and at what trigger or time. Record the intent distinctly from Git execution, in the existing request or project record; a separate file or actor is not required. This fuller example applies when a tracked release needs a structured plan (`work_item_ref` applies only when one exists):

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
