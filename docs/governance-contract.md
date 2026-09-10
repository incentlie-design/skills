# Governance responsibility and handoff contract

The four governance Skills have exclusive responsibility for their own state. They constrain actions; they do not prescribe the Agent's scheduling, role sequence, Session topology, or control flow. The same Agent can apply several Skills without creating separate actors or approval hops. The three artifact Skills and the closed-loop advisor own no governance slice.

## Action ownership

| Action | Owner | Required facts for that action | Boundary |
| --- | --- | --- | --- |
| Register/update canonical work; change scope, acceptance, dependencies, milestones, candidates, gates, or remote-sync intent | `eng-project-governance` | Relevant request and decision sources; canonical binding and expected revision for task writes; exact candidates, target and authority for selection | No artifact authoring, Git mechanics, or runtime Session state |
| Change cross-repository topology or dependencies; provide a reproducible tuple | `eng-workspace-governance` | Participating repositories and actual dependency facts; exact commits and launch context when reproduction or verification needs them | No repository mutations, project selection, or Session management |
| Mutate Git state in one repository | `eng-repo-governance` | Exact targets and relevant refs, dirty/worktree ownership, scope and authority; project-selected remote-sync intent for pushes | No release selection, new remote-sync intent, cross-repository dependency ownership, or Session state |
| Delegate/reassign work, manage conflicting shared ownership, or hand off/adopt results | `eng-agent-governance` | Outcome, executor, inputs/output and scope; independence, budgets and leases only when applicable | No second task system, runtime lifecycle controller, Git mechanics, or test semantics |

Ownership is a constraint on the action, not a requirement to create an object. A Skill may reference another slice but must not rewrite it. Do not create missing WorkItems, assignments, budgets, leases, or receipts solely to satisfy routing.

## Conditional routing, not execution dependencies

```text
project -> workspace -> repo
agent   -> project
agent   -> repo
```

These registry edges describe conditional routing to another owner when its action is needed. They are not startup dependencies, a loading sequence, or approval hops. Repository state never selects a release; workspace topology never creates task status; assignment observations never become a second canonical project record.

`eng-closed-loop-decisions` recommends a product/architecture path. `eng-pm`, `eng-dev`, and `eng-qa-reviewer` produce their bounded artifacts. None creates another governance slice. A role boundary requires a separate executor only when an actual independence or authority constraint demands one.

## Evidence without a packet protocol

The four slices—project, workspace, repo, and agent—are responsibility boundaries, not a required JSON format. Use existing artifacts, messages, and authoritative records. No envelope version, handoff id, or extra registry is required.

Supply the facts needed by the actual action: a release needs selection authority and exact eligible candidates, a tracker write needs its expected revision, and a result handoff needs locatable output, relevant checks, and limitations. Reference another owner's evidence instead of recreating its state. Do not invent irrelevant revisions, budgets, release targets, or consumption numbers.

An explicitly requested consumer format remains a task-specific constraint; it does not become a universal Skill protocol. Removing the repository's packet schema does not migrate or invalidate existing external records.

## Evidence, authority, and blocking

- Bind Git and reproducible workspace claims to exact commits, and external writes to expected revisions. Reassess evidence affected by changed inputs; unrelated revisions do not automatically block all work.
- Project governance classifies definition, code, and promotion dependencies. Repository governance enforces ancestry only for actual code consumption; an exact definition reference need not become a contributor's Git ancestor.
- Project governance records remote-sync intent and selected refs/timing. Repository governance validates exact local/remote revisions and authorized refspecs; it may reject unsafe intent but cannot expand it.
- Delegation, a lease, a plan, or a local commit grants no new tracker, push, publication, rewrite, cleanup, deployment, or production authority.
- A missing required fact blocks the dependent action. Continue independent authorized work where safe, without creating a substitute system of record or claiming the blocked action succeeded.
- Runtime completion, message delivery, artifact acceptance, integration, and archival are separate facts. Depend on required outputs and evidence, not titles or terminal Session states.
