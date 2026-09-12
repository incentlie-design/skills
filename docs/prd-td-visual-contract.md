# PRD and TD visual documentation contract

Use this contract for a product Requirement/PRD, technical design (TD),
architecture proposal, or another non-trivial design. It keeps human decisions
and Agent-executable contracts aligned without requiring a diagram package for
every document.

The words **MUST**, **SHOULD**, and **MAY** express requirement strength.

## Template ownership and resolution

Resolve the artifact shape in this order:

1. an explicit user-supplied template or reference;
2. the active repository-local template or accepted project convention;
3. the compact compatibility fallbacks in this repository.

Read only the selected template. Project-local templates own business fields,
roles, vocabulary, document locations, and lifecycle semantics; this reusable
contract owns only the cross-project information priority, diagram decision, and
review invariants. GitHub Issue/PR templates are appropriate for intake and
review entry points, while longer Requirement/PRD/TD shapes normally live with
the project's documentation. Do not copy changing project facts into this
contract or treat a central fallback as a second project authority.

## Artifact profiles

These markers apply only when an existing artifact or the selected template uses
them. Existing unmarked documents retain their project format until explicitly
migrated. A marker selects reading depth, not a mandatory set of figures.

### `full-visual-design-package`

Use when the user requests a complete design package, the existing document uses
this marker, or the project has selected it. If no project template exists, use
the [PRD and TD visual fallback](prd-td-visual-template.md). Include all contracts,
decisions, risks, and views needed to remove the material ambiguities of the
subject; do not fill a fixed diagram catalog.

### `reader-first-requirement`

Use when the Requirement is primarily a product-owner decision document. If no
project template exists, use the
[reader-first Requirement fallback](requirement-reader-first-template.md). Lead
with problem, outcome, scope, acceptance, ownership, and decisions requested now.
Technical detail belongs in a later artifact only when that artifact is actually
needed; the marker does not impose an Architecture → TD → QA sequence.

### Architecture, TD, and QA artifacts

Architecture defines selected ownership and structural decisions. TD defines the
implementation contracts, affected components, runtime behavior, lifecycle, and
failure/recovery semantics required by the change. QA maps accepted criteria and
risks to evidence. Each links the exact upstream decision it consumes and avoids
copying upstream facts. None receives a fixed figure quota from its artifact type
or author role.

## Review-first document shape

Use the project's existing structure, but make the opening reviewable in one
pass. Apply the [review and handoff information template](review-handoff-template.md):

1. exact subject/source revision;
2. proposed decision or current status;
3. blocking/material findings or open decisions;
4. required decision/action and owner.

Then provide the smallest applicable human explanation and Agent contract:
actors/outcomes, scope/non-goals, measurable acceptance, invariants, interfaces,
data or state rules, failure/recovery behavior, risks, and change impact. Use
stable IDs when several artifacts must trace the same facts. Do not create empty
sections or repeat authoritative project facts for completeness.

Every functional requirement that drives implementation SHOULD make its actor,
trigger/preconditions, observable behavior, inputs/outputs, success,
failure/recovery, invariants, and acceptance evidence locatable. Quantify quality
requirements when a threshold changes the design.

## Diagram decision

A diagram is required only when a material ambiguity in scope, ownership,
relationship, order, state, data movement, trust, deployment, or failure behavior
is clearer as a visual than as short prose or a table. Select the smallest view
that answers that ambiguity. A role or document type never requires a fixed
diagram family.

Record one of these dispositions near the relevant decision:

- `Diagram: present` with its question, mapped body/goal/risk/AC, editable source,
  and validation evidence;
- `Diagram: deferred` only when the current artifact deliberately leaves a real
  question to a named owning artifact and entry condition;
- `Diagram: N/A — <specific reason>` when no material visual ambiguity exists or
  prose/table is the clearer expression.

A concrete `N/A` names the subject and why a diagram would not change the
decision. Do not enumerate every unused diagram type. Silence is acceptable for
an ordinary localized artifact whose project format does not ask for a diagram
disposition.

## Smallest useful view

| Ambiguity to remove | Prefer | Minimum content |
| --- | --- | --- |
| Scope, external actors, or handoff ownership | Context/boundary view | In-scope subject, external parties, labelled purposes and owner boundaries |
| Domain/data ownership, cardinality, or persisted relationships | Conceptual/logical/physical ER at one declared level | Entities, relationship verbs, cardinality/optionality, authoritative owner; keys only when the level needs them |
| Component responsibility or dependency direction | Component/container view | One abstraction level, responsibilities, interfaces, directed labelled dependencies |
| Ordering, async behavior, timeout, retry, or partial failure | Sequence view | Initiator, ordered interactions, contract IDs where available, success and material failure outcome |
| Allowed lifecycle changes or rejected transitions | State view | One object/workflow, initial/terminal states, `event [guard] / effect`, rejection/recovery and atomicity when material |
| Actor value path and business recovery | Journey/activity flow | Entrance, action/decision, feedback, success, rejection/recovery, exit |
| Sensitive or cross-boundary data movement | Data-flow/trust view | Sources/sinks, transformations, classification, trust boundaries, retention/deletion when material |
| Runtime/deployment/failure-domain topology | Deployment or resilience view | Deployable units, environment/boundaries, protocols, ownership, failover/recovery constraints |
| Dense cross-artifact coverage | Trace view | Goal/risk/AC derivation, implementation/decision target, verification and uncovered edges |

A compact table or labelled prose remains preferable when it communicates the
same relationship more precisely. Do not use one generic flowchart to imply
scope, data, time, and state simultaneously.

## Content and diagram responsibility

| Capability | Content responsibility | Diagram responsibility |
| --- | --- | --- |
| PIC | Select the smallest work slice, join points, conflicting owner, and next decision | Decide whether a visual is needed for the aggregate and select the minimum view set; do not become a second design author |
| PM | Problem, actor, outcome, scope/non-goals, AC, product options and unknowns | Add only concept/context/journey/decision views needed to resolve product ambiguity |
| DEV | Call path, contracts, data, components, runtime, failure/recovery and compatibility | Add only the component/data/sequence/state/runtime view needed for an affected technical risk |
| QA/Reviewer | Judge the exact subject against supplied acceptance, risk and evidence | Verify that supplied figures match prose, contracts and implementation and can falsify critical claims; do not invent or own the design |
| PR feedback triage | Decide whether each comment is addressed, discussed, deferred, or no action | Suggest a figure only when it resolves the comment's real relationship or flow ambiguity more cheaply than prose |
| Wiki authoring | Organize accepted exact sources into derived explanations | Reuse or transform visuals for navigation/comprehension without changing canonical meaning or source ownership |

Capability boundaries do not imply a role sequence, separate Agent, approval hop,
or permission. Project assignment and native systems still determine the current
owner and authority.

## Mapping and traceability

For each selected figure, keep the following locatable in a nearby caption or a
small manifest. A manifest is useful for several figures; it is not required for
a single obvious inline figure.

| Field | Meaning |
| --- | --- |
| Figure ID and question | Stable locator and the single ambiguity it resolves |
| Scope/viewpoint | Current/target state and declared abstraction level |
| Body mapping | Exact section, goal, risk, acceptance or decision IDs supported |
| Authoritative source | Prose, schema, contract, or accepted source whose meaning the figure represents |
| Editable source | Repository path or inline source and revision |
| Status/evidence | Proposed/accepted/derived, renderer/check used, and remaining visual uncertainty |

Do not invent IDs solely to fill a table. When the project has no IDs, map to
exact headings and source revisions. A diagram does not silently override prose,
schema, contracts, or a canonical project decision.

## Authoring and Archify boundary

Keep project diagram sources text-first, diffable, editable, and source
controlled. Prefer the repository's existing notation; Mermaid, Structurizr DSL,
PlantUML, editable SVG, or another local format are acceptable when they preserve
the required semantics. A rendered bitmap, whiteboard, editor URL, or design file
must not be the only source.

Project diagram authoring MUST NOT depend on Archify. Archify MAY be selected only
by an asynchronous derived-document build, such as wiki generation, when it
improves presentation. That build must preserve exact source provenance, keep the
result derived, and MUST NOT write generated interpretations back into the
canonical diagram or design source.

Render or otherwise validate every changed diagram with the project's supported
tooling. Visually inspect readable labels, clipping, contrast, direction, and
consistency. If the environment cannot render it, report that evidence gap; do
not claim visual validation from syntax alone.

## Review checks

A design is review-ready when, for its exact subject:

- the opening decision/status, material findings, and required action are clear;
- each selected figure answers a real question and maps to the governing body,
  goal, risk, acceptance, or decision;
- names, directions, cardinalities, states, and messages agree with prose and
  executable contracts;
- changed editable sources are present and the performed render/inspection is
  reported;
- concrete `N/A` or `deferred` decisions are honest and do not hide a material
  ambiguity;
- unverified claims and residual risk remain visible.

Block on a contradiction that can change implementation or acceptance, an
unreadable required figure, missing editable source, or a false `N/A`. Treat a
cosmetic preference as a suggestion and place it after material findings.

## Research basis

This contract synthesizes ISO/IEC/IEEE 42010 viewpoints, C4's explicit scope and
labelled relationships, arc42 runtime scenarios, Kubernetes' source-controlled
diagram guidance, and Microsoft architecture-diagram/ADR guidance. Mermaid,
Structurizr, PlantUML, OpenAPI, AsyncAPI, and repository-local schema formats are
possible carriers; none is a product or provider requirement.
