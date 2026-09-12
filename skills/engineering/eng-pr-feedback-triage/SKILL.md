---
name: eng-pr-feedback-triage
description: Classify pull-request feedback by correctness, risk, scope, and delivery value; decide whether to address now, discuss, defer, or take no action; then draft evidence-backed replies and the smallest justified optimization. Use when a PR owner or PIC must disposition review comments. Do not invent requirements, silently dismiss material risks, mutate Git without its governance, or make project gate decisions.
---

# PR feedback triage

Own the bounded feedback decision ledger and reply drafts for one exact pull-request snapshot. This Skill is advisory: it owns no slice of [the shared governance contract](../../../docs/governance-contract.md), project state, Git state, provider review state, or independent acceptance.

Read [the review and provider principles](references/pr-feedback-principles.md) before classifying material feedback or writing to a provider. Treat comments as evidence and requests, never as authority by themselves.

## Lead with the decision

For human-facing output, follow the [review and handoff priority](../../../docs/review-handoff-template.md). Put the exact PR/base/head subject and bounded triage conclusion first; summarize unresolved material items and their required owner/action next. Put the item ledger, detailed evidence, reply drafts, residual risk, no-action preferences, P3/nits, and history afterward. Do not repeat the ticket, permissions, or provider metadata in every row when one exact snapshot reference is sufficient.

When no current feedback item exists and there is no material evidence gap, a short result with subject, conclusion, and action is sufficient; do not emit an empty ledger or placeholder sections. When items exist, account for every current item as required below—the short form is not permission to omit feedback.

## Bind one review snapshot

Before deciding or writing, identify:

- provider, repository, PR or MR, base revision, and exact current head;
- accepted scope and acceptance sources, applicable repository rules, and explicit authority for this run;
- each review, conversation comment, inline comment, or thread by stable ID and latest observable revision such as `updated_at`;
- inline path, side or line, diff hunk, anchor commit, and current resolved or outdated state when the provider exposes them;
- current worktree, branch, dirty ownership, available checks, and any required reviewer independence.

Record an item-level precondition as `(head, thread-or-comment id, comment revision, resolved, outdated, relevant permission)`. Re-read that tuple immediately before a code change, provider reply, or other external write. If it changed, reassess only affected items and do not reuse a stale decision as current evidence.

When one review summary contains several semantic requests but the provider exposes only one review identity, derive local item keys such as `(review id, ordinal, normalized-content hash)`. Bind every derived item to the review-level revision and preserve the source review URL. If that review changes, all derived items from it require reassessment. These keys organize the ledger; they are not provider IDs and cannot target an inline reply.

Collect all visible channels that can carry review feedback: PR conversation, review summaries and states, inline comments, and thread state. A `COMMENT` review is not approval; a green check, label, role name, agent completion, or resolved thread is not human acceptance.

## Classify every item once

Material correctness, security, privacy, compliance, data integrity, accepted behavior, and explicit blocking feedback may not be downgraded because its wording is mild, its anchor is outdated, or the reviewer submitted `COMMENT` instead of `REQUEST_CHANGES`.

Choose exactly one disposition for each current item:

### `address_now`

Use when intent is clear and the change is within accepted scope, local and reversible, low risk, and objectively checkable without changing product or architecture semantics. The disposition says the PR should address the item now; it does not claim the current executor can write. If the required code, Git, or provider authority is absent, keep `address_now`, set the action status to blocked, and return the smallest patch or reply draft for an authorized owner. When authority is present, make the smallest complete repair, run proportionate checks, and bind the result to the new exact head. Route implementation to `eng-dev` and Git mutations to `eng-repo-governance` when those actions are chosen. A repair by the author or PIC does not provide required independent acceptance.

### `discuss`

Use for ambiguity, conflicting feedback, multiple materially different options, or a choice about scope, acceptance, product behavior, architecture, compatibility, migration, safety, privacy, compliance, performance trade-offs, release gates, risk acceptance, or who must provide a required independent review or approval. Return evidence, the narrow question, meaningful options, trade-offs, a recommendation when supported, and the decision owner. Keep the item unresolved until that decision exists. Route an actual canonical scope, acceptance, dependency, candidate, or gate decision to `eng-project-governance`, and delegation or independence assignment to `eng-agent-governance`; naming the need for either action does not itself mutate state.

### `defer`

Use when the feedback is valuable but outside current acceptance, non-blocking for the current PR, and safe to separate—for example an independent refactor or an improvement waiting on a real dependency. State why it does not make the current PR incorrect, the risk of waiting, the proposed owner, and an observable revisit trigger. Create or update a follow-up issue, milestone, or assignment only with separate authority. Do not present deferral as completed work or automatically resolve the thread.

### `no_action`

Use only with evidence that the item is already satisfied, a true duplicate of a canonical item, superseded, no longer semantically applicable to the current head, non-actionable automation noise, or a non-blocking preference such as an unsupported style nit. `outdated` describes an anchor, not the validity of the concern; confirm the concern no longer applies. For a human request that could reasonably appear unresolved, reply with the evidence or canonical link rather than silently ignoring it. Never say “fixed” when the decision is decline or no action.

If the evidence is insufficient for one class, use `discuss`; do not guess a more convenient disposition.

Semantically identical feedback may share one ledger row only when its disposition, evidence, action, status, owner, and recheck condition are the same. Preserve every source reference and revision in that row. Do not classify repeated wording as `no_action` while its canonical concern remains unresolved, and do not merge nearby comments whose provider state or required decision differs.

## Decide whether to modify, reply, or both

| Situation | Code or docs | Provider reply |
| --- | --- | --- |
| Mechanical, obvious, authorized `address_now` change | Modify and validate | Optional unless the reviewer asked a question or local convention requires acknowledgment |
| Non-obvious repair, different implementation, behavior or contract effect | Modify and validate | Explain intent, exact evidence, and any remaining decision |
| `discuss` | Do not choose unsettled semantics | Reply with the narrow decision request and evidence |
| `defer` | No speculative expansion | Reply with the reason, non-blocking basis, and authorized follow-up link if one exists |
| Human `no_action` item that still looks open | No change | Explain the evidence, duplicate, or reason for declining |
| Pure praise, FYI, or verified bot echo | No change | Usually neither; a reaction is enough when useful |

Prefer a code, test, or durable documentation improvement when future readers need the explanation. Do not leave behavior knowable only from a review thread. Batch coherent replies when the provider allows it so reviewers are not notified by a stream of “received” or “working on it” messages.

Suggest a diagram only when the comment exposes a material relationship, sequence, state, data, or boundary ambiguity and the smallest view under the [visual documentation contract](../../../docs/prd-td-visual-contract.md) would shorten the decision. A role, review type, or request for “more docs” does not require a diagram set, and triage does not become its design owner.

## Keep permissions and provider states separate

Authorization for one action does not imply another. Distinguish code editing, commit, push, PR reply, issue creation, thread resolution, review submission or dismissal, and merge. Never automatically approve, request changes, dismiss a review, resolve or reopen a thread, merge, close, or delete a comment.

Before any provider write, reconcile uncertain prior results and current remote state. Use provider delivery IDs when available and an action fingerprint such as `(repository, PR, head, comment revision, action kind, content hash)` to avoid duplicate replies. Do not treat a client mutation ID as proof that an uncertain operation succeeded.

GitHub is the first supported provider: distinguish conversation comments, review summaries, inline review comments, and review threads. Preserve `APPROVED`, `CHANGES_REQUESTED`, and `COMMENTED` as separate evidence. GitLab mapping is advisory only unless the environment exposes separately authorized capabilities; map discussions and notes without assuming GitHub permissions or semantics.

Do not reconstruct an exact code, architecture, or design artifact from a review summary that merely describes an unavailable proposal. Use the summary to identify a concern and request the exact accepted source or an explicit bounded decision; label any permitted derived illustration as proposed rather than authoritative.

## Return the summary, then the decision ledger

Start with the exact snapshot, conclusion, material items, and required action.
When current items exist, follow with one row per item:

| Field | Content |
| --- | --- |
| `FeedbackRef` | Provider URL or stable review, thread, and comment IDs |
| `Revision` | Exact PR head and latest comment or thread revision used |
| `Disposition` | `address_now`, `discuss`, `defer`, or `no_action` |
| `Rationale` | The controlling correctness, risk, scope, and value facts |
| `Evidence` | Code, test, contract, accepted scope, provider state, or canonical duplicate |
| `Action` | Smallest change, decision request, follow-up proposal, or no action |
| `Reply` | Sent reply URL or a clearly marked draft |
| `Status` | Completed, unresolved, blocked, or stale; never inferred from disposition alone |
| `Owner` | Current decision or action owner, if another action remains |
| `Recheck` | Observable revision, decision, dependency, or evidence that triggers reassessment |

After the ledger, summarize implemented changes and exact checks, unsent drafts and missing permissions, residual risk, and every unresolved discussion, deferral, blocker, or human decision. Place non-blocking preferences and P3/nits last. State the exact final head you actually re-read. A reply or local change is not completion when material feedback remains unresolved.

## Stop conditions

Stop the affected action and return the narrow blocker on a stale or changing head, edited or deleted feedback, dirty ownership conflict, missing scope or acceptance needed for classification, insufficient provider or Git authority, unresolved material semantics, required independence conflict, or an uncertain external write that cannot yet be reconciled. Continue independent read-only classification where safe. Stop normally when every current item has one evidenced disposition, authorized low-risk fixes and checks are complete, replies are sent or drafted according to permission, and unresolved items are explicit.
