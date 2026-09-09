# Multi-repository workspace manifest

Read this reference when a task spans multiple repositories or needs a reproducible workspace handoff.

## Manifest shape

```json
{
  "schema_version": 1,
  "workspace_id": "payments-suite",
  "revision": "workspace-r3",
  "repos": [
    {
      "repo_id": "api",
      "path": "repos/api",
      "remote": "origin",
      "role": "service",
      "default_ref": "main",
      "commit": "0123456789abcdef"
    }
  ],
  "dependency_edges": [
    {"from": "web", "to": "api", "reason": "Consumes API schema"}
  ],
  "change_set": [
    {"work_item_ref": "tracker:42", "repo_id": "api", "scope": ["schema/"]}
  ],
  "launch": {
    "directory": "repos/api",
    "environment_ref": "env/local-v1"
  },
  "source_facts": [
    {"field": "repos.api.commit", "source": "local-ref", "observed": true}
  ]
}
```

Paths are workspace-relative unless the caller explicitly needs an environment-specific absolute path. `default_ref` is descriptive; `commit` is the exact consumed state. Remote may be absent or null for a local-only repository.

## Validation

- Each `repo_id` and resolved path is unique.
- Every participating repository has an exact commit and a source for that fact.
- Dependency endpoints exist and the directed graph is acyclic.
- Change-set scopes identify a repository and do not overlap another active writer without an ownership decision.
- Launch directory and environment reference are sufficient for the next consumer; credentials remain external.

For an edge `{from: A, to: B}`, A depends on B, so prepare and integrate B before A unless an interface contract explicitly allows parallel work. A changed edge, commit, or interface constraint increments the manifest revision and makes dependent cross-repository evidence stale.

When one repository consumes repo-scoped Skills from another, record the consumer-to-source edge and bind the synchronization to the source repository's exact `main` commit and canonical registry. Delegate the source refresh and consumer write to each repository's governance, reconcile only the managed `.agents/skills` entries to the registered names, preserve unrelated project Skills, and verify every resulting entry resolves to a `SKILL.md`. Record both exact commits; do not treat a floating branch or copied Skill body as a reproducible synchronization.

## Handoff and delegation

The workspace slice carries the manifest ref, exact repository tuples, and dependency edges. Repository-specific base/head, branch/worktree, and mutation evidence stay in repository slices. Use `eng-repo-governance` for every concrete Git operation, one repository at a time and in the derived order.

A valid workspace handoff is reproducible topology, not proof that repository candidates passed gates or that a release was selected.
