# Governance responsibility and handoff contract

This contract prevents the four Skills from copying or competing for the same state. The canonical machine-readable shape is [`governance-handoff.schema.json`](../contracts/governance-handoff.schema.json).

## Responsibility matrix

| Owner | Required input | Owned output | Forbidden scope | Reads or delegates to |
| --- | --- | --- | --- | --- |
| `eng-project-governance` | Raw intake or `work_item_ref`, system of record, goal/architecture/task revisions, acceptance criteria, project profile, release/publication authority | Project slice, canonical work-item decisions, milestone/candidate/release-window/gate state, remote-sync selection and timing | Authoring requirements or architecture, implementation, testing, Git mechanics, agent-session state | Workspace slice when multiple repositories participate; repository governance for authorized Git execution |
| `eng-workspace-governance` | Workspace identity, repository facts, exact commits, dependency edges, change set, launch context | Workspace slice, validated manifest, cross-repository DAG and integration order | Single-repository Git policy, task state, agent lifecycle | Repository slice for each concrete Git operation |
| `eng-repo-governance` | Repository identity/path, exact base/head, requested mutation, dirty/worktree facts, branch profile, project-selected remote-sync plan when applicable, authority | Repository slice, mutation plan/result, handoff commit, freeze/promotion evidence, remote-sync execution evidence, cleanup decision | Work/release or remote-sync selection/timing, multi-repository dependency ownership, agent-session state | No governance dependency for its owned mechanics |
| `eng-agent-governance` | `work_item_ref`, adapter binding, role/capability, session owner, scope, budget, acceptance and stop conditions | Agent slice, assignment/lease state, blocked/handoff/closure record | A second work-item state machine, Git mechanics, test semantics | Project state through its adapter; repository operations through repository governance |

Ownership is exclusive. A Skill may quote another slice by `handoff_id` or reference, but must not rewrite it. If required fields are unavailable, return `needs_input` or `blocked`; do not invent placeholder revisions, commits, authority, or evidence.

## Dependency direction

```text
project -> workspace -> repo
agent   -> project
agent   -> repo
```

There is no reverse dependency. Repository state never chooses a release; workspace topology never creates work-item status; agent status never becomes a second task system. Dependencies are conditional routing boundaries, not a requirement to load every Skill.

## Composite handoff

The envelope contains `schema_version`, a stable `handoff_id`, and one or more owned slices. Include only slices that actually participate, but an included slice must be complete.

| Slice | Owner | Required content |
| --- | --- | --- |
| `project` | `eng-project-governance` | `work_item_ref`, goal/architecture/task revision, acceptance criteria, release target, and `remote_sync_plan_ref` when remote synchronization participates |
| `workspace` | `eng-workspace-governance` | Manifest reference, repository exact-ref tuples, cross-repository dependency edges |
| `repo` | `eng-repo-governance` | Repository id, base/head, branch/worktree, write scope, freeze and promotion evidence |
| `agent` | `eng-agent-governance` | Role/session/owner, budget, status, stop condition, handoff reference, released leases |

Evidence binds to exact revisions. A selection or gate decision that changes any participating revision makes earlier downstream evidence stale until the owning Skill records an impact decision.

## Authority and stop rules

- Project governance decides which candidate or release target is selected, when a window opens, and which project branch roles/refs need remote synchronization at what trigger or time. Repository governance resolves an approved plan to exact refspecs, validates expected local and remote revisions, and only then implements the authorized Git mechanics.
- Repository governance may reject an unsafe or stale remote-sync plan, but it may not add refs, choose publication timing, or infer synchronization need from local branches and worktrees.
- Workspace governance supplies repository facts and order. It cannot turn a missing commit into a floating default.
- Agent governance may claim or release an ownership lease; it may only propose repository cleanup and report clean/dirty state.
- External task-system writes require an authorized sink binding and an expected revision. Git push, tag publication, history rewrite, destructive cleanup, deployment, and production writes require their own authority.
- Stop at the requested local candidate, gate, or handoff. “Integrated,” “published,” and “deployed” are distinct states and must not be inferred from one another.
