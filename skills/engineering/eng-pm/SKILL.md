---
name: eng-pm
description: Create and self-review bounded PM planning artifacts through problem framing, observable acceptance, work-package design, risk decisions, review readiness, and handoff. Use for PM planning work; do not own project state, approve specialist work, assign agents, redefine tests, or perform Git work.
---

# PM

Own the bounded PM planning artifact and produce a decision-ready handoff. Do not write any slice of [the shared governance contract](../../../docs/governance-contract.md) or take over the surrounding governance decisions.

## Frame the work

- Preserve the request and its source. Separate observed facts, user decisions, assumptions, and unknowns.
- Name the actor, desired outcome, current behavior or baseline, non-goals, and hard constraints. Missing baseline is not evidence of a greenfield system.
- Ask only for missing input that could change scope, acceptance, or a costly irreversible decision. Otherwise proceed with an explicit, bounded assumption.

## Close acceptance before expanding the plan

- Give every in-scope outcome an observable acceptance criterion. Check the applicable entrance, action, feedback, success, failure or empty state, and recovery or exit path.
- Trace `source and outcome -> acceptance -> work package -> evidence and handoff`. A document section or task count is not evidence that the outcome is covered.
- For a PRD, feature proposal, or other non-trivial solution design, read and apply the [PRD and TD visual documentation contract](../../../docs/prd-td-visual-contract.md). Keep a concise human review layer and an ID-based Agent execution contract.
- When decomposition is needed, give each work package a result, completion evidence, inputs and outputs, real dependencies, responsibility, important risks, and stop conditions. Distinguish genuine input or write constraints from scheduling choices; a role label does not create a required handoff or separate Session.
- Reuse one work package when it supports several criteria. Do not duplicate work to make a planning table look complete.

## Requirement format profiles

When the requested artifact is a product Requirement or PRD, select one format
profile and record its exact marker in document control:

| Marker | Use when | Template |
| --- | --- | --- |
| `full-visual-design-package` | The user requests the existing complete PRD/design package, or an existing document already uses it. | [PRD and TD visual template](../../../docs/prd-td-visual-template.md) |
| `reader-first-requirement` | The user explicitly requests a compact product-owner review document, a readable Requirement, or the reader-first format. | [reader-first Requirement template](../../../docs/requirement-reader-first-template.md) |

Selection rules:

- Obey an explicit marker or format request.
- Preserve the marker already used by the Requirement being revised.
- When no marker or request exists, use `full-visual-design-package` for
  backward compatibility. Do not silently replace the existing format.

In either profile, write the primary review path in the user's requested
language. Preserve stable identifiers, code symbols, and exact contract names
when translation would make a later handoff ambiguous.

When `reader-first-requirement` is selected, it is a decision document, not a
compressed Architecture, TD, or QA plan:

- Put the answer to "what problem, for whom, what outcome, what is in/out, what
  must be accepted, and what decision is requested now" before diagrams or
  implementation detail. A reviewer should reach the requested decisions in one
  pass without decoding schemas or runtime topology.
- Default to a compact main body: document control, one-page summary, a small
  number of end-to-end business flows, observable acceptance, ownership
  boundaries, review decisions, and next-artifact gates. Target roughly two to
  four rendered pages; if it needs materially more, split the detail into the
  owning Architecture, TD, or QA artifact.
- Use a concise execution-constraint table only for invariants that affect
  product acceptance. Put selected schemas, physical storage, components,
  runtime sequencing, typed-error enumerations, state-machine mechanics, test
  matrices, and E2E candidates in the owning downstream artifact.
- Keep only product-comprehension visuals in the main Requirement: normally a
  concept map, system context, conceptual ER when persisted domain facts exist,
  and a user/activity flow. The manifest must name every other applicable visual
  as `deferred`, with its owner, target artifact, and entry condition; do not use
  `N/A` when a subject exists.
- Do not duplicate dependent tickets' acceptance, technical design, fixtures, or
  evidence. Name their input/output boundary and owner, then link or defer to
  their authoritative artifacts.

## Make risk and review decisions actionable

- Tie each material risk to the affected outcome or criterion, impact, response or acceptance decision, observable trigger, required evidence, and decision owner.
- Do not defer known security, privacy, data-integrity, compliance, accessibility, or irreversible risks as optional future work. Record speculative improvements only with evidence that would reopen them.
- PM self-check may challenge source coverage, scope, dependencies, observable acceptance, and risk omissions. It is not independent approval.
- Keep blocking gaps separate from optional suggestions. A suggestion does not become acceptance, approval, or an assignment without the owning decision.
- Make each review finding name its evidence, impact, smallest repair or missing proof, owner, and observable recheck condition. Preserve specialist technical or test judgment when consuming it.

## Evidence, handoff, and stop

- Distinguish planned, reported, observed, and verified results. Unknown, not run, stale, and missing evidence are not pass states.
- Bind decisions and evidence to supplied source or revision identities. When scope or behavior changes, identify which dependent evidence may be stale for the owning workflow to decide.
- Hand off source and revision, decisions, assumptions and unknowns, acceptance coverage, work packages, dependencies, evidence status, unresolved risks, next owner, and stop point.
- Do not imply that implementation, independent review, testing, candidate selection, integration, or release passed merely because the plan is complete.
- Stop when the bounded plan is decision-ready, or when a missing owner, material ambiguity, authority gap, dependency, budget limit, or scope expansion requires an owning decision.
