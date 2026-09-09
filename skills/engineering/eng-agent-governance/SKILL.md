---
name: eng-agent-governance
description: Govern agent capabilities, independent roles, sessions, assignments, ownership leases, context, budgets, stopping, blocking, handoffs, and closure. Use a project-selected work-item adapter; do not create task state, Git policy, or test semantics.
---

# Agent governance

Own the lifecycle and accountability of a bounded agent assignment. “Agent” means any delegated execution unit; labels such as PIC, DEV, QA, Spec, and Reviewer are profile-defined capability roles, not assumptions about a particular runtime or organization.

## Required inputs

Require a `work_item_ref`, project-selected adapter binding, role/capability profile, session binding and owner, read/write and closure scope, optional parent assignment, context revisions, acceptance criteria, budget, independence constraints, lease targets, stop conditions, and forbidden actions. If the WorkItem, authority, ownership, or budget is missing, do not start the assignment.

Read [sessions, assignments, and leases](references/sessions-and-leases.md) when creating or closing an assignment or resolving a conflict. Use only the agent slice from [the shared governance contract](../../../docs/governance-contract.md).

## Decisions and workflow

1. Match required capabilities to a role profile. A PIC coordinates closure and may coordinate another PIC for a distinct or nested closure scope; each scope has one closure owner, the coordination relation is acyclic, and it transfers no permission or approval authority. DEV implements within scope; Spec produces or revises specification artifacts; QA or Reviewer supplies the declared independent evidence.
2. Resolve whether each requested assignment reuses an existing session or creates a new one. Adding an assignment leaves the current assignment, session, and display title unchanged unless the user explicitly requests a change; a title change is not an assignment or session change.
3. Create one assignment and session with explicit owner, optional parent assignment, closure scope, WorkItem reference, adapter binding, context revisions, inputs, outputs, write scope, budget, acceptance, stop, and forbidden actions.
4. Claim time-bounded ownership leases only for the declared resources. Detect overlap before work. A lease grants coordination ownership, not new filesystem, network, Git, tracker, or production permission.
5. Track session state as `ready`, `running`, `blocked`, `handoff`, `complete`, or `stopped`. Project status remains in the project-selected system of record and is only read or requested through its adapter.
6. On success, budget exhaustion, blocked state, replacement, or stop, produce a handoff, report clean/dirty resource state, release leases, and name the closure owner. Do not leave ownership implied by an ended session.

Use `eng-project-governance` for WorkItem transitions or task-system writes. Use `eng-repo-governance` for branches, worktrees, commits, merges, or cleanup. QA independence here does not select test layers or change pass/fail semantics.

## Output and stop

Return the agent slice, assignment/session references, capability and independence decision, consumed budget, status, produced artifact/handoff refs, released leases, clean/dirty report, unresolved blockers, and closure owner. Stop at the declared condition or budget. An agent may propose cleanup or status transition, but the owning governance boundary must authorize and perform it.
