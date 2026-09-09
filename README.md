# skill-creator

A public source repository for eight orthogonal engineering Skills: four state-owning governance Skills, one closed-loop decision advisor, and three artifact-owning role Skills.

## Constrain actions, not orchestration

The Agent decides how to organize work within the user's request and authority. Skills constrain the actions it chooses: when a rule applies, which facts or permissions that action needs, what is forbidden, and what evidence supports the result. They do not install a lifecycle, prescribe a role sequence, or require separate Sessions and approval hops.

Loading a Skill does not require creating its objects. A normal local change can remain in the current task and use a suitable branch, focused checks, and a concise result. It does not need a WorkItem, assignment packet, budget, lease, milestone, or release window unless the requested action or actual project policy needs one.

## Action routing

| Chosen action | Skill | Constraint and evidence |
| --- | --- | --- |
| Compare zero-to-one product or architecture paths | [Closed Loop](skills/engineering/eng-closed-loop-decisions/SKILL.md) | Recommend the smallest clean actor-to-evidence loop; advice does not change canonical state or authorize implementation |
| Produce a bounded plan | [PM](skills/engineering/eng-pm/SKILL.md) | Preserve intent, observable acceptance, real dependencies, risks, and decision evidence |
| Implement or self-check a bounded change | [DEV](skills/engineering/eng-dev/SKILL.md) | Trace affected behavior, use the smallest complete change, and provide focused evidence |
| Evaluate evidence or review an implementation | [QA and Reviewer](skills/engineering/eng-qa-reviewer/SKILL.md) | Bind conclusions to the subject and applicable checks; preserve required independence |
| Register/update canonical work or make scope, acceptance, dependency, candidate, gate, or remote-sync decisions | [Project](skills/engineering/eng-project-governance/SKILL.md) | Preserve the authoritative source, relevant revisions, decision authority, and actual evidence |
| Delegate, create/reuse a Session, resolve shared ownership, or adopt delegated results | [Agent](skills/engineering/eng-agent-governance/SKILL.md) | Clarify scope and responsibility; prevent write conflicts and false independence; collect required outputs |
| Change multi-repository topology/dependencies or supply a reproducible tuple | [Workspace](skills/engineering/eng-workspace-governance/SKILL.md) | Identify repositories, actual dependencies, and exact consumed commits when reproduction needs them |
| Mutate Git state | [Repo](skills/engineering/eng-repo-governance/SKILL.md) | Resolve exact targets, preserve ownership and dirty state, enforce authority, and report actual resulting refs |

These are routing choices, not stages. The same Agent can use compatible capabilities in any order consistent with real input dependencies, safety, and authority. A role boundary does not require a different executor except for required independence or approval authority. Read-only Git inspection does not trigger mutation governance.

Registry dependencies describe conditional owner routing, not mandatory loading or execution dependencies. The four slice owners remain exclusive; the advisor and three role Skills own their respective artifacts, not governance state.

## Branch, project, and Session boundaries

- **Branches carry changes.** Reuse a suitable branch/worktree with clear ownership; without a project naming rule, use `codex/<change>`. Concurrent repository writers need isolated worktrees; read-only collaborators do not. Review, aggregate, and integration branches are optional, not a required chain.
- **Project records carry project facts.** Respect the selected system of record when operating on it. A missing adapter blocks its operations and dependent decisions, not all useful authorized work. Do not create a mirror or claim an unperformed task update.
- **Sessions carry execution context.** They are not acceptance records. Do not require a title/status mirror, lifecycle transitions, or one branch per Session. Creation pending or missing from a list does not justify duplicate creation.
- **Results carry dependencies.** A consumer needs the required artifact and evidence, not a terminal producer Session or a callback receipt. Account for all required outputs before claiming aggregate completion; a first completed child is not the aggregate result.
- **Changed evidence gets an impact check.** Reassess only affected inputs and claims. Do not pause all work because any upstream revision changed.
- **Cleanup remains a separate action.** Merge, archival, and acceptance are distinct. Honor explicit cleanup/archival requests or configured preferences within their exact scope; a bare merge-status statement is not a universal deletion rule.

## Shared evidence contract

Use existing artifacts and messages unless a consumer actually needs a structured handoff. The [governance contract](docs/governance-contract.md) and [version 2 schema](contracts/governance-handoff.schema.json) retain exactly four slices without requiring lifecycle bookkeeping.

For example, a structured coordination result can identify its actual owner, scope, and output without a Session id, numeric budget, or tracker item:

```json
{
  "schema_version": 2,
  "handoff_id": "handoff:parser-fix",
  "slices": {
    "agent": {
      "owner": "implementation-owner",
      "scope": ["src/parser.py"],
      "output_refs": ["repo:service-a@0123456789abcdef"]
    }
  }
}
```

This is a schema-valid shape, not evidence that the example result exists. Omit irrelevant fields; include actual facts required by the action. Schema validity alone proves neither permission nor acceptance. Project references, repository commits, and workspace tuples retain their own owners; a Session record does not replace them.

Closed Loop and `ponytail` are complementary: the former narrows the product/architecture decision, the latter minimizes the implementation. Neither waives safety, data integrity, or explicit requirements.

## GitHub remote and branch synchronization

The canonical repository is [incentlie-design/skills](https://github.com/incentlie-design/skills), stored locally as `origin`. `eng-project-governance` owns the decision about which project branch roles/refs need synchronization and when; the table below is this project's profile for that decision. `eng-repo-governance` consumes the approved plan, resolves it to exact refspecs, validates remote state and safety, and executes only a separately authorized push. Configuring the remote does not authorize one.

| Ref role | Project decision condition | Default |
| --- | --- | --- |
| `main` | The exact local head passed the required gates and was promoted to the stable branch | Push after each authorized stable promotion; never force-push |
| `archive/*` | A named recovery baseline must survive local machine loss, the remote visibility is approved, and the archived tree passed an exposure review | Conditional push to an approved remote; keep immutable and do not silently move or delete |
| `integrate/*`, `codex/integrate/*` | Remote CI, review, or another integrator must consume the exact frozen head | Local-only otherwise; remove remotely only with separate cleanup authority |
| `codex/<change>` and existing contributor, review, or aggregate branch patterns | An unmerged handoff must cross machines/owners, a PR or remote CI requires it, or it is approved as recovery-worthy work | Local-only after ordinary work; do not upload merely because a worktree exists |
| `release/*` | A real release-stabilization workflow explicitly uses a remote branch | Do not create or push for routine delivery |

For the first publication of this rebuilt repository, only `main` is required. `archive/2026-09-08/main-before-public-governance-rebuild` is conditional because it contains the complete removed tree: synchronize it only after the owner confirms remote visibility and approves that historical content for exposure; otherwise retain it locally or in a restricted backup. The already-integrated rebuild session branch and unrelated historical worktree branches are not part of the initial set.

Before any push, fetch or query remote refs, bind validation to the exact local head, confirm the branch contains no unintended or sensitive files, and obtain push authority. Push explicit refs only—never use `--all`, `--mirror`, bulk tag upload, remote deletion, or force update as a convenience. Tags are published separately only for an authorized version release.

## Project task adapter

[`project.yaml`](project.yaml) selects one provider-neutral task-adapter binding and target; it contains no credentials, database path, provider client settings, WorkItem data, or Agent/Session state. The core [task-adapter SDK](docs/project-task-adapters.md) contains the TaskSource/TaskSink contract and canonical-operation mappings for SQLite, GitHub Issues, and GitLab Issues.

The selected mapping uses provider tools already exposed in the Session. Plugin installation and authentication, SQLite storage, provider initialization, and mirrors belong to the execution environment; the Skill only checks availability and never bootstraps them.

## Validate

The validator uses only the Python standard library:

```sh
python3 scripts/validate_project.py
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests
git diff --check
```

It checks the exact eight-entry registry, required Skill frontmatter, any supplied metadata and behavior cases, discovery links, relative Markdown links, dependency acyclicity, the four shared-slice owners, and bounded action-routing scenarios. Scenario routes are unordered required owner sets, not execution sequences. Defined behavior cases are not claimed as executed behavior. Focused schema-instance tests use `jsonschema` when already installed and otherwise report a skip; the repository validator itself remains standard-library-only. Behavioral evaluation must separately observe decisions and forbidden side effects, not merely match headings or wording.

Project discovery links in `.agents/skills/` point to the source folders with relative symlinks. Installing or removing user-level Skills, pushing, publishing, and writing production systems are separate authorized actions.
