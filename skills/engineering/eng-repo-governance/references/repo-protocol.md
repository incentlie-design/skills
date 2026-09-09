# Single-repository mutation protocol

Read this reference only when a Git mutation is requested or is a necessary implementation step.

## Repository profile

Use only the profile parameters relevant to the requested operation. This expanded example describes a project that actually uses several branch roles; it is not a required branch topology or a startup form:

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

Names are examples resolved through the profile, not universal branch rules. A bounded local change normally needs a suitable contributor branch, not the review, aggregate, integration, integrator, or promotion fields. Without a supplied naming policy, use `codex/<change>`. Preserve existing branch/worktree ownership when reusing them.

## Mutation record

Before a write, resolve repository path and common Git directory, relevant exact base/current refs, branch/worktree occupancy, dirty paths and owner, requested operation, write scope, authorization, and a recovery point when needed. These facts may come from read-only inspection and existing context; a separate plan file is not required. Abort the affected mutation on a mismatch between expected and observed refs.

After a write, capture the exact resulting head, changed paths, command class, verification bound to that head, and any remaining local or remote action. Do not report a planned commit as created or a dry run as execution.

## Branch and worktree roles

- A contributor branch carries one bounded change from an exact base.
- A review branch is optional and must not become a second writer for contributor-owned paths.
- An aggregate branch combines compatible candidates without declaring them stable.
- An integration branch freezes an ordered candidate set and exact head for verification.
- A stable branch receives only the selected, verified history through the authorized promotion mechanism.

These roles describe optional uses, not a required sequence. Branches carry changes independently of Session lifetime. One worktree has one active writer; concurrent repository writers use isolated worktrees, while read-only collaborators need no separate write worktree. A branch already checked out elsewhere is not silently moved. A handed-off commit is immutable; subsequent corrections are new commits or an authorized integration operation.

## Freeze, verification, and promotion

For integration, bind evidence to the selected candidate commits, relevant base, resulting head, and required verification. A multiple-candidate integration also identifies the selected set and dependency order. Do not create a freeze record or an integration branch for an unrelated Git action. If candidates or the base change, reassess affected evidence and verify or justify reuse for the new head; never label evidence from another head as current without that basis.

Project governance owns candidate and release-window selection. This Skill confirms ancestry and performs the profile-authorized merge, cherry-pick, or fast-forward. Squash or rewrite creates a new head and therefore needs evidence on that resulting head.

## Remote branch synchronization

Consume the approved project `RemoteSyncPlan` and resolve only its named branch roles/refs into an explicit refspec allowlist. Never infer synchronization need from all local branches or worktrees, and never add a branch because it appears useful.

Validate the plan against these repository guardrails:

- A selected stable branch must name the exact promoted head that passed its gates. Do not force-update it.
- A selected archive branch requires approved destination visibility and exposure-review evidence. Treat a published archive ref as immutable; reject publication to the main remote when a restricted backup is required.
- A selected integration branch must bind remote CI, review, or integrator consumption to the exact frozen head.
- A selected contributor, review, aggregate, session, or agent branch must identify its cross-machine/owner handoff, PR, remote CI, or recovery purpose. Reject ordinary local or already-integrated work with no current purpose.
- A selected release branch must correspond to an actual release workflow. Tags remain a separate publication decision and are never added implicitly or bulk-pushed.

Repository governance may reject a stale, ambiguous, unauthorized, or unsafe plan, but it must not choose a new synchronization need or time. Before pushing, read remote refs, compare the expected remote revision, verify the exact local head and intended paths, and obtain authority for the named refspecs. Push those refspecs individually. A non-fast-forward update, remote deletion, force update, or cleanup requires a separate decision and recovery evidence. Afterward, re-read the remote refs and report the exact result; partial success must not be summarized as full synchronization.

## History rewrite and cleanup

Rewrite only an unshared branch when policy and authority explicitly allow it; never use rewrite to bypass dirty state, evidence, or another writer. Push and force updates are remote writes with separate authority.

Cleanup is a new mutation, not an automatic epilogue. Resolve each branch/worktree/tag target, confirm clean state, retained recovery commit, integration status, and authorization. Prefer leaving a recoverable candidate over deleting uncertain state.

A bare merge-status statement such as “已合并” does not by itself authorize deletion. An explicit cleanup request or configured user preference may supply that authority without another confirmation. Resolve its exact scope, verify integration, clean state, and recovery, then remove only the covered targets when no retention rule applies. Remote deletion needs authority that covers the remote ref. Keep unverifiable or dirty state and report why; never extend authority to unrelated refs, tags, archive branches, or history rewrites. Session archival is independent and is not a repository completion gate.
