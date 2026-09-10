---
name: eng-repo-governance
description: Constrain mutations inside one Git repository, including branches, worktrees, commits, integration, promotion, history rewrites, and cleanup. Use for Git writes; do not trigger for read-only status, diff, log, or show.
---

# Repository governance

Own Git safety and mutation evidence, not project selection or workflow orchestration. Read [the repository protocol](references/repo-protocol.md) for the requested Git action. Use only the repo slice from [the shared governance contract](../../../docs/governance-contract.md) when structured mutation evidence is needed.

## Before a Git mutation

- Resolve the exact repository, operation, targets, relevant base/current refs, branch/worktree occupancy, dirty-state ownership, write scope, and authority. Discover available facts through read-only checks rather than asking the user to fill a form.
- Preserve existing changes. Stop the affected mutation on ambiguous ownership, conflicting writers, unresolved targets, or insufficient authority; do not stash, reset, rewrite, or clean up to conceal the conflict.
- Apply relevant project policy. A local branch or commit does not require an integrator, release window, promotion authority, task adapter, or Session record.

## Creating branches, worktrees, or commits

- Bind a contributor branch to a bounded change, not a role, date, or Session lifecycle. Create or reuse a suitable branch/worktree within the requested scope from an exact stable code base. An immutable definition input may be read by exact reference without being an ancestor or merged branch. Respect supplied naming rules; otherwise use a descriptive `codex/<change>` branch.
- Enforce one active writer per worktree. Concurrent repository writers need isolated worktrees; read-only analysis or review does not. Do not move a branch already checked out elsewhere.
- Keep the commit scoped and report its actual resulting identity. Do not force an extra handoff commit for an action that does not create content.
- Review, aggregate, and integration branches are optional tools for an actual need, not mandatory stages. A new Session does not require a new branch, and ending a Session does not require deleting one.

For a foreground writer on a POSIX host, [writer.py](scripts/writer.py) validates the exact branch/base and holds a per-worktree process lock for the command lifetime. Use it when competing launchers are a real risk; it is not a required persistent lease or Session service. See the protocol for its limits.

## Integrating or promoting

- Consume the authorized target and selected exact candidates. Check actual code ancestry, definition references, promotion constraints, conflicts, and the applicable verification requirements. For multiple candidates, start from the project-selected current stable base and preserve the selected set and meaningful code-dependency order.
- Bind validation to the exact resulting head. Promote only verified history under the supplied authority. A changed base, candidate, squash, or merge result needs new or justified reusable evidence for that result.
- Do not rewrite a shared or handed-off commit. Corrections use new commits or an explicitly authorized integration operation.

## Synchronizing, rewriting, or cleaning up

- For remote synchronization, consume the project-selected `RemoteSyncPlan` without adding refs or changing timing. Resolve exact refspecs and expected remote revisions, apply safety checks, execute only authorized writes, and verify the observed remote result.
- A review branch is an ephemeral carrier for an active PR, remote CI, collaboration, or recovery purpose. Updating one proposal does not require a new branch for every draft revision. Merge, cancellation, or supersession makes it eligible for separately authorized cleanup; it does not delete the ref automatically.
- Treat push, tag publication, force updates, history rewrite, and cleanup as separately authorized actions. A local commit or merge supplies none of that authority.
- Cleanup requires exact targets, clean-state and recovery evidence, and explicit permission or a configured user preference covering those targets. Merge status alone does not create a universal cleanup rule; uncertain state is retained.

## Evidence and boundaries

Report the actual mutation and relevant before/after refs, scoped verification, unresolved risks, and any remaining requested action. Stop at the requested boundary. Project governance owns candidate and release decisions and remote-sync intent; workspace governance owns cross-repository dependencies. Those ownership boundaries do not require separate Agents or approval hops. Repository governance does not manage Session state or infer publication, deployment, or cleanup.
