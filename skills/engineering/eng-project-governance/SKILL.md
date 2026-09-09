---
name: eng-project-governance
description: Constrain canonical work-item updates, scope and acceptance changes, dependency and milestone decisions, candidate selection, release gates, remote-sync intent, and project closure. Use for those project actions, not as a prerequisite to ordinary analysis or implementation.
---

# Project governance

Own project facts and delivery decisions, not the Agent's workflow orchestration. The Agent may combine capabilities in one task; this Skill does not require separate producers, approvers, Sessions, or a universal delivery pipeline. Use only the project slice from [the shared governance contract](../../../docs/governance-contract.md) when structured project evidence is needed.

Read [work items and adapters](references/work-items-and-adapters.md) for canonical task operations, revision decisions, release selection, or remote-sync intent. Require only facts needed by the action being performed.

## Registering or updating canonical work

- Preserve the user request, scope, observable acceptance, and material unknowns. A bounded request is sufficient input for work that needs no formal project-state change; do not create a WorkItem, DAG, architecture revision, milestone, or release target just to enable it.
- When registering or changing a WorkItem, resolve its single system of record and the selected adapter binding and target. Other sources remain evidence, not additional canonical writers. Do not silently create a mirror or switch providers.
- Check mapped tools for the required operation. An unavailable adapter blocks that operation and actions dependent on unavailable canonical facts, not unrelated authorized analysis or local work. Report the gap; do not claim the task was registered or closed.
- External sink writes require explicit authority and `expected_revision`. On conflict, re-read and reassess the affected decision; never retry as a blind overwrite. Do not provision storage, install or authenticate a plugin, or create a provider client from this Skill.

## Changing scope, dependencies, or acceptance

- Preserve the source and revision of the changed decision, its authority, and impact on applicable acceptance and dependent work. Do not invent missing revisions for artifacts that do not exist.
- Represent actual dependencies when decomposition is needed. A dependency describes a required input or constraint, not a required role-to-role or Session-to-Session hop.
- Evaluate changed context before invalidating evidence. A changed candidate head requires new or justified reusable evidence for that head; an unrelated planning revision does not automatically pause all work or require project reapproval.
- Artifact correctness remains with the appropriate author or reviewer capability. This ownership boundary does not require another person or Session unless independence or approval authority actually demands it.

## Selecting candidates, gates, or remote synchronization

- For a release or integration selection, identify the authorized target, exact candidates, actual dependency constraints, required gates, and selection authority. Record the decision against the relevant revisions. Do not create a release window or extra gates for ordinary local delivery.
- For a gate or completion claim, require current evidence for the applicable acceptance and unresolved-risk decisions. Planning, Session completion, and successful Git commands do not prove acceptance.
- For remote synchronization, record a `RemoteSyncPlan`: selected project refs or roles, concrete purpose, target remote/visibility, trigger or timing, retention, decision owner, and required approvals. A concise decision in existing context is sufficient; no new planning service or separate approving Agent is implied.
- Select remote refs only for an actual handoff, CI, review, release, recovery, or publication need. Local branch existence is not a reason. Route exact Git mechanics to `eng-repo-governance`; use `eng-workspace-governance` for participating cross-repository facts and dependencies.

## Evidence and boundaries

Report the project decision actually made, relevant references, evidence, and unresolved constraints. Structured handoffs contain only applicable project fields. Stop the action on ambiguous canonical state, stale required evidence, or missing authority; continue independent authorized work when safe. Selection, local integration, synchronization, publication, and deployment remain distinct. This Skill does not author delivery artifacts, run Git, redefine test semantics, or manage Session state.
