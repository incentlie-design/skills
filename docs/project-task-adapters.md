# Project task-system binding and adapters

[`project.yaml`](../project.yaml) is the one project-level task-system binding. The intake spelling `project.ymal` was normalized to the conventional `project.yaml`; no alias is provided. `eng-project-governance` owns the configuration schema, semantics, version decisions, and validation rules. The file configures project identity and adapter behavior; it is not a WorkItem store and must never hold Session, Agent, lease, credential, or personal connection state.

## Bounded file format

The canonical file uses **JSON-compatible YAML**: one UTF-8 JSON object, which is also a YAML 1.2 document. Comments, anchors, aliases, tags, multiple documents, and YAML-only scalar syntax are outside this bounded format. This lets the standard-library validator parse the file deterministically without adding a YAML dependency.

Run:

```sh
python3 scripts/validate_project.py
```

The validator applies [`project.schema.json`](../contracts/project.schema.json), rejects unknown fields, verifies the adapter/system-of-record binding, requires a project-relative SQLite path, and rejects credential or personal-connection keys.

## Configuration semantics

| Field | Meaning |
| --- | --- |
| `project_id` | Stable project identity. Renaming a directory does not change it. |
| `task_space_id` | Stable namespace for task numbers and WorkItem references. It must not be reused by a different task authority. |
| `selected_adapter` | Exactly one adapter binding. `binding` is `<adapter_id>@<task_space_id>`; only its project-relative database location is configured. |
| `number_issuance` | The adapter allocates the next number atomically. With the supplied profile, number 1 becomes `TASK-000001`. |
| `work_item_binding` | One external task binds to one stable `local:{task_space_id}:{external_id}` WorkItem reference. A repeat returns a non-applied `duplicate` result with the current snapshot; a conflicting binding is rejected. |
| `system_of_record` | A single object naming the selected binding. Other references are evidence or mirrors, never a second write authority. Migration to another binding requires an explicit project decision with source and target revisions. |
| `revision_policy` | Create uses `expected_revision="absent"`; every other write requires `rN`. A mismatch returns a conflict with a fresh snapshot, after which the caller re-reads, assesses impact, and stops until a new decision—never blind retry. |
| `status_mapping` | The project profile's minimal WorkItem mapping: `ready`, `running`, `blocked`, `complete`, and `stopped`. The adapter accepts configured targets but adds no transition graph or project state machine. |

The status names configure WorkItem translation only. They do not store or control the similarly named Agent lifecycle; Agent state remains owned by `eng-agent-governance` through the [governance contract](governance-contract.md).

## Provider-neutral adapter contract

The contract follows the existing [WorkItem and adapter reference](../skills/engineering/eng-project-governance/references/work-items-and-adapters.md). A source is read-only:

- `resolve(external_id) -> ResolveResult(work_item_ref, revision)`
- `fetch(work_item_ref) -> TaskSnapshot(canonical_fields, revision, source_evidence)`
- `changes(work_item_ref, since_revision) -> ChangeSet(changed_fields, current_revision)`

A sink exposes the smallest mutation set:

- `create(request) -> WriteResult`
- `update(work_item_ref, request) -> WriteResult`
- `transition(work_item_ref, request) -> WriteResult`
- `comment(work_item_ref, request) -> WriteResult`

Every sink call receives an immutable `WriteRequest(adapter_binding, operation, payload, authorization_evidence, expected_revision)`. The operation must match the invoked method and binding must match `project.yaml`. Success returns the applied result and new revision. Duplicate create returns a non-applied `duplicate` result plus the current snapshot. Revision mismatch returns a conflict carrying a fresh snapshot; the caller must treat it as a read-and-decide boundary.

Canonical task data stays provider-neutral: stable `work_item_ref`, the unique `system_of_record`, source references/evidence, goal/architecture/task revisions, acceptance criteria, dependencies, milestones, candidate references, release target, status, and adapter revision. The local adapter may persist its own task and change records, but it must not recreate project candidate/release state, repository mechanics, or Agent sessions.

## Version evolution

There are two independent revisions:

- `schema_version` identifies the configuration contract. Version 1 rejects unknown fields. Any removal, rename, type change, required-field change, or semantic reinterpretation requires a new integer schema version, a new schema, and an explicit migration decision. Consumers must reject an unsupported version rather than guess.
- `config_revision` identifies edits to one project instance. Increment `project-config-rN` for any binding, identity, numbering, status, or storage-location change. Changing the adapter or task-space identity is a system-of-record migration, not an in-place cosmetic edit.

Backward-compatible documentation clarifications do not change the schema version. Adding an optional field may remain within a version only after the owner updates the schema, validator, examples, and compatibility tests together. Adapter database migrations are versioned by the adapter and do not turn `project.yaml` into task state.

The first implementation deliberately includes only the standard-library SQLite adapter. A GitHub Issues adapter is deferred until remote collaboration or hosted review creates evidence for it; Jira and a second local storage model are outside this candidate.
