---
name: eng-project-governance
description: Govern work from raw intake through canonical work items, requirement and architecture revisions, DAG planning, milestones, candidate selection, release windows, pipeline gates, project remote-sync decisions, and closure. Use task-system adapters; do not author implementation artifacts or perform Git mechanics.
---

# Project governance

Own delivery and release decisions without binding the workflow to one tracker, repository host, or agent runtime. The project or user profile supplies the release-selection owner.

## Required inputs

Start from raw intake or a resolvable `work_item_ref`. Require exactly one `system_of_record`, source references, current goal/architecture/task revisions, acceptance criteria, dependencies, project profile, and the authority relevant to any external write, release selection, or remote-sync decision. When `project.yaml` selects a task adapter, also require a validated binding and a matching environment-injected dependency. When remote synchronization is in scope, require its purpose, target remote/visibility, candidate branch roles or refs, trigger or timing, retention needs, and decision owner. Missing or conflicting source-of-record or adapter-dependency data stops at `needs_input` or `blocked`.

Read [work items and adapters](references/work-items-and-adapters.md) when normalizing intake, binding a task system, selecting candidates, opening a release window, deciding project remote synchronization, or writing external state. Use only the project slice from [the shared governance contract](../../../docs/governance-contract.md).

## Decisions and workflow

1. When the project selects an adapter, validate the project binding and run the read-only dependency checker before adapter access. Treat `profile_ref` as an environment lookup reference; do not provision a database, authenticate a client, initialize a provider, or start a mirror.
2. Normalize raw intake into one canonical WorkItem. Preserve source evidence, unknowns, and the unique system of record; all other `source_refs` are links or mirrors.
3. Track goal, architecture, and task-DAG revisions plus acceptance criteria and their impact relationships. Request specialized producers or reviewers when those artifacts are missing; do not write or approve them here.
4. Derive bounded work packages, dependency order, milestones, and candidate criteria. Agent assignments may consume the WorkItem, but agent sessions do not become project state.
5. Select which eligible candidates enter a release target and when a release window opens. Record the selection owner, exact candidate refs, pipeline gates, and decision revision.
6. Decide whether remote synchronization is needed and, if so, create a `RemoteSyncPlan` naming only the project branch roles/refs, purpose, trigger or timing, target remote/visibility, retention, decision owner, and required approvals. Base the decision on an actual collaboration, CI, review, release, recovery, or publication need; local branch existence alone is not a reason.
7. When multiple repositories participate, request the exact workspace slice from `eng-workspace-governance`. Delegate every push and other Git mechanic to `eng-repo-governance`, which resolves the approved plan to exact refspecs and may reject unsafe or stale input but must not expand the selected set.
8. Close only when acceptance, required gates, handoffs, remote-sync decisions when applicable, and unresolved-risk decisions are recorded against current revisions.

Project governance orchestrates. It decides remote-sync intent, selected project branches, and timing, but does not author product requirements or architecture, produce application code, execute or redefine tests, manage branches/worktrees, construct refspecs, run Git commands, or create a second agent-state store.

## Output and stop

Return the project slice, canonical WorkItem reference, revision/AC/dependency map, milestone and candidate decisions, release-window/gate status, optional `remote_sync_plan_ref`, adapter evidence, unresolved items, and next owner. External sink writes require explicit authority and `expected_revision`; on conflict, stop and re-read instead of overwriting. A selected or gated candidate is not automatically integrated, synchronized, published, or deployed.
