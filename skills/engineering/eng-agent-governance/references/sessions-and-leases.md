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
