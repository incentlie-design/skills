---
name: eng-closed-loop-decisions
description: Advise zero-to-one product and architecture decisions toward the smallest clean end-to-end loop, using reversible defaults, progressive commitment, and evidence-triggered complexity. Use as a decision supplement when over-design or option load could delay learning; do not waive safety constraints or take over project, artifact, Git, or agent-state ownership.
---

# Closed-loop decisions

Help an Agent reduce decision load and reach observable product learning before investing in a sophisticated target architecture. Optimize for the smallest clean loop that can run, deliver value, produce evidence, and inform the next decision.

This is an advisory Skill. It does not own a slice in [the shared governance contract](../../../docs/governance-contract.md). Return a `ClosureDecision` artifact that the owning product, architecture, or project workflow may accept, revise, or reject.

## Required inputs

Identify the target user or actor, problem and desired outcome, the observable signal that would change the next decision, current assets, hard constraints, important unknowns, time or decision budget, and any known irreversible commitments. If the outcome or feedback signal is absent, return `needs_input` with only the missing essentials; do not replace them with a platform design.

Read [research basis and derived principles](references/decision-principles.md) when comparing material product or architecture options, explaining the recommendation, or deciding whether complexity is justified.

## Decision protocol

1. Express the loop as `actor → trigger → action → delivered value → observable signal → next decision`. A component demo without delivered value and feedback is not a closed loop.
2. Lock non-deferrable constraints first: trust-boundary validation, security, privacy, data integrity, compliance, accessibility basics, and any explicit reliability or compatibility requirement. Simplicity cannot remove them.
3. Trace the shortest plausible route through existing product and technical assets. Prefer reuse, native capabilities, one source of truth, fewer components and handoffs, and a vertical path over horizontal foundations built for hypothetical consumers.
4. Use closure-directed divergence: investigate the fastest viable route first and branch only when a named uncertainty could invalidate it. Return one recommendation; include at most one fallback when it protects a materially different irreversible risk.
5. Triage every proposed decision:
   - **Decide now:** it blocks the loop, protects a non-deferrable constraint, or creates a costly one-way door.
   - **Default now:** it is reversible, bounded, and a conventional choice can keep the loop moving.
   - **Defer:** its value depends on future scale, variation, or evidence; record the observable trigger that will reopen it.
   - **Reject:** it does not improve current value, learning, safety, or reversibility.
6. Choose the smallest clean vertical slice. Manual steps, coarse modules, or a replaceable implementation are acceptable when explicitly bounded. Hidden coupling, duplicate truth, unowned temporary paths, missing failure handling, and unexplained debt are not.
7. Define one runnable loop check and the smallest useful evidence signal before recommending expansion. New complexity must answer a measured constraint or a demonstrated user need.
8. Stop once the proposed path closes the loop within constraints. Do not append speculative platforms, extensibility, automation, scale work, or option catalogs.

When two routes both close the loop, prefer shorter time to evidence, fewer irreversible commitments, less accidental complexity, easier rollback or replacement, and stronger evidence per unit of effort—in that order unless the user supplies a different priority. Do not create a weighted decision framework unless one is requested.

## Close Architecture conflicts without false stops

When the current Architecture path appears unable to close an accepted goal, do
not silently narrow the goal, treat every baseline choice as immutable, or bypass
an actual invariant. Use project-defined constraint levels when supplied;
otherwise classify the conflicting statement by its real consequence:

| Level | Meaning | Default treatment |
| --- | --- | --- |
| `C0` | Non-deferrable authority, safety, privacy, compliance, data-integrity, or irreversible-effect constraint | Stop any path that would violate it |
| `C1` | Accepted product or domain invariant | Obtain the owning product/domain decision before changing it |
| `C2` | Architecture guardrail or cross-boundary ownership rule | Make the delta explicit; evidence may proceed when safely admitted, but promotion waits for acceptance |
| `C3` | Accepted but replaceable baseline design choice | Prefer it; compare the smallest safe relaxation when it cannot close the goal |
| `C4` | Local implementation detail | Let the implementing owner decide and verify it proportionally |

Add an `ArchitectureConflict` block to the `ClosureDecision` with the signed
goal/acceptance, exact current constraint and revision, level, current-path result
across the complete flow, effect, and known-consumer axes, smallest relaxed
assumption, result under that assumption, affected actions, and promotion
condition. If either result is unknown, name one falsifiable probe instead of
returning a vague blocker.

Candidate admission and promotion are separate decisions. Recommend an isolated,
bounded, reversible candidate only when it preserves `C0` and `C1`, exposes any
`C2` delta, has no unauthorized live/provider/paid/destructive effect, and can
produce decision-relevant evidence. Promotion that depends on an unaccepted delta
waits for its owner, current applicable independent evidence, and the actual
promotion authority. Return one recommendation—`retain`, `revise`,
`relax-for-candidate`, or `defer`—plus at most one fallback for a materially
different risk. Pause only affected actions; unrelated analysis and admitted
offline evidence work continue while their inputs remain current.

## Keep simple and keep clean

`Keep simple` minimizes moving parts and decisions required before the loop runs. `Keep clean` preserves explicit boundaries, one authoritative state, understandable control flow, basic failure behavior, and a credible removal or migration seam. A shortcut that makes the next iteration opaque or unsafe is not simple; it merely moves cost out of view.

For coding or implementation design, pair this Skill with `ponytail` when it is available: this Skill decides the minimum loop worth building, while `ponytail` finds the least implementation that satisfies it. If `ponytail` is unavailable, apply the same order directly: skip speculative need, reuse what exists, prefer standard or native capabilities, then add only the minimum custom implementation.

## Output and boundaries

Return one concise `ClosureDecision`. Lead with the exact decision subject, recommendation/status, the material uncertainty that could invalidate it, and the next owner/action. Put evidence, limits, and deferred detail afterward; omit empty categories instead of filling a decision ledger. Follow the [review and handoff priority](../../../docs/review-handoff-template.md) when the result is handed off.

- the actor-to-evidence loop and success signal;
- the recommended vertical path and why it closes first;
- `decide_now`, `default_now`, `defer_until`, and `reject` decisions;
- any `ArchitectureConflict`, candidate admission, promotion condition, and
  owning decision;
- clean-boundary and non-deferrable invariants;
- the first runnable check, known ceiling, rollback or replacement seam;
- unresolved risks, next evidence review, and owning workflow.

Use prose or a small table by default. Add a diagram only when scope, ownership, sequence, state, or data ambiguity would otherwise obscure the recommendation; select the smallest view under the [visual documentation contract](../../../docs/prd-td-visual-contract.md). A `ClosureDecision` does not require a diagram inventory.

Do not author or approve the final product specification or architecture, create project/task state, assign agents, perform repository mutations, redefine test semantics, or execute external writes. Load the owning product or architecture Skill for the artifact, `eng-project-governance` for canonical work and gate decisions, `eng-agent-governance` for assignments, and `eng-repo-governance` for Git mutations.

For mature migrations, safety-critical systems, known scale limits, contractual interfaces, or regulated products, preserve their explicit constraints and apply closure-first reasoning only to the smallest safe decision or experiment. Never use “MVP,” “simple,” or “temporary” to bypass a known risk.
