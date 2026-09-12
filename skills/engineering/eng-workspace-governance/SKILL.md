---
name: eng-workspace-governance
description: Constrain multi-repository topology and dependency changes, reproducible commit tuples, workspace handoffs, and integration order. Use for those cross-repository actions; do not require a manifest for single-repository work or manage Session lifecycle.
---

# Workspace governance

Own cross-repository topology, dependencies, and reproducibility, not the Agent's scheduling. Use only the workspace slice from [the shared governance contract](../../../docs/governance-contract.md) when a structured reproducible handoff is needed.

Read [the workspace manifest reference](references/workspace-manifest.md) when creating, revising, or consuming a manifest. Mere access to several repositories does not require a new manifest, change set, or integration pipeline.

## Changing topology or dependencies

- Resolve participating repository identities, paths, source facts, and relevant interface or version constraints. Distinguish observed facts from assumptions and validate dependency endpoints.
- Represent genuine input dependencies and shared-write conflicts, not a prescribed sequence of Agent roles. Reject cyclic dependency claims; independent work may be organized as the Agent chooses.
- Reuse an existing manifest when applicable. Describe only the requested change and affected repositories; do not require task-system or Session records.

## Providing a reproducible handoff or verification tuple

- Resolve the intended repository refs to exact commits through supplied evidence or read-only checks. A default branch name is descriptive, not immutable evidence. If the intended version cannot be determined, block the reproducibility claim and affected actions, not useful partial analysis.
- Record a manifest reference with unique repository ids and paths, exact consumed commits, actual dependency edges, and launch context sufficient for the requested consumer. Credentials remain external.
- Before cross-repository verification or integration, identify the participating tuple and order constrained by real dependencies. Changed commits or interfaces require reassessment of affected evidence, not a blanket pause on unrelated work.

## Mutations, evidence, and boundaries

Every Git mutation uses `eng-repo-governance`; reference its exact-state evidence without duplicating its rules. For a human-facing result, lead with the exact repository tuple or topology subject, conclusion, material mismatch, and required owner/action; put dependency detail and residual uncertainty afterward using the [review and handoff priority](../../../docs/review-handoff-template.md). A short verified tuple needs no empty manifest sections. A valid manifest does not prove acceptance, integration, publication, or deployment. This Skill does not select releases, create project state, assign Agents, or require a separate Session for each repository.
