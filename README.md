# skill-creator

A public source repository for ten orthogonal engineering Skills (four state-owning governance Skills, two advisors, three artifact-owning role Skills, and one documentation-authoring Skill) plus a separate **content catalog**. Content Skills live under `skills/content/` and are **not** counted against that engineering closed set.

## Constrain actions, not orchestration

The Agent decides how to organize work within the user's request and authority. Skills constrain the actions it chooses: when a rule applies, which facts or permissions that action needs, what is forbidden, and what evidence supports the result. They do not install a lifecycle, prescribe a role sequence, or require separate Sessions and approval hops.

Loading a Skill does not require creating its objects. A normal local change can remain in the current task and use a suitable branch, focused checks, and a concise result. It does not need a WorkItem, assignment packet, budget, lease, milestone, or release window unless the requested action or actual project policy needs one.

## Action routing

| Chosen action | Skill | Constraint and evidence |
| --- | --- | --- |
| Compare zero-to-one product or architecture paths | [Closed Loop](skills/engineering/eng-closed-loop-decisions/SKILL.md) | Recommend the smallest clean actor-to-evidence loop; advice does not change canonical state or authorize implementation |
| Disposition PR or MR feedback and draft evidence-backed responses | [PR feedback triage](skills/engineering/eng-pr-feedback-triage/SKILL.md) | Classify each current comment as address now, discuss, defer, or no action; do not infer scope, provider-state, Git, review, or merge authority |
| Produce a bounded plan | [PM](skills/engineering/eng-pm/SKILL.md) | Preserve intent, observable acceptance, real dependencies, risks, and decision evidence |
| Implement or self-check a bounded change | [DEV](skills/engineering/eng-dev/SKILL.md) | Trace affected behavior, use the smallest complete change, and provide focused evidence |
| Evaluate evidence or review an implementation | [QA and Reviewer](skills/engineering/eng-qa-reviewer/SKILL.md) | Bind conclusions to the subject and applicable checks; preserve required independence |
| Author or restructure a dual-track project wiki/docs site | [Wiki authoring](skills/engineering/eng-wiki-authoring/SKILL.md) | Dual-audience IA, Diátaxis page types, diagram rules; does not own architecture truth or Git mutation |
| Register/update canonical work or make scope, acceptance, dependency, candidate, gate, or remote-sync decisions | [Project](skills/engineering/eng-project-governance/SKILL.md) | Preserve the authoritative source, relevant revisions, decision authority, and actual evidence |
| Delegate, create/reuse a Session, resolve shared ownership, or adopt delegated results | [Agent](skills/engineering/eng-agent-governance/SKILL.md) | Clarify scope and responsibility; prevent write conflicts and false independence; collect required outputs |
| Change multi-repository topology/dependencies or supply a reproducible tuple | [Workspace](skills/engineering/eng-workspace-governance/SKILL.md) | Identify repositories, actual dependencies, and exact consumed commits when reproduction needs them |
| Mutate Git state | [Repo](skills/engineering/eng-repo-governance/SKILL.md) | Resolve exact targets, preserve ownership and dirty state, enforce authority, and report actual resulting refs |
| Adapt, lock identity, storyboard, voice, mix, or evaluate narrated-drama content | [Content catalog](skills/content/README.md) | Distilled methods for R1–R6 production problems; not product Architecture, Git, or Provider selection |

These are routing choices, not stages. The same Agent can use compatible capabilities in any order consistent with real input dependencies, safety, and authority. A role boundary does not require a different executor except for required independence or approval authority. Read-only Git inspection does not trigger mutation governance.

Registry dependencies describe conditional owner routing, not mandatory loading or execution dependencies. The four slice owners remain exclusive; the two advisors, three role Skills, and documentation Skill own their respective artifacts, not governance state.

## Branch, project, and Session boundaries

- **Branches carry changes.** Reuse a suitable branch/worktree with clear ownership; without a project naming rule, use `codex/<change>`. Concurrent repository writers need isolated worktrees; read-only collaborators do not. Review, aggregate, and integration branches are optional, not a required chain.
- **Project records carry project facts.** Respect the selected system of record when operating on it. A missing adapter blocks its operations and dependent decisions, not all useful authorized work. Do not create a mirror or claim an unperformed task update.
- **Sessions carry execution context.** They are not acceptance records. Do not require a title/status mirror, lifecycle transitions, or one branch per Session. Creation pending or missing from a list does not justify duplicate creation.
- **Results carry dependencies.** A consumer needs the required artifact and evidence, not a terminal producer Session or a callback receipt. Account for all required outputs before claiming aggregate completion; a first completed child is not the aggregate result.
- **Changed evidence gets an impact check.** Reassess only affected inputs and claims. Do not pause all work because any upstream revision changed.
- **Cleanup remains a separate action.** Merge, archival, and acceptance are distinct. Honor explicit cleanup/archival requests or configured preferences within their exact scope; a bare merge-status statement is not a universal deletion rule.

## Shared evidence contract

The [governance contract](docs/governance-contract.md) defines four responsibility boundaries, not a machine packet. Use existing artifacts and messages, with facts required by the action: scope, locatable output, relevant revisions, checks, and limitations. A Session record does not replace project facts or exact repository evidence. No extra metadata file or handoff schema is needed.

Closed Loop and `ponytail` are complementary: the former narrows the product/architecture decision, the latter minimizes the implementation. Neither waives safety, data integrity, or explicit requirements.

## PRD and TD visual contract

Non-trivial product and technical designs follow the shared [PRD and TD visual documentation contract](docs/prd-td-visual-contract.md). It separates a human review layer from an ID-based Agent execution contract and requires a source-controlled diagram manifest covering concept, context, data, component, runtime, lifecycle, and user-flow viewpoints as applicable. PM authors the bounded requirements artifact, DEV authors the bounded technical design, and QA/Reviewer judges the supplied contract without becoming a second design owner. The [copyable template](docs/prd-td-visual-template.md) provides Mermaid-first skeletons.

## GitHub remote and branch synchronization

The canonical repository is [incentlie-design/skills](https://github.com/incentlie-design/skills), stored locally as `origin`. `eng-project-governance` owns the decision about which project branch roles/refs need synchronization and when; the table below is this project's profile for that decision. `eng-repo-governance` consumes the approved plan, resolves it to exact refspecs, validates remote state and safety, and executes only a separately authorized push. Configuring the remote does not authorize one.

| Ref role | Project decision condition | Default |
| --- | --- | --- |
| `main` | A reviewed, verified candidate is selected for stable promotion | Promote through an authorized GitHub PR; never push directly or force-push |
| `archive/*` | A named recovery baseline must survive local machine loss, the remote visibility is approved, and the archived tree passed an exposure review | Conditional push to an approved remote; keep immutable and do not silently move or delete |
| `integrate/*`, `codex/integrate/*` | Remote CI, review, or another integrator must consume the exact frozen head | Local-only otherwise; remove remotely only with separate cleanup authority |
| `governance/<change>`, `codex/<change>` and existing contributor, review, or aggregate branch patterns | An unmerged handoff must cross machines/owners, a PR or remote CI requires it, or it is approved as recovery-worthy work | Local-only after ordinary work; do not upload merely because a worktree exists |
| `release/*` | A real release-stabilization workflow explicitly uses a remote branch | Do not create or push for routine delivery |

Historical initial-publication and archive decisions remain in Git history; they are not standing authority for a later change.

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

The repository validator checks the exact ten-entry **engineering** registry, Skill frontmatter, discovery links, relative Markdown links, dependency acyclicity, and the single [behavior case collection](tests/routing_scenarios.json). If `skills/content/` exists, it also checks the content registry, source index (≤200), content Skill frontmatter, and extra discovery links. Scenario routes are unordered required owner sets, not execution sequences. It validates case structure, not Agent behavior or the meaning of the responsibility contract. Behavioral evaluation must separately observe decisions and forbidden side effects; declared cases are not claimed as executed tests.

Project discovery links in `.agents/skills/` point to the source folders with relative symlinks. All ten engineering Skills are required; content Skills may add extra links. Installing or removing user-level Skills, pushing, publishing, and writing production systems are separate authorized actions.

## Cross-project work

A change commissioned by another project retains that project’s canonical ticket, referenced by full URL in commits and handoffs. Do not mirror it into this repository’s configured task space. This does not migrate the task adapter for independent skills work. A consumer records the exact skills commit it used; discoverable links must resolve to that pinned checkout, not a moving sibling `main`. Missing optional Skills do not block operations whose required project rules are locally available.
