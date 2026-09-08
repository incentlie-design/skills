# skill-creator

A public source repository for four orthogonal engineering-governance Skills. They coordinate delivery without assuming a particular task system, agent implementation, Git host, or Codex Project.

## Agent-centered operating model

The Agent is the execution center. It loads only the Skills needed for the current lifecycle stage, uses each loaded Skill to govern that Skill's objects, and carries the resulting references into the next stage. The same Agent may load several Skills during one task, but loading a Skill neither transfers ownership between object types nor grants additional filesystem, Git, network, tracker, or production permission.

```text
request or WorkItem
        |
        v
Agent routes the operation
        |
        +-- project decision needed ------> load eng-project-governance
        |                                  operate Project objects
        |
        +-- assignment lifecycle needed --> load eng-agent-governance
        |                                  operate Agent objects
        |
        +-- multiple repositories --------> load eng-workspace-governance
        |                                  operate Workspace objects
        |
        `-- Git mutation needed ----------> load eng-repo-governance
                                           operate Repository objects
        |
        v
handoff, release leases, gate, integrate, synchronize, or close
```

These four Skills govern execution; they do not replace the producer Skill needed to write a product requirement, architecture, implementation, test, presentation, or other domain artifact. The Agent loads that domain Skill for the artifact and loads the appropriate governance Skill for the surrounding state transition.

## Which Skill the Agent loads

“Can operate” below means the Agent may create, validate, or update that governance object within the request and supplied authority. It does not mean that loading the Skill bypasses target-system permissions.

| Agent need | Skill to load | Objects the Agent can operate while loaded | Result and boundary |
| --- | --- | --- | --- |
| Normalize raw intake, resolve or transition canonical work, select candidates/releases, decide gates, decide whether and when project branches synchronize to a remote | [`eng-project-governance`](skills/engineering/eng-project-governance/SKILL.md) | `WorkItem`, system-of-record binding, goal/architecture/task revisions, acceptance criteria, dependency and milestone decisions, candidate set, release window, pipeline gate, `RemoteSyncPlan`, project closure record | Writes only the project slice. It may select work and timing, but cannot author delivery artifacts, manage sessions, define workspace topology, construct refspecs, or run Git operations. |
| Start, supervise, block, hand off, replace, stop, or close a bounded execution assignment | [`eng-agent-governance`](skills/engineering/eng-agent-governance/SKILL.md) | Capability profile, `Assignment`, `Session`, context revision binding, read/write scope, budget, independence rule, `OwnershipLease`, blocked record, handoff, lease release and closure record | Writes only the agent slice. A lease coordinates ownership but is not permission. WorkItem transitions go to Project; branches, commits, worktrees, and cleanup go to Repo. |
| Compose or reproduce a deliverable spanning more than one repository | [`eng-workspace-governance`](skills/engineering/eng-workspace-governance/SKILL.md) | `WorkspaceManifest`, exact repository tuple, source-fact ledger, cross-repository `ChangeSet`, dependency edge/DAG, launch context, frozen manifest revision, handoff and integration order | Writes only the workspace slice. It can order repository work but cannot mutate a repository, create project state, or manage the Agent lifecycle. Do not load it for an ordinary single-repository task. |
| Create or mutate Git state in one repository | [`eng-repo-governance`](skills/engineering/eng-repo-governance/SKILL.md) | Repository profile, exact base/head, branch and worktree, dirty/write scope, mutation record, handoff commit, freeze record, integration/promotion evidence, approved remote-sync execution, rewrite or cleanup decision | Writes only the repo slice. It executes exact Git mechanics but cannot select candidates, release timing, remote-sync need/branches, cross-repository dependencies, or Agent state. Read-only `status`, `diff`, `log`, and `show` do not load this mutation workflow. |

The selection rule is object-based:

- If the Agent changes a **WorkItem or delivery decision**, load Project.
- If the Agent changes an **Assignment, Session, Lease, budget, handoff, or closure state**, load Agent.
- If the Agent changes a **multi-repository manifest, exact tuple, or dependency order**, load Workspace.
- If the Agent changes a **branch, worktree, commit, merge, tag, remote ref, rewrite, or cleanup target**, load Repo.
- If one request changes several object types, load the corresponding Skills in sequence and keep their outputs in separate contract slices.

## Agent lifecycle and Skill composition

| Lifecycle stage | Agent action | Skill loading and object transition |
| --- | --- | --- |
| 1. Intake and binding | Determine whether the request already has a canonical WorkItem and current acceptance/context revisions. | Load Project when intake, project state, release, or remote-sync decisions are missing or changing. Project returns `work_item_ref` and current project references. |
| 2. Assignment start | Bind an executor/capability, scope, budget, independence, stop conditions, and ownership leases to the current WorkItem revision. | Load Agent. The assignment remains `ready` until required ownership and authority exist, then becomes `running`. |
| 3. Execution context | Identify the concrete artifact inputs and repository scope. | Load Workspace only for multiple repositories to freeze exact commits and dependency order. Load the relevant domain Skill to create or review the actual artifact. |
| 4. Durable repository work | Materialize authorized changes as branches, worktrees, commits, handoff commits, or integration candidates. | Load Repo for every Git mutation. Repo records exact before/after refs; the Agent lifecycle only references that repo evidence. |
| 5. Block or handoff | Report actual output, evidence, remaining work, risk, budget, and clean/dirty state. | Load Agent to move to `blocked`, `handoff`, `complete`, or `stopped`, and release or explicitly transfer leases. It does not silently create a replacement Agent. |
| 6. Select and integrate | Decide which candidates enter a target; for multi-repo work, preserve the frozen tuple and order; integrate exact verified heads. | Load Project for selection/gates, Workspace for cross-repo ordering, and Repo for Git integration/promotion. No one Skill claims all three decisions. |
| 7. Remote synchronization | Decide whether a project branch must cross the remote boundary, then execute the named update. | Project creates or revises `RemoteSyncPlan`; Repo validates exact local/remote revisions and separately authorized refspecs, executes the push, and records the result. Agent only carries the references and reports status. |
| 8. Closure and cleanup | Close the assignment and project decision, then consider repository cleanup as a separate operation. | Agent releases leases and records closure; Project closes the WorkItem when current acceptance/gates allow; Repo cleans exact Git targets only with separate evidence and authority. |

The delegated Agent lifecycle is explicit:

```text
ready --> running --> handoff --> complete
            |            |
            v            `--------> stopped
         blocked --> running / handoff / stopped
```

A context revision change pauses the assignment until Project records whether it remains valid. Budget exhaustion, replacement, success, block, or stop always produces a handoff and lease-release decision; an ended process never implies that its ownership lease was released.

## Contract carried by the Agent

The Agent exchanges one shared envelope defined by the [responsibility and composition contract](docs/governance-contract.md) and [machine-readable schema](contracts/governance-handoff.schema.json). It includes only the slices needed for the current route:

```json
{
  "schema_version": 1,
  "handoff_id": "handoff:example-42",
  "slices": {
    "project": {"work_item_ref": "tracker:42", "release_target": "window-1"},
    "workspace": {"manifest_ref": "workspace:r3"},
    "repo": {"repo_id": "service-a", "head_commit": "0123456"},
    "agent": {"session_id": "session-9", "status": "handoff"}
  }
}
```

The abbreviated example shows identity, not a schema-valid complete packet. An included slice must contain all required fields from the schema.

| Loaded Skill | Slice it may write | Other slices it may consume by reference |
| --- | --- | --- |
| Project | `project` | Workspace facts when delivery spans repositories; Repo execution evidence returned through the delivery route |
| Workspace | `workspace` | Project change/release references; Repo exact-state evidence for each participating repository |
| Repo | `repo` | Project candidate or `RemoteSyncPlan`; Workspace repository tuple/order |
| Agent | `agent` | Project-selected WorkItem/context; Repo handoff/cleanliness evidence |

The contract enforces five lifecycle rules:

- **One writer per slice:** loading multiple Skills does not merge their ownership. The Agent changes an object only while operating under its owning Skill.
- **Exact context:** project/external decisions bind to explicit revisions; workspace and repository facts bind to exact commits. Floating or merely planned state is not completed evidence.
- **Stale evidence stops progression:** changed goal, architecture, task, candidate, manifest, base, or head revisions invalidate dependent assignment, gate, or execution evidence until the owning Skill records an impact decision.
- **Authority remains separate:** assignment, lease, plan, local commit, or handoff does not authorize tracker writes, push, tag publication, history rewrite, cleanup, deployment, or production changes.
- **Lifecycle closes explicitly:** missing ownership, authority, exact refs, or system of record returns `needs_input` or `blocked`; every ended Agent session records its handoff and released or transferred leases.

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
