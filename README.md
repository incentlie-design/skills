# skill-creator

A public source repository for four orthogonal engineering-governance Skills. They coordinate delivery without assuming a particular task system, agent implementation, Git host, or Codex Project.

| Skill | Owns | Does not own |
| --- | --- | --- |
| [`eng-repo-governance`](skills/engineering/eng-repo-governance/SKILL.md) | One Git repository: roles, branches, worktrees, exact refs, handoff commits, aggregation, freeze, verification, promotion, rewrite, and cleanup safety | Work-item selection, cross-repository topology, or agent lifecycle |
| [`eng-workspace-governance`](skills/engineering/eng-workspace-governance/SKILL.md) | A multi-repository workspace: manifest, exact repository tuples, dependency DAG, source facts, cross-repository change set, launch context, and integration order | Per-repository Git mechanics, work-item state, or agent lifecycle |
| [`eng-project-governance`](skills/engineering/eng-project-governance/SKILL.md) | Intake-to-close governance: canonical work items, revisions, milestones, candidate/release selection, release windows, pipeline gates, and task-system adapters | Writing requirements/architecture/code/tests or performing Git operations |
| [`eng-agent-governance`](skills/engineering/eng-agent-governance/SKILL.md) | Capability roles, independence, sessions, assignments, budgets, ownership leases, blocking, handoffs, release, and closure responsibility | A second task state machine, Git mechanics, or test semantics |

## Composition

The dependency direction is:

```text
eng-project-governance -> eng-workspace-governance -> eng-repo-governance
eng-agent-governance   -> eng-project-governance
eng-agent-governance   -> eng-repo-governance
```

Dependencies mean “read or delegate when that boundary is needed,” not “invoke every Skill for every request.” Project governance selects what and when; workspace governance freezes where and in which dependency order; repository governance performs Git mechanics; agent governance assigns who or which capability and releases its leases.

Cross-Skill handoffs use one shared, slice-owned packet: [responsibility and composition contract](docs/governance-contract.md) and [machine-readable schema](contracts/governance-handoff.schema.json). Each Skill writes only its own slice and references the others.

## GitHub remote and branch synchronization

The canonical repository is [incentlie-design/skills](https://github.com/incentlie-design/skills), stored locally as `origin`. Remote writes remain separately authorized; configuring the remote does not authorize a push.

| Ref role | Synchronize to GitHub when | Default |
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
