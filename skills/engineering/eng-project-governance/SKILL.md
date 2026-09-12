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

## Starting from a ticket with no prior context

- Read the canonical ticket and its selected decision/evidence links before loading broad project history. Resolve scope/revision, human decision owner, current authorization, exact inputs, output paths, applicable checks and next action. Missing unrelated stage/release data is not a startup gate.
- Keep mutable scope and decisions in that ticket. Derive branch, PR, CI and executor facts from their native systems; use immutable comments or existing reports for candidate/test evidence. A new commit or test run needs a distinguishable evidence reference, not automatically a new task or lifecycle.
- A freeze is a one-way snapshot of exact ticket bytes and required inputs. Do not copy lifecycle, blockers or closure into a writable mirror, or include the resulting planning commit in its own hash input. Record the resulting commit in the canonical ticket after freezing.
- Fetch availability and ancestry do not prove an input is still accepted: inspect later decisions, reverts and relevant content changes before adopting an old candidate.

## Changing scope, dependencies, or acceptance

- Preserve the source and revision of the changed decision, its authority, and impact on applicable acceptance and dependent work. Do not invent missing revisions for artifacts that do not exist.
- Classify actual dependencies when decomposition is needed: a definition/input reference selects exact meaning, a code dependency selects an implementation that must be consumed, and a promotion dependency constrains ordering or gates. A dependency is not a required role-to-role or Session-to-Session hop. Do not force definition or promotion dependencies into Git ancestry.
- Evaluate changed context before invalidating evidence. A changed candidate head requires new or justified reusable evidence for that head; an unrelated planning revision does not automatically pause all work or require project reapproval.
- Explicit authority may allow bounded analysis, probes, or reversible implementation from an exact proposal before its acceptance. Keep promotion blocked until the canonical decision accepts the applicable input and evidence. Derive this boundary from the canonical record; do not add a copied `speculative` status.
- For an Architecture conflict, canonically record the `eng-closed-loop-decisions`
  result, owner, candidate admission, and promotion condition. Invalidate only
  dependent evidence/actions; do not copy it into parallel trackers.
- Revise the current WorkItem when its goal, scope, acceptance, dependency, risk, or authority changes. Create a lightweight child WorkItem when a discovered future slice has independently actionable scope and acceptance. Do not turn every later milestone into another revision of the active delivery.
- Artifact correctness remains with the appropriate author or reviewer capability. This ownership boundary does not require another person or Session unless independence or approval authority actually demands it.

## Selecting candidates, gates, or remote synchronization

- For a release or integration selection, identify the authorized target, exact candidates, actual dependency constraints, required gates, and selection authority. Record the decision against the relevant revisions. Do not create a release window or extra gates for ordinary local delivery.
- For a gate or completion claim, require current evidence for the applicable acceptance and unresolved-risk decisions. Planning, Session completion, and successful Git commands do not prove acceptance.
- For remote synchronization, record a `RemoteSyncPlan`: selected project refs or roles, concrete purpose, target remote/visibility, trigger or timing, retention, decision owner, and required approvals. A concise decision in existing context is sufficient; no new planning service or separate approving Agent is implied.
- Select remote refs only for an actual handoff, CI, review, release, recovery, or publication need. Local branch existence is not a reason. Route exact Git mechanics to `eng-repo-governance`; use `eng-workspace-governance` for participating cross-repository facts and dependencies.

## Evidence and boundaries

Report the exact decision subject and outcome first, followed by material blockers and the required owner/action. Put references, evidence detail, residual risk, and history later; omit empty fields instead of emitting a full WorkItem-shaped record. Follow the [review and handoff priority](../../../docs/review-handoff-template.md) for a human-facing handoff. Stop the action on ambiguous canonical state, stale required evidence, or missing authority; continue independent authorized work when safe. Selection, local integration, synchronization, publication, and deployment remain distinct. This Skill does not author delivery artifacts, run Git, redefine test semantics, or manage Session state.
