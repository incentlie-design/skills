# Multi-repository workspace manifest

Read this reference when creating or changing a multi-repository manifest, or providing a reproducible workspace handoff. The example's change-set and launch fields apply when the consumer needs them; they are not prerequisites for cross-repository analysis.

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

For an edge `{from: A, to: B}`, A depends on B. The required input or interface must be available before the dependent action consumes it; this does not serialize every action in either repository. Bind manifest changes to their actual affected evidence and recheck or justify reuse before relying on that evidence.

## Handoff and delegation

The workspace slice carries the manifest ref, exact repository tuples, and dependency edges. Repository-specific base/head, branch/worktree, and mutation evidence stay in repository slices. Use `eng-repo-governance` for every concrete Git operation, preserving actual dependency and write-isolation constraints without imposing a universal serial schedule.

A valid workspace handoff is reproducible topology, not proof that repository candidates passed gates or that a release was selected.
