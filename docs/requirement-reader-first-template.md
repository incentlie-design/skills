# Reader-first Requirement template

This is a compatibility fallback, not an active project template. Use it only
when no explicit user-supplied or repository-local template applies and a
Requirement or PRD selects `reader-first-requirement`. Projects own their
business fields, vocabulary, roles, locations, and lifecycle semantics. This is
a product decision outline, not a compressed Architecture, TD, QA plan, or fixed
delivery sequence. Delete every unused optional section.

See the [visual documentation contract](prd-td-visual-contract.md) and
[review/handoff priority](review-handoff-template.md).

## Exact subject and decision

| Field | Value |
| --- | --- |
| Document ID / title | `REQ-...`: user-visible outcome |
| Format profile | `reader-first-requirement` |
| Exact source/revision | issue, brief, or accepted requirement revision |
| Status/conclusion | draft / proposed / decision-ready / approved / superseded |
| Product owner |  |
| Scope | one sentence |
| Supersedes | omit when none |

State whether this document is authoritative or a review candidate. Link the
current authority when it is not this document.

### Material findings or open product decisions

Omit when none. Put scope/acceptance conflicts and required product decisions
here, before flows or supporting evidence.

| Decision/finding | Evidence and impact | Owner/action | Recheck |
| --- | --- | --- | --- |
|  |  |  |  |

### Required decision/action now

Name the smallest decision the product owner must accept, reject, or amend. Use
`none` only when the bounded Requirement is already decision-ready without an
open material item.

## One-page review

### Problem and outcome

- Problem and current evidence:
- Actor receiving value or making the decision:
- Desired observable outcome:
- Why now:

### Scope and selected direction

- In scope:
- Non-goals:
- Hard constraints:
- Selected product direction and reason:
- Ownership boundary handed to another artifact or dependency:

## Core business flows

Include only distinct flows that change product scope or acceptance. Each names
the trigger, business action, visible success, rejection/recovery, and acceptance
IDs. Do not specify components, queues, schemas, retry algorithms, or storage
unless the product decision depends on them.

### <Actor reaches the primary outcome>

<Trigger → action → visible result; rejection/recovery; linked AC.>

## Acceptance criteria

| ID | Observable result | Owning requirement/dependency |
| --- | --- | --- |
| `AC-001` |  |  |

Keep each row independently checkable. Detailed cases, fixtures, commands, and
executed evidence belong to QA artifacts.

## Ownership boundaries

| Topic/handoff | This Requirement owns | Owned elsewhere and exact authority |
| --- | --- | --- |
|  |  |  |

Reference dependent facts once. Do not copy another ticket's requirements,
implementation, fixture, evidence, or acceptance.

## Dependent artifacts and stop conditions

List an Architecture, TD, QA, or another artifact only when it must answer a real
question before the outcome can proceed. Order by actual input dependency; do not
impose a role or approval sequence.

| Artifact/owner | Question or bounded output | Entry/recheck condition |
| --- | --- | --- |
|  |  |  |

Return to the product owner only for a changed scope/acceptance boundary, a
material dependent-contract change, a privacy/integrity conflict, or another
decision this Requirement owns.

## Diagram disposition

Choose the smallest applicable statement:

- `Diagram: N/A — <specific reason no scope, relationship, order, state, data, trust, or failure ambiguity needs a visual>`
- `Diagram: deferred — <real technical question, owning artifact/owner, entry condition>`
- `Diagram: present — <figure ID/type and the product ambiguity it resolves>`

For present figures, keep editable source with the document and map each figure
to the body heading, outcome, risk, AC, or decision it supports. Product
Requirements typically use a context, concept, journey, or decision view, but
none is mandatory by name. Do not enumerate unused diagram types.

| ID/type | Question | Body/outcome/risk/AC mapping | Editable source/revision | Render/inspection |
| --- | --- | --- | --- | --- |
| `D-01` |  |  |  |  |

Omit the table when `Diagram: N/A` and no existing project format requires it.

## Review evidence and change impact

- Exact source checked:
- Acceptance coverage and exclusions:
- Figures/checks actually performed:
- Residual risk or unverified assumptions:
- Downstream artifacts whose evidence becomes stale if this Requirement changes:
- Optional history/P3/appendix (last; omit when empty):
