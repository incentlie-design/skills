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

## Validate

The validator uses only the Python standard library:

```sh
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests
git diff --check
```

It checks the exact four-entry registry, Skill/frontmatter/metadata/case completeness, discovery links, relative Markdown links, dependency acyclicity, shared-slice ownership, and four bounded composition scenarios. Defined behavior cases are not claimed as live external execution.

Project discovery links in `.agents/skills/` point to the source folders with relative symlinks. Installing or removing user-level Skills, pushing, publishing, and writing production systems are separate authorized actions.
