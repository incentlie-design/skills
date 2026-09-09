---
name: eng-agent-governance
description: Govern agent capabilities, independent roles, sessions, assignments, ownership leases, context, budgets, stopping, blocking, handoffs, and closure. Use a project-selected work-item adapter; do not create task state, Git policy, or test semantics.
---

# Agent governance

Own the lifecycle and accountability of a bounded agent assignment. “Agent” means any delegated execution unit; labels such as PIC, DEV, QA, Spec, and Reviewer are profile-defined capability roles, not assumptions about a particular runtime or organization.

## Required inputs

Require a `work_item_ref`, project-selected adapter binding, role/capability profile, session and owner, read/write scope, context revisions, acceptance criteria, budget, independence constraints, lease targets, stop conditions, and forbidden actions. If the WorkItem, authority, ownership, or budget is missing, do not start the assignment.

Read [sessions, assignments, and leases](references/sessions-and-leases.md) when creating, naming, synchronizing, or closing an assignment, or when resolving a conflict. Use only the agent slice from [the shared governance contract](../../../docs/governance-contract.md).

## Decisions and workflow

1. Match required capabilities to a role profile. A PIC coordinates closure; DEV implements within scope; Spec produces or revises specification artifacts; QA or Reviewer supplies the declared independent evidence. These labels may be renamed or combined only when independence requirements still hold.
2. Create one assignment and session with explicit owner, WorkItem reference, adapter binding, context revisions, inputs, outputs, write scope, budget, acceptance, stop, and forbidden actions.
3. Claim time-bounded ownership leases only for the declared resources. Detect overlap before work. A lease grants coordination ownership, not new filesystem, network, Git, tracker, or production permission.
4. Track session state as `ready`, `running`, `blocked`, `handoff`, `complete`, or `stopped`. Project status remains in the project-selected system of record and is only read or requested through its adapter.
5. On success, budget exhaustion, blocked state, replacement, or stop, produce a handoff, report clean/dirty resource state, release leases, and name the closure owner. Do not leave ownership implied by an ended session.

Use `eng-project-governance` for WorkItem transitions or task-system writes. Use `eng-repo-governance` for branches, worktrees, commits, merges, or cleanup. QA independence here does not select test layers or change pass/fail semantics.

## Output and stop

Return the agent slice, assignment/session references, capability and independence decision, consumed budget, status, produced artifact/handoff refs, released leases, clean/dirty report, unresolved blockers, and closure owner. Stop at the declared condition or budget. An agent may propose cleanup or status transition, but the owning governance boundary must authorize and perform it.
