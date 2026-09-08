---
name: eng-repo-governance
description: Govern mutations inside one Git repository, including branches, worktrees, commits, integration, promotion, history rewrites, and cleanup. Use for Git writes; do not trigger for read-only status, diff, log, or show.
---

# Repository governance

Own the collaboration and integration mechanics of one Git repository without assuming a task system or whether contributors are people or agents.

## Required inputs

Identify the repository and requested mutation, exact base and current head, branch/worktree and dirty-state facts, intended write scope, and the applicable project profile: branch patterns, change key, integrator, and promotion authority. Resolve the exact target before mutating. If a required ref, dirty-path owner, or authority is missing, return `needs_input` or `blocked` and make no mutation.

Read [the repository protocol](references/repo-protocol.md) when planning or performing a Git mutation. Use the repository slice from [the shared governance contract](../../../docs/governance-contract.md); write no other slice.

## Decisions and workflow

1. Inventory the repository, common Git directory, refs, worktrees, dirty paths, and relevant remotes. Existing dirty content belongs to its current owner until proven otherwise.
2. Assign neutral branch roles such as contributor, review, aggregate, integration, and stable from the supplied profile. Do not hard-code ticket systems, job titles, or one hosting provider.
3. Enforce one writer per worktree and an explicit write scope. Create or reuse branches/worktrees only within the requested workflow and from an exact base.
4. Perform only the authorized mutation. Record old and new exact refs; never use an unresolved path, glob, floating ref, or destructive fallback to conceal a conflict.
5. Produce a handoff commit and repository slice containing base/head, branch/worktree, write scope, evidence, dependencies, and unresolved risks.
6. For integration, freeze the candidate set and head, aggregate in declared order, verify the frozen head, and promote only the same verified history under the supplied promotion authority.
7. Treat rebase, force updates, history rewrite, tag publication, push, and cleanup as separate decisions. Do not rewrite a handed-off/shared commit. Cleanup requires exact targets, clean-state and recoverability evidence, and explicit authority.

Repository governance implements Git mechanics after project governance selects what and when. It does not select candidates or release windows, define cross-repository dependencies, or manage agent sessions.

## Output and stop

Return the repository slice plus actual command/evidence summary, status (`complete`, `blocked`, or `needs_input`), and any authority still required. Stop at the requested local commit, integration, or promotion boundary. A local commit or merge never implies push, publication, deployment, or cleanup.
