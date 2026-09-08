---
name: eng-workspace-governance
description: Govern a workspace composed of multiple repositories through a manifest, exact commit tuples, cross-repository dependencies, change sets, launch context, handoffs, and integration order. Do not use for single-repository Git mechanics or agent lifecycle.
---

# Workspace governance

Own the topology and reproducibility of a workspace whose deliverable spans multiple repositories. A Codex Project may be an adapter, but it is never the only implementation assumption.

## Required inputs

Identify the workspace, participating repository facts, exact commit for each repository, dependency edges, cross-repository change set, source evidence, and required launch directory/environment. Missing or floating repository refs stop planning at `needs_input`; do not silently resolve them from default branches.

Read [the workspace manifest reference](references/workspace-manifest.md) when creating, revising, or consuming a workspace manifest. Use only the workspace slice from [the shared governance contract](../../../docs/governance-contract.md).

## Decisions and workflow

1. Build a manifest with stable `repo_id`, path, remote, role, default ref, and exact commit for every participating repository. Record where each fact came from and distinguish observed facts from assumptions.
2. Validate unique repository ids and paths, accessible launch contexts, dependency endpoints, and an acyclic cross-repository DAG.
3. Define the cross-repository change set: participating work items or change refs, repository-local scope, interface/version constraints, and the exact tuple that downstream work consumes.
4. Derive handoff and integration order from dependency direction. Freeze the manifest revision and exact repository tuple before cross-repository verification.
5. Delegate every branch, worktree, commit, merge, rebase, tag, push, or cleanup operation within a repository to `eng-repo-governance`. Reference its repository slice; do not copy its Git rules here.

Workspace governance does not create work-item state, choose a release window, manage agents, or declare a repository mutation successful from topology alone.

## Output and stop

Return the workspace slice, manifest location/revision, validated dependency order, source-fact ledger, launch instructions, unresolved constraints, and status. Stop when the requested manifest/handoff is reproducible, or earlier on missing exact refs, ambiguous repository identity, inaccessible inputs, or a dependency cycle. Do not infer integration, publication, or deployment from a valid manifest.
