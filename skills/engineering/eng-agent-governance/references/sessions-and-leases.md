# Sessions, assignments, and ownership leases

Read this reference when an agent is assigned, replaced, blocked, handed off, or closed.

## Capability profile

A capability profile defines responsibilities, required independence, allowed actions, and evidence—not a fixed product role. Common labels include:

- PIC: owns coordination, dependency visibility, escalation, and final closure accounting.
- DEV: owns bounded implementation output, not its own final independent acceptance.
- Spec: owns the requested specification artifact, not release selection.
- QA: owns independent execution/evidence within an existing test contract; it does not redefine test semantics.
- Reviewer: owns an independent decision for a declared review scope and revision.

One session may hold multiple compatible capabilities only when the WorkItem permits it and no self-review boundary is violated.

## Session title and status synchronization

Treat a display title as a synchronized projection, not the canonical lifecycle or repository record. Use this field order and delimiter:

```text
<role> · <status> · <branch-phase> · <requirement>
```

- `role` is one no-space capability token from the assignment profile, such as `PIC`, `DEV`, `QA`, or `Reviewer`. Combine roles only when the assignment permits it and independence remains valid.
- `status` is exactly one of `🔵 running`, `🟡 waiting`, `🔴 blocked`, or `🟢 completed`. `running` means execution is active. `waiting` means no execution is active while a named event is pending; never use it as a substitute for `running`.
- `branch-phase` is exactly `dev`, `test`, `mr`, or `merged`. It reports repository delivery progress independently of session status: `dev` is implementation, `test` is a frozen candidate under validation, `mr` has an opened but unmerged PR or MR, and `merged` requires observed integration of the exact candidate. Conflicts, review waits, and failed checks remain `mr` and are reported separately.
- `requirement` is the stable, concise WorkItem name. It is one line and must not contain the `·` delimiter.

The machine-readable grammar is:

```regex
^([A-Za-z][A-Za-z0-9-]*) · (🔵 running|🟡 waiting|🔴 blocked|🟢 completed) · (dev|test|mr|merged) · ([^·\r\n]+)$
```

Project the lifecycle states into titles without creating a second state machine: `running` maps to `🔵 running`; a `ready` or `handoff` session with a named pending event maps to `🟡 waiting`; `blocked` maps to `🔴 blocked`; and `complete` maps to `🟢 completed`. Never relabel `stopped` as completed; record its closure and remove or archive it from the active-session inventory.

Normal title transitions are `waiting -> running`, `running -> waiting | blocked | completed`, and `blocked -> running | waiting`. `completed` is terminal for that assignment. Branch phase normally advances `dev -> test -> mr -> merged`; rework after a PR or MR opens remains `mr`, while a discarded candidate starts a new assignment and branch at `dev`.

The session owner updates the title when execution starts, pauses, blocks, or closes. The repository owner supplies exact branch evidence, and the PIC reconciles the active-session list at assignment and handoff boundaries. A title update does not grant either owner authority over the other's state.

If any field cannot be verified, do not manufacture a replacement title. Keep the last verified title and mark the synchronization record `unverified`; mark it `stale` after an underlying lifecycle, branch, or PR/MR event occurs later than its `verified_at`. A minimal synchronization record contains `session_id`, `title`, `owner`, lifecycle evidence, `branch_evidence_ref`, `verified_at`, and `sync_status`. Refresh stale or unverified records before using them for a handoff or status claim.

## Assignment record

```json
{
  "assignment_id": "assignment-17",
  "work_item_ref": "tracker:42",
  "adapter_binding": "tracker-primary",
  "role": "DEV",
  "session_id": "session-9",
  "owner": "contributor-a",
  "capabilities": ["implementation"],
  "context_revisions": ["goal-r2", "arch-r4", "tasks-r6"],
  "read_scope": ["specs/"],
  "write_scope": ["src/component/"],
  "acceptance_criteria": ["AC-001"],
  "budget": {"unit": "minutes", "limit": 60},
  "leases": ["path:src/component"],
  "stop_conditions": ["AC complete", "blocked", "budget exhausted"],
  "forbidden_actions": ["external write", "Git cleanup"]
}
```

Context references bind the assignment to exact upstream revisions. If a relevant revision changes, pause and ask project governance whether the assignment remains valid.

## Lease rules

A lease has a resource id, owner/session, start, expiry or review point, and release status. Claim it before writing; reject overlapping exclusive leases. Lease renewal is an explicit lifecycle event and must not hide a blocked or abandoned session.

A lease is not an authorization token. Repository paths still follow repository governance; task records follow project governance; external tools keep their own permissions.

## Blocking, handoff, and closure

Blocked output states the observed blocker, attempted in-scope checks, affected AC, remaining budget, clean/dirty resources, and the owner who can decide. Do not recursively create replacement sessions without project/PIC authority.

A handoff includes actual artifacts/evidence, current context revisions, status, remaining work, known risks, budget consumed, clean/dirty report, and every released or transferred lease. The agent slice records the lifecycle summary; project and repository slices remain owned elsewhere.

The closure owner verifies that the handoff exists and leases are released even when work is stopped or abandoned. Repository cleanup is only a proposal until `eng-repo-governance` accepts the exact target and authority.
