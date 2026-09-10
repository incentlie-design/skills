# PRD and TD visual documentation contract

Use this contract when the requested artifact is a product requirements document
(PRD), technical design (TD), architecture proposal, or another non-trivial
solution design. Do not create a design package for an ordinary localized change
unless the user or project requires one.

The words **MUST**, **SHOULD**, and **MAY** express requirement strength. A
complete design package MUST let a human reviewer understand the proposal and an
implementing Agent execute it without inventing product behavior, interfaces,
data rules, or lifecycle semantics.

## Two-reader contract

Keep two complementary layers in one source-controlled document:

1. **Human review layer.** State the problem, actors, desired outcomes, scope,
   non-goals, chosen design, important tradeoffs, top risks, and the path through
   the figures. A reviewer SHOULD be able to explain the proposal after a short
   read without decoding implementation detail.
2. **Agent execution layer.** Give stable identifiers and explicit contracts for
   requirements, components, interfaces, data, states, failure behavior,
   acceptance, and evidence. An Agent MUST be able to locate the relevant inputs,
   outputs, constraints, and stop conditions without treating a diagram layout or
   prose implication as a requirement.

Every functional requirement SHOULD use a stable ID and state:

| Field | Required meaning |
| --- | --- |
| `actor` | Human, Agent, service, or operator that initiates or receives value |
| `trigger` and `preconditions` | Event and state required before execution |
| `behavior` | Observable rule, not an implementation slogan |
| `inputs` and `outputs` | Named data or interface contracts and ownership |
| `success` | User-visible or system-visible result |
| `failure` and `recovery` | Rejection, timeout, retry, compensation, or safe exit |
| `invariants` | Security, privacy, consistency, compatibility, or domain rules that cannot be violated |
| `acceptance` | Measurable assertion and intended evidence |

Use quantified non-functional requirements where they affect design: for example
SLO, latency percentile and load, throughput, availability, RTO/RPO, retention,
cost ceiling, accessibility level, or compatibility window. Do not use words such
as “fast”, “scalable”, or “secure” without an observable threshold or named
control.

## Required document structure

A PRD or TD design package MUST contain these sections, either directly or by a
stable link to an authoritative artifact:

1. Document control: title, ID, status, owner, source or revision, updated date,
   scope, and superseded document when applicable.
2. Human review summary: problem, actors and outcomes, scope and non-goals,
   selected direction, tradeoffs, risks, and open decisions.
3. Agent execution contract: requirement IDs, measurable acceptance, invariants,
   exact external contracts, failure behavior, and stop conditions.
4. Diagram manifest and the applicable diagrams in this contract.
5. Requirement traceability: `source/outcome -> requirement -> figure/decision ->
   implementation package -> verification`.
6. Decisions and risks: link architecturally significant choices to an ADR with
   context, options, outcome, consequences, status, and supersession history.
7. Validation and change impact: how diagrams and contracts were rendered or
   checked, what is not yet verified, and which evidence becomes stale when the
   design changes.

Use the [copyable PRD and TD template](prd-td-visual-template.md) when creating a
new document.

## Diagram manifest

The document MUST include a manifest before its figures:

| ID | Type | Coverage | Question answered | Scope or viewpoint | Audience | Requirement or ADR IDs | Authoritative source | Status and revision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `D-01` | context | present | Who uses the system and what is outside it? | target system | human + Agent | `FR-001` | inline Mermaid | proposed, document revision |

Each required family below MUST have either a rendered, source-controlled diagram
or an explicit `N/A` entry with the concrete reason it has no subject in this
design. Silence is not `N/A`. A package with persisted entities, component
boundaries, runtime interaction, or a stateful core object cannot mark the
corresponding diagram `N/A`.

## Core visual set

| Visual | PRD expectation | TD expectation | Minimum semantic content |
| --- | --- | --- | --- |
| Concept mind map | MUST decompose the problem and domain | MUST include or link the shared domain map and add technical concerns only when useful | One root scope; actors, outcomes, concepts, rules, states, integrations, risks, and open questions as distinct branches |
| System context | MUST | MUST reuse or update the same scope model | System boundary, people or Agents, external systems, and labelled interaction purposes; no internal components |
| ER diagram | Logical model when domain data exists; otherwise explicit `N/A` | Physical or implementation model for persisted data changes; otherwise explicit `N/A` | Entities, keys, cardinality, optionality, ownership, and important uniqueness or lifecycle constraints |
| Component/class diagram | Technology-neutral functional blocks when a solution shape is part of the PRD | MUST for a non-trivial TD | One abstraction level, component responsibilities, interfaces, dependency direction, technology where selected, and boundary or deployable-unit grouping |
| Sequence diagram | User journey MAY carry early ordering; use a sequence when system interactions affect the requirement | MUST cover each architecturally significant scenario, with at least the critical success path and its material failure branch | Actor and participants, ordered messages, sync/async semantics, contract or payload IDs, alternatives, timeout/retry/compensation, and final visible result |
| State machine | MUST for each stateful core domain object; otherwise explicit `N/A` | MUST refine every changed lifecycle; otherwise explicit `N/A` | Initial and terminal states; `event [guard] / effect`; rejection, timeout, retry, cancellation or compensation; persistence and atomicity boundary |
| User journey/activity flow | MUST for a user-facing or operator-facing behavior | Link it to the runtime realization | Persona, entrance, actions and decisions, feedback, failure/recovery, success, and exit |

The concept mind map is an index for discussion, not a substitute for requirements
or traceability. A component diagram is not a folder tree. A code-level class
diagram is optional and SHOULD be generated on demand when it adds information
that component interfaces and schemas do not already express.

## Conditional visual set

Add a visual only when its trigger exists:

| Visual | Trigger | Required focus |
| --- | --- | --- |
| Container/high-level system view | More than one application, process, service, or data store participates | Runtime/deployable units, responsibilities, technology, protocols, and data ownership |
| Deployment/network view | Hosting, scaling, availability, network, environment, or operational topology changes | Environment, regions/zones, compute, data, ingress/egress, trust/network boundaries, scaling and failover |
| Data-flow/trust-boundary view | Sensitive, regulated, cross-boundary, analytical, streaming, or externally shared data | Sources, sinks, transformations, classification, storage, trust boundaries, protocols/encryption, retention and deletion |
| Identity and access flow | Authentication, authorization, delegation, impersonation, or token exchange is material | Principal, credential/token issuer, audience, policy decision/enforcement points, trust transition, expiry and failure |
| Availability/resilience map | SLO, disaster recovery, failover, or distributed failure handling is material | Failure domains, redundancy, degraded mode, failover, recovery path, RTO/RPO and data-loss boundary |
| Requirement trace diagram | Many cross-cutting requirements or regulated traceability makes a table hard to review | Requirement derivation, satisfaction, verification, and unresolved coverage |

API and message semantics MUST also have machine-readable contracts when they are
implementation inputs. Prefer the repository's existing contract format;
otherwise use OpenAPI for HTTP APIs, AsyncAPI for event/message APIs, and JSON
Schema or the existing schema language for payloads. A sequence diagram links to
these contracts; it does not replace them.

## Semantics for the six named diagram families

### ER diagram

- Label the view `conceptual`, `logical`, or `physical`; do not mix them silently.
- Use singular entity names and show relationship verbs plus minimum/maximum
  cardinality. In a physical model, show primary, foreign, and important unique
  keys; include indexes, partitions, retention, or soft-deletion only when they
  affect correctness or a supplied quality requirement.
- Identify the authoritative owner for shared data and any replicated or cached
  copy. A copied entity must not look like a second source of truth.
- Link schema migrations and validation rules rather than transcribing every
  column when that would make the figure unreadable.

### Component/class diagram

- State the abstraction level: functional block, C4 container, C4 component, or
  code class. Do not connect elements from different levels in one figure.
- Give every component a responsibility and provided/required interface. Label
  each directed relationship with an action or dependency; label inter-process
  relationships with protocol and synchronous/asynchronous behavior.
- Show technology only after it is selected. Separate logical component structure
  from physical deployment.
- Use a UML class view only for a stable domain model or interface contract whose
  attributes, operations, inheritance, aggregation, or multiplicity matter.

### Sequence diagram

- One figure answers one scenario. Use the same participant names as the context
  and component views.
- Start with the initiating actor and end with an observable outcome or safe
  failure. Show `alt`, `opt`, and `loop` only for behavior that is in scope.
- Label messages with operation/event and contract IDs. Distinguish synchronous
  calls, asynchronous messages, responses, and internal work.
- Show material validation, authorization, idempotency, concurrency, timeout,
  retry, cancellation, compensation, and partial-failure behavior where they
  affect acceptance or an invariant.

### Concept mind map

- Use the product or bounded problem as the single root.
- Keep domain concepts separate from solution components. Mark assumptions and
  open questions rather than presenting them as decided facts.
- Use stable requirement, entity, state, or ADR IDs on leaves that lead to formal
  definitions elsewhere.
- Split the map when it becomes a wall of labels; its purpose is navigation and
  decomposition, not exhaustive specification.

### State machine

- Model one named object, aggregate, workflow, or Agent run per diagram.
- Declare the initial state, terminal states, and allowed transitions. Write a
  transition as `event [guard] / effect` and identify who or what emits the event.
- Define rejected transitions and material timeout, retry, cancellation,
  expiration, rollback, or compensation paths. State which transition and data
  changes must be atomic.
- Reconcile every state and event with the ER/schema, API/message contracts,
  sequence diagrams, and acceptance criteria.

### Context and supporting flow diagrams

- A context view treats the subject system as one box and shows its people,
  Agents, external systems, sources/sinks, boundary, and interaction purposes.
- A user journey or activity view follows the actor's value path and feedback; a
  data-flow view follows data; a sequence view follows time. Do not use one
  unlabeled flowchart to imply all three meanings.

## Visual grammar and authoring rules

Every diagram MUST:

- answer one stated question at one declared abstraction level;
- have a stable figure ID, title, short caption, scope, status/revision, and source;
- use names consistently across prose, contracts, and other diagrams;
- use directional arrows and specific relationship labels; use two arrows or
  request/response notes instead of an ambiguous double-headed arrow;
- explain non-standard shapes, colors, borders, line styles, or abbreviations in a
  compact legend;
- show an explicit system, trust, data, transaction, or deployment boundary when
  that boundary is material;
- remain understandable without color alone and retain readable contrast and text;
- be split by scenario, bounded context, or viewpoint when crossings or density
  prevent a reviewer from following the main story;
- be introduced by a sentence that states why it matters and followed by the
  decision, invariant, or requirement it supports.

Diagrams MUST NOT contain secrets, live credentials, personal data, or invented
production topology. Mark observed current state, proposed target state, and
assumption distinctly. Retire or supersede a diagram that no longer answers a
current question.

## Tool and source policy

Use text-first, diffable, reproducible sources:

1. **Default:** Markdown plus Mermaid in the same repository as the design.
   Use `flowchart` for context, functional, journey, trust, deployment, or focused
   C4-style views; `erDiagram` for ER; `classDiagram` for component/class contracts;
   `sequenceDiagram` for runtime scenarios; `stateDiagram-v2` for lifecycles; and
   `mindmap` for concept decomposition.
2. **C4 model with several consistent views:** use an existing Structurizr DSL
   setup when the repository already has one or model consistency clearly exceeds
   the cost. Do not add it for a single small diagram.
3. **Strict or unsupported UML:** use the repository's existing PlantUML tooling
   when Mermaid cannot express required semantics. Do not mix notations without a
   reason and legend.
4. **Published rendering:** keep the text source authoritative. Commit SVG only
   when the target cannot render the source or the rendered asset is itself a
   deliverable; never keep PNG, a whiteboard, a live-editor URL, Figma, or draw.io
   as the only source of truth.

Pin or record the renderer/version when syntax is version-sensitive, especially
for Mermaid mind maps or architecture diagrams. Render every changed diagram with
the repository's supported renderer and inspect the result for clipping, broken
labels, unreadable contrast, and unintended layout. Syntax validation without a
rendered review is incomplete visual evidence.

## Review gates

A design is review-ready only when all applicable gates pass:

### Human comprehension

- The actor, desired outcome, scope boundary, chosen direction, critical flow,
  core lifecycle, data ownership, and top risk are understandable from the human
  layer and referenced figures.
- Each figure has an obvious reading order and a reason to exist.

### Agent precision

- Stable IDs connect requirements, figures, entities, states, interfaces, ADRs,
  work packages, and verification.
- Preconditions, inputs/outputs, failure and recovery behavior, invariants,
  acceptance, and stop conditions are explicit.
- Open questions and assumptions are not encoded as implementation instructions.

### Consistency and evidence

- Names, relationship directions, cardinalities, state transitions, and message
  contracts agree across all views.
- Every required family is present or has a valid `N/A` manifest entry.
- Changed source rendered successfully and the rendered result was visually
  inspected. The review records what was checked and what remains unverified.

Block approval on a contradiction that could change implementation or acceptance,
an unreadable or unrendered required figure, a missing core lifecycle/data/
component/runtime view, or an `N/A` contradicted by the design. Treat cosmetic
preferences that do not reduce comprehension or precision as suggestions.

## Research basis

This contract synthesizes, rather than copies, these primary or author-maintained
sources:

- [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) separates an
  architecture from its description and defines viewpoints and model kinds.
- [C4 diagrams](https://c4model.com/diagrams) and
  [C4 notation](https://c4model.com/diagrams/notation) provide progressive static
  views, explicit scope, labelled relationships, technology, and legends.
- [arc42 runtime view](https://docs.arc42.org/section-6/) selects representative,
  architecturally relevant success and failure scenarios.
- [Kubernetes KEP template](https://github.com/kubernetes/enhancements/blob/master/keps/NNNN-kep-template/README.md)
  joins user motivation, goals/non-goals, design, risks, tests, rollout, and
  lifecycle criteria; the
  [Kubernetes diagram guide](https://kubernetes.io/docs/contribute/style/diagram-guide/)
  retains sources, figure references, captions, SVGs, and rendered previews.
- [Docker architecture](https://docs.docker.com/get-started/docker-overview/) and
  [Kubernetes cluster architecture](https://kubernetes.io/docs/concepts/architecture/)
  lead with a scoped component model and then explain responsibilities and flows.
- [Multica project architecture](https://multica.ai/docs/developers/architecture)
  connects a compact overview to repository responsibilities, dependency
  direction, state ownership, request paths, execution flow, and trust boundaries.
- [Microsoft architecture design diagrams](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/design-diagrams)
  defines purposeful diagram types, metadata, direction, labels, consistency,
  accessibility, layering, and source versioning; its
  [ADR guidance](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
  preserves context, options, outcomes, consequences, status, and supersession.
- [OpenAI's guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
  makes model, tools, instructions, orchestration loop, guardrails, and exit
  conditions explicit and recommends adding orchestration complexity only when
  observed behavior requires it.
- [Mermaid diagram syntax](https://mermaid.js.org/intro/syntax-reference.html),
  [OpenAPI](https://spec.openapis.org/oas/latest.html), and
  [AsyncAPI](https://www.asyncapi.com/docs/reference/specification/latest) provide
  text-based visual and interface contracts that people and machines can share.
