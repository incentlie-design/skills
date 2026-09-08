# skill-creator

A public source repository for four orthogonal engineering-governance Skills. They coordinate delivery without assuming a particular task system, agent implementation, Git host, or Codex Project.

## Boundaries and responsibilities

Choose the owner from the decision being made, not merely from the tool being used. Each Skill owns one state domain and delegates work outside that domain.

| Skill | Governing question | Owns | Must not own |
| --- | --- | --- | --- |
| [`eng-project-governance`](skills/engineering/eng-project-governance/SKILL.md) | What work or candidate enters delivery, and when? | One canonical WorkItem and system of record; goal/architecture/task revisions; acceptance criteria; milestones; candidate and release-window selection; pipeline gates; closure decisions; `RemoteSyncPlan` selection and timing | Authoring requirements, architecture, code, or tests; repository mutations; workspace topology; agent-session state |
| [`eng-workspace-governance`](skills/engineering/eng-workspace-governance/SKILL.md) | Which repositories and exact commits form the deliverable, in what dependency order? | Multi-repository manifest; exact repository tuples; source-fact ledger; cross-repository change set and DAG; launch context; handoff and integration order | Project/work-item state; single-repository Git policy or mutation; agent lifecycle |
| [`eng-repo-governance`](skills/engineering/eng-repo-governance/SKILL.md) | How does one repository move safely from one exact Git state to another? | Branch/worktree roles; exact base and head; write scope; commits and handoffs; freeze, verification, integration, and promotion mechanics; execution of approved pushes, rewrites, and cleanup | Candidate/release or remote-sync selection and timing; cross-repository dependency ownership; agent-session state |
| [`eng-agent-governance`](skills/engineering/eng-agent-governance/SKILL.md) | Who or which capability executes a bounded assignment, under what ownership, budget, and stop condition? | Capability roles; sessions and assignments; independence constraints; ownership leases; context and budget; blocked/handoff/closure records; lease release | A second WorkItem state machine; Git policy or mechanics; test-layer and pass/fail semantics |

The practical split is:

1. Project governance normalizes the request, records the current decision revisions and acceptance criteria, and selects candidates, release timing, gates, and any branches that need remote synchronization.
2. Agent governance binds a bounded assignment to that project state. Its lease coordinates ownership but grants no new filesystem, Git, network, tracker, or production permission.
3. Workspace governance participates only when the deliverable spans multiple repositories. It freezes the exact repository tuple and dependency order; a single-repository task does not need a workspace layer.
4. Repository governance performs each authorized Git mutation against exact refs. It may reject stale or unsafe input, but it cannot change the project decision or expand a `RemoteSyncPlan`.
5. Results return through the owning slices. Project governance records gate or closure decisions; “handoff,” “integrated,” “synchronized,” “published,” and “deployed” remain distinct states.

## Composition

The dependency direction is:

```text
eng-project-governance -> eng-workspace-governance -> eng-repo-governance
eng-agent-governance   -> eng-project-governance
eng-agent-governance   -> eng-repo-governance
```

Dependencies mean “read or delegate when that boundary is needed,” not “invoke every Skill for every request.” Project governance selects what and when; workspace governance freezes where and in which dependency order; repository governance performs Git mechanics; agent governance assigns who or which capability and releases its leases.

Typical routes remain bounded:

| Request shape | Route |
| --- | --- |
| One local repository change with an assigned executor | Agent → Repo |
| Multi-repository delivery or release | Project → Workspace → Repo, with Agent for assignments |
| External WorkItem transition | Agent → Project |
| Branch/worktree cleanup after handoff | Agent reports/releases → Repo decides and executes |

## Contract model

Cross-Skill handoffs use one shared envelope defined by the [responsibility and composition contract](docs/governance-contract.md) and [machine-readable schema](contracts/governance-handoff.schema.json):

```json
{
  "schema_version": 1,
  "handoff_id": "handoff:example-42",
  "slices": {
    "project": {},
    "workspace": {},
    "repo": {},
    "agent": {}
  }
}
```

Include only the slices that participate in the request. An included slice is complete and has exactly one owner:

| Slice | Owner | Contract identity |
| --- | --- | --- |
| `project` | `eng-project-governance` | WorkItem reference; goal, architecture, and task revisions; acceptance criteria; release target; optional `remote_sync_plan_ref` |
| `workspace` | `eng-workspace-governance` | Manifest reference; exact repository refs; cross-repository dependency edges |
| `repo` | `eng-repo-governance` | Repository id; exact base/head; branch/worktree; write scope; freeze and promotion evidence |
| `agent` | `eng-agent-governance` | Role/session/owner; budget and status; stop condition; handoff reference; released leases |

The contract has five invariants:

- **Exclusive ownership:** a Skill writes only its own slice. It may reference another slice by `handoff_id` or stable reference, but it cannot copy and then redefine that state.
- **Exact evidence:** repository and workspace facts bind to exact commits; project and external-system decisions bind to explicit revisions. Floating refs and planned-but-unexecuted evidence are not accepted as completed state.
- **Freshness propagation:** changing a participating goal, architecture, task, candidate, manifest, base, or head revision makes dependent gate and execution evidence stale until the owning Skill records an impact decision.
- **Separate authority:** a plan or local commit does not authorize tracker writes, push, tag publication, history rewrite, cleanup, deployment, or production changes. Each external or destructive action needs its own authority and expected target revision.
- **Bounded failure:** missing ownership, authority, exact refs, or a unique system of record returns `needs_input` or `blocked`; no Skill invents placeholder state or silently takes over another slice.

## GitHub remote and branch synchronization

The canonical repository is [incentlie-design/skills](https://github.com/incentlie-design/skills), stored locally as `origin`. `eng-project-governance` owns the decision about which project branch roles/refs need synchronization and when; the table below is this project's profile for that decision. `eng-repo-governance` consumes the approved plan, resolves it to exact refspecs, validates remote state and safety, and executes only a separately authorized push. Configuring the remote does not authorize one.

| Ref role | Project decision condition | Default |
| --- | --- | --- |
| `main` | The exact local head passed the required gates and was promoted to the stable branch | Push after each authorized stable promotion; never force-push |
| `archive/*` | A named recovery baseline must survive local machine loss, the remote visibility is approved, and the archived tree passed an exposure review | Conditional push to an approved remote; keep immutable and do not silently move or delete |
| `integrate/*`, `codex/integrate/*` | Remote CI, review, or another integrator must consume the exact frozen head | Local-only otherwise; remove remotely only with separate cleanup authority |
| `session/*`, `codex/session/*`, `agent/*`, `codex/agent/*`, `review/*`, `aggregate/*` | An unmerged handoff must cross machines/owners, a PR or remote CI requires it, or it is approved as recovery-worthy work | Local-only after ordinary work; do not upload merely because a worktree exists |
| `release/*` | A real release-stabilization workflow explicitly uses a remote branch | Do not create or push for routine delivery |

For the first publication of this rebuilt repository, only `main` is required. `archive/2026-09-08/main-before-public-governance-rebuild` is conditional because it contains the complete removed tree: synchronize it only after the owner confirms remote visibility and approves that historical content for exposure; otherwise retain it locally or in a restricted backup. The already-integrated rebuild session branch and unrelated historical worktree branches are not part of the initial set.

Before any push, fetch or query remote refs, bind validation to the exact local head, confirm the branch contains no unintended or sensitive files, and obtain push authority. Push explicit refs only—never use `--all`, `--mirror`, bulk tag upload, remote deletion, or force update as a convenience. Tags are published separately only for an authorized version release.

## Validate

The validator uses only the Python standard library:

```sh
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests
git diff --check
```

It checks the exact four-entry registry, Skill/frontmatter/metadata/case completeness, discovery links, relative Markdown links, dependency acyclicity, shared-slice ownership, and four bounded composition scenarios. Defined behavior cases are not claimed as live external execution.

Project discovery links in `.agents/skills/` point to the source folders with relative symlinks. Installing or removing user-level Skills, pushing, publishing, and writing production systems are separate authorized actions.
