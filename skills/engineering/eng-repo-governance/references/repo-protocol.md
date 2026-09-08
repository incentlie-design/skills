# Single-repository mutation protocol

Read this reference only when a Git mutation is requested or is a necessary implementation step.

## Repository profile

The caller or project supplies the policy parameters; this Skill supplies mechanics:

```json
{
  "repo_id": "service-a",
  "path": "repos/service-a",
  "change_key": "change-42",
  "branch_patterns": {
    "contributor": "change/{change_key}",
    "review": "review/{change_key}",
    "aggregate": "aggregate/{change_key}",
    "integration": "integrate/{window}",
    "stable": "main"
  },
  "integrator": "integration-owner",
  "promotion_authority": "release-owner"
}
```

Names are examples resolved through the profile, not universal branch rules. Record the resolved profile with the mutation plan.

## Mutation record

Before a write, capture repository path and common Git directory, exact base/current head, branch/worktree occupancy, dirty paths and owner, requested operation, write scope, authorization, and rollback or recovery point. Abort on a mismatch between expected and observed refs.

After a write, capture the exact resulting head, changed paths, command class, verification bound to that head, and any remaining local or remote action. Do not report a planned commit as created or a dry run as execution.

## Branch and worktree roles

- A contributor branch carries one bounded change from an exact base.
- A review branch is optional and must not become a second writer for contributor-owned paths.
- An aggregate branch combines compatible candidates without declaring them stable.
- An integration branch freezes an ordered candidate set and exact head for verification.
- A stable branch receives only the selected, verified history through the authorized promotion mechanism.

One worktree has one active writer. A branch already checked out elsewhere is not silently moved. A handed-off commit is immutable; subsequent corrections are new commits or an authorized integration operation.

## Freeze, verification, and promotion

The freeze record contains stable base, ordered candidate commits, dependency order, generated integration head, and verification plan. Evidence is valid only for that exact head. If candidates or the base change, mark it stale and verify the new head.

Project governance owns candidate and release-window selection. This Skill confirms ancestry and performs the profile-authorized merge, cherry-pick, or fast-forward. Squash or rewrite creates a new head and therefore needs evidence on that resulting head.

## History rewrite and cleanup

Rewrite only an unshared branch when policy and authority explicitly allow it; never use rewrite to bypass dirty state, evidence, or another writer. Push and force updates are remote writes with separate authority.

Cleanup is a new mutation, not an automatic epilogue. Resolve each branch/worktree/tag target, confirm clean state, retained recovery commit, integration status, and authorization. Prefer leaving a recoverable candidate over deleting uncertain state.
