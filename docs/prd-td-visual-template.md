# PRD and TD visual template

Copy only the sections that apply, but retain the diagram manifest and account for
every core diagram family as `present` or `N/A` under the
[PRD and TD visual documentation contract](prd-td-visual-contract.md).

## Document control

| Field | Value |
| --- | --- |
| Document ID | `PRD-...` or `TD-...` |
| Title |  |
| Status | draft / proposed / approved / superseded |
| Owner |  |
| Source or revision | issue, brief, commit, or document revision |
| Updated | YYYY-MM-DD |
| Scope |  |
| Supersedes | `N/A` or document ID |

## Human review layer

### Problem, actors, and outcome

- Problem and current evidence:
- Human/Agent actors:
- Desired observable outcome:
- Why now:

### Scope and decision

- In scope:
- Non-goals:
- Hard constraints:
- Selected direction and why:
- Material alternative and rejection reason:
- Top risks, assumptions, and open decisions:

## Agent execution contract

### Requirements

| ID | Actor | Trigger/preconditions | Behavior | Inputs/outputs | Success | Failure/recovery | Invariants | Acceptance/evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `FR-001` |  |  |  |  |  |  |  |  |

### Quality requirements

| ID | Attribute | Workload and threshold | Measurement | Design consequence |
| --- | --- | --- | --- | --- |
| `NFR-001` | reliability / latency / security / cost / ... |  |  |  |

### Authoritative contracts

| Contract ID | Type | Location/revision | Producer/owner | Consumers | Compatibility rule |
| --- | --- | --- | --- | --- | --- |
| `API-001` | OpenAPI / AsyncAPI / schema / migration / policy |  |  |  |  |

## Diagram manifest

| ID | Type | Coverage | Question answered | Scope/viewpoint | Audience | Requirement/ADR IDs | Source | Status/revision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `D-01` | concept mind map | present | What concepts must stay distinct? | product/domain | human + Agent |  | inline Mermaid |  |
| `D-02` | system context | present | Who interacts with the system and what is outside it? | target system | human + Agent |  | inline Mermaid |  |
| `D-03` | ER | present or `N/A: reason` | What entities, ownership, and cardinalities exist? | conceptual/logical/physical | human + Agent |  | inline Mermaid |  |
| `D-04` | component/class | present or `N/A: reason` | Which components own behavior and dependencies? | functional/container/component/code | human + Agent |  | inline Mermaid |  |
| `D-05` | sequence | present or `N/A: reason` | How does a named scenario succeed or fail over time? | named scenario | human + Agent |  | inline Mermaid |  |
| `D-06` | state machine | present or `N/A: reason` | Which lifecycle transitions are allowed? | named object/workflow | human + Agent |  | inline Mermaid |  |
| `D-07` | user journey/activity | present or `N/A: reason` | How does an actor reach value and recover? | named actor and outcome | human + Agent |  | inline Mermaid |  |

Add conditional deployment/network, data-flow/trust, identity/access,
availability/resilience, or requirement-trace views when their trigger exists.

## Visuals

Replace labels with domain terms and stable IDs. These are semantic skeletons,
not a sample solution.

### D-01 — Concept mind map

Question: What concepts must reviewers and implementers keep distinct?

```mermaid
mindmap
  root((Product or bounded problem))
    Actors
      Human role
      Agent role
    Outcomes
      FR-001 observable value
    Domain
      Entity
      Rule
      State
    Integrations
      External system
    Risks and unknowns
      RISK-001
      OPEN-001
```

Figure D-01. Concept decomposition; leaves link to formal definitions below.

### D-02 — System context

Question: Who interacts with the system, and what is outside its boundary?

```mermaid
flowchart LR
  person["Person<br/>Desired outcome"]
  agent["Agent<br/>Authorized task"]
  external["External system<br/>Owned elsewhere"]
  subgraph scope["System in scope — purpose"]
    system["System<br/>Black box at context level"]
  end
  person -->|"initiates FR-001"| system
  agent -->|"executes under policy POL-001"| system
  system -->|"sends/receives via contract API-001"| external
```

Figure D-02. System context and external interaction purposes.

### D-03 — ER diagram

Question: What are the authoritative entities and their cardinalities?

```mermaid
erDiagram
  PARENT ||--o{ CHILD : owns
  PARENT {
    uuid id PK
    string natural_key UK
    string state
  }
  CHILD {
    uuid id PK
    uuid parent_id FK
  }
```

Figure D-03. Logical or physical data model; label the level in the narrative.

### D-04 — Component/class diagram

Question: Which components own the behavior and how may they depend on each other?

```mermaid
classDiagram
  direction LR
  class EntryPoint {
    <<component>>
    +handle(command)
  }
  class DomainService {
    <<component>>
    +execute(FR-001)
  }
  class Repository {
    <<interface>>
    +load(id)
    +save(entity)
  }
  EntryPoint --> DomainService : invokes
  DomainService --> Repository : requires
```

Figure D-04. One component abstraction level with responsibilities and directed
dependencies.

### D-05 — Sequence diagram

Question: How does the critical scenario succeed or fail over time?

```mermaid
sequenceDiagram
  actor User
  participant Entry as Entry point
  participant Service as Domain service
  participant Store as Authoritative store
  User->>Entry: command (API-001)
  Entry->>Entry: validate and authorize (POL-001)
  Entry->>Service: execute FR-001
  Service->>Store: conditional write
  alt accepted
    Store-->>Service: committed revision
    Service-->>User: success outcome
  else conflict, timeout, or rejection
    Store-->>Service: typed failure
    Service-->>User: safe failure and recovery action
  end
```

Figure D-05. Critical success and material failure behavior.

### D-06 — State machine

Question: What lifecycle transitions are allowed for the core object?

```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Submitted: submit [valid] / persist request
  Draft --> Draft: submit [invalid] / return violations
  Submitted --> Completed: complete [work committed] / publish result
  Submitted --> Cancelled: cancel [cancellable] / compensate
  Submitted --> Failed: timeout [retry exhausted] / preserve evidence
  Completed --> [*]
  Cancelled --> [*]
  Failed --> [*]
```

Figure D-06. Core lifecycle using `event [guard] / effect` transitions.

### D-07 — User journey or activity flow

Question: How does the actor reach value and recover from a blocked path?

```mermaid
flowchart LR
  start(["Actor enters"]) --> act["Performs FR-001 action"]
  act --> decision{"Accepted?"}
  decision -->|Yes| feedback["Receives success feedback"]
  feedback --> done(["Outcome achieved"])
  decision -->|No| recovery["Receives reason and recovery action"]
  recovery --> act
```

Figure D-07. Actor journey, feedback, and recovery.

## Decisions and risks

| ADR/Risk ID | Context or trigger | Options/impact | Decision/response | Status/owner | Recheck or supersession condition |
| --- | --- | --- | --- | --- | --- |
| `ADR-001` |  |  |  | proposed |  |
| `RISK-001` |  |  |  | open |  |

## Traceability and delivery

| Outcome/source | Requirement | Figures/contracts/ADR | Work package | Verification | Status |
| --- | --- | --- | --- | --- | --- |
|  | `FR-001` | `D-02`, `D-05`, `API-001` |  |  | planned |

### Rollout, rollback, and operations

- Migration and compatibility:
- Rollout stages and abort signals:
- Rollback or replacement seam:
- Observability and alert evidence:
- Security/privacy/data handling:

### Review evidence

- Renderer and version:
- Rendered figures visually inspected:
- Contract/schema validation:
- Human comprehension reviewer and result:
- Agent precision/self-check or evaluation and result:
- Not run, unknown, stale, or blocked evidence:
