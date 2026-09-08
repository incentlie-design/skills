---
name: eng-project-governance
description: Govern work from raw intake through canonical work items, requirement and architecture revisions, DAG planning, milestones, candidate selection, release windows, pipeline gates, and closure. Use task-system adapters; do not author implementation artifacts or perform Git mechanics.
---

# Project governance

Own delivery and release decisions without binding the workflow to one tracker, repository host, or agent runtime. The project or user profile supplies the release-selection owner.

## Required inputs

Start from raw intake or a resolvable `work_item_ref`. Require exactly one `system_of_record`, source references, current goal/architecture/task revisions, acceptance criteria, dependencies, project profile, and the authority relevant to any external write or release selection. Missing or conflicting source-of-record data stops at `needs_input` or `blocked`.

Read [work items and adapters](references/work-items-and-adapters.md) when normalizing intake, binding a task system, selecting candidates, opening a release window, or writing external state. Use only the project slice from [the shared governance contract](../../../docs/governance-contract.md).

## Decisions and workflow

1. Normalize raw intake into one canonical WorkItem. Preserve source evidence, unknowns, and the unique system of record; all other `source_refs` are links or mirrors.
2. Track goal, architecture, and task-DAG revisions plus acceptance criteria and their impact relationships. Request specialized producers or reviewers when those artifacts are missing; do not write or approve them here.
3. Derive bounded work packages, dependency order, milestones, and candidate criteria. Agent assignments may consume the WorkItem, but agent sessions do not become project state.
4. Select which eligible candidates enter a release target and when a release window opens. Record the selection owner, exact candidate refs, pipeline gates, and decision revision.
5. When multiple repositories participate, request the exact workspace slice from `eng-workspace-governance`. Route all Git mechanics to `eng-repo-governance` through that boundary.
6. Close only when acceptance, required gates, handoffs, and unresolved-risk decisions are recorded against current revisions.

Project governance orchestrates. It does not author product requirements or architecture, produce application code, execute or redefine tests, manage branches/worktrees, or create a second agent-state store.

## Output and stop

Return the project slice, canonical WorkItem reference, revision/AC/dependency map, milestone and candidate decisions, release-window/gate status, adapter evidence, unresolved items, and next owner. External sink writes require explicit authority and `expected_revision`; on conflict, stop and re-read instead of overwriting. A selected or gated candidate is not automatically integrated, published, or deployed.
