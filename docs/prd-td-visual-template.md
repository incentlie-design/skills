# PRD and TD visual template

Use this copyable template when document control selects
`full-visual-design-package`. It is complete with respect to material decisions,
not a fixed number of sections or diagrams. Delete unused optional sections; do
not leave empty tables or placeholder headings.

See the [visual documentation contract](prd-td-visual-contract.md) and
[review/handoff priority](review-handoff-template.md).

## Exact subject and review decision

| Field | Value |
| --- | --- |
| Document ID / title |  |
| Format profile | `full-visual-design-package` |
| Exact subject/source revision | issue, brief, commit, or document revision |
| Status/conclusion | draft / proposed / review-ready / approved / superseded |
| Owner |  |
| Scope |  |
| Supersedes | omit when none |

### Material findings or open decisions

Omit when none. Put each blocking/material item before design detail:

| Finding/decision | Evidence and impact | Required owner/action | Recheck |
| --- | --- | --- | --- |
|  |  |  |  |

### Required action

State the decision or review action required now. Use `none` only for a bounded
clean result.

## Human review layer

### Problem, actors, and outcome

- Problem and current evidence:
- Actor and desired observable outcome:
- Why now:

### Scope and selected direction

- In scope / non-goals:
- Hard constraints and invariants:
- Selected direction and why:
- Material alternative and rejection reason:
- Top risks and assumptions:

## Agent execution contract

Keep only rows needed by the subject.

| ID | Trigger/preconditions | Observable behavior | Inputs/outputs | Success | Failure/recovery | Invariants | Acceptance/evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `FR-001` |  |  |  |  |  |  |  |

Link authoritative API, message, schema, migration, or policy contracts instead
of copying them. Add quantified quality requirements only when they change the
design.

## Decisions and risks

| ID | Context/trigger | Decision or response | Owner/status | Recheck or supersession condition |
| --- | --- | --- | --- | --- |
| `ADR-001` / `RISK-001` |  |  |  |  |

## Diagram disposition

Choose one:

- `Diagram: N/A — <specific reason no visual ambiguity exists or prose/table is clearer>`
- `Diagram: deferred — <real question, owning artifact/owner, entry condition>`
- `Diagram: present — see selected-figure manifest below`

Do not list unused diagram families. Select the smallest type from the contract's
ambiguity table.

### Selected-figure manifest

Include only when one or more figures are present.

| ID/type | Question and scope | Body/goal/risk/AC mapping | Authoritative source | Editable source/revision | Render/inspection status |
| --- | --- | --- | --- | --- | --- |
| `D-01` |  |  |  | inline or repository path |  |

### Selected figures

For each figure: introduce the question, include or link the editable source,
give a short caption, and state the decision/invariant it supports. Split figures
that mix abstraction levels or try to express scope, data, order, and state at
once.

## Traceability and delivery

Use when several requirements or artifacts need cross-reference.

| Outcome/source | Requirement/decision | Figure/contract | Work package or implementation | Verification/status |
| --- | --- | --- | --- | --- |
|  | `FR-001` |  |  |  |

Record rollout, compatibility, rollback/replacement, operations, and data
handling only when the subject creates those concerns.

## Evidence and change impact

- Exact source checked:
- Checks/rendering actually performed:
- Coverage and exclusions:
- Residual risk or unverified claims:
- Downstream evidence made stale by a change:
- Optional P3/nits/appendix (last; omit when empty):
