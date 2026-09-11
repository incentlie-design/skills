# PR feedback principles and provider mapping

Use this reference to justify material triage decisions and provider writes. The sources define provider or review semantics; they do not decide local scope, acceptance, authority, or risk. Distinguish sourced behavior from the inference applied to the current PR.

## Derived operating rules

| Source idea | Derived rule | Limit |
| --- | --- | --- |
| GitHub review states distinguish comment, approval, and requested changes | Preserve the submitted state; never infer approval from a general comment or from a reply. | Branch protection and repository policy decide whether a state blocks merge. |
| A conversation can be resolved without dismissing a review, and a review can be dismissed separately | Reply, thread resolution, review state, and merge are different actions and permissions. | A resolved thread can still contain a valid concern; inspect content and current code. |
| Inline comments expose original/current commit and location fields | Bind the item to stable IDs, latest revision, anchor commit, and current head before acting. | Provider `outdated` is only an anchor fact, not evidence that the concern is semantically obsolete. |
| Good review comments explain why and distinguish required feedback from optional, nit, and FYI | Classify by correctness, risk, scope, and delivery value instead of tone alone; state the reason for discussion, deferral, or no action. | A reviewer label does not override accepted requirements or a material risk. |
| Authors should understand comments and may respectfully disagree with evidence | Ask a narrow question when intent is unclear; decline unsupported preferences without pretending they were fixed. | Disagreement is not permission to dismiss or resolve provider state. |
| Code should remain understandable without review history | Prefer a durable code, test, or documentation improvement when the explanation matters to future maintainers. | Do not add comments that merely narrate obvious code. |
| API clients should avoid unnecessary polling, serial request bursts, and blind retries | Batch coherent replies, use revisions and idempotency fingerprints, and reconcile uncertain writes before retrying. | A GraphQL `clientMutationId` supports correlation but is not an exactly-once guarantee. |

## Four-way decision test

Evaluate in this order so convenience cannot hide material feedback:

1. **Material validity:** Could this affect correctness, security, privacy, compliance, data integrity, accepted behavior, compatibility, or a required gate? If yes, it must be addressed or discussed; it is not noise.
2. **Current repair gate:** Is intent clear, scope accepted, risk low and local, and objective validation available? If all are true, use `address_now`; record missing execution authority as a blocked action rather than changing the feedback's disposition.
3. **Decision gate:** Is a human or project choice needed, or is evidence insufficient? Use `discuss`.
4. **Separability:** Is it useful, outside current acceptance, non-blocking, and safe to split with a real revisit trigger? Use `defer`.
5. **Evidence-backed no action:** Only then use `no_action` for satisfied, duplicate, superseded, semantically obsolete, noise, or non-blocking preference items.

Do not manufacture a follow-up issue to make deferral look tracked. If issue-write authority is absent, return a draft follow-up and keep the source item explicit.

One provider review can contain several decisions. When no item-level identity exists, derive local keys under the review revision and treat any review edit as changing all of them. Group repetitions only when all decision fields match, while retaining every source reference. Repetition is not resolution.

## GitHub evidence and capabilities

Read all relevant PR channels. A complete snapshot can require REST review comments plus review summaries and conversation comments, and GraphQL review-thread state. Capture the exact head after collection and recheck it before writes.

| Fact or action | Evidence or boundary |
| --- | --- |
| Review decision | Keep `APPROVE`, `REQUEST_CHANGES`, and `COMMENT` distinct. |
| Review thread | Track stable thread identity plus resolved and outdated state when exposed. |
| Inline comment | Capture `id`, `updated_at`, `commit_id`, `original_commit_id`, path, diff side or line, and hunk where available. |
| Reply | Requires comment capability; reply success does not resolve a thread or change review state. |
| Resolve or unresolve | Separate GraphQL mutation and separate authority; never implied by “handle comments.” |
| Dismiss review | Administrative action with its own permissions and audit meaning; never automate as triage cleanup. |
| Merge | Separate repository action and gate; no disposition or green check authorizes it. |

## GitLab compatibility boundary

Use provider-neutral internal fields such as `provider`, `change_request`, `head`, `feedback_id`, `feedback_revision`, `anchor`, `resolvable`, `resolved`, `outdated`, and `permission`. On GitLab, a discussion contains notes; note `updated_at`, `resolvable`, `resolved`, and `resolved_by` do not map one-for-one to GitHub review decisions. Treat provider permission and approval settings as independent inputs. The first version may read or describe this mapping, but it must not claim GitLab writes or use GitHub mutations against it.

## Primary sources

- GitHub, [Pull request reviews](https://docs.github.com/en/pull-requests/reference/pull-request-reviews): review decision meanings and branch-protection interaction.
- GitHub, [Resolving reviews](https://docs.github.com/en/pull-requests/concepts/resolving-reviews): author workflow for understanding, incorporating, validating, and tracking feedback.
- GitHub, [Dismissing a pull request review](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/dismissing-a-pull-request-review): dismissal permissions and audit behavior.
- GitHub, [REST API endpoints for pull request review comments](https://docs.github.com/en/rest/pulls/comments): review-comment identity, revisions, commits, and diff locations.
- GitHub, [GraphQL reference](https://docs.github.com/en/graphql/reference): thread state and distinct resolve, unresolve, review, and merge operations.
- GitHub, [Best practices for using the REST API](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api): conditional requests, serial mutation guidance, and retry behavior.
- Google Engineering Practices, [The standard of code review](https://google.github.io/eng-practices/review/reviewer/standard.html), [How to write code review comments](https://google.github.io/eng-practices/review/reviewer/comments.html), and [How to handle reviewer comments](https://google.github.io/eng-practices/review/developer/handling-comments.html): fact-based review, severity signals, rationale, durable code clarity, and respectful disagreement.
- GitLab, [Merge request reviews](https://docs.gitlab.com/user/project/merge_requests/reviews/), [Discussions API](https://docs.gitlab.com/api/discussions/), and [Merge request approval settings](https://docs.gitlab.com/user/project/merge_requests/approvals/settings/): discussions, notes, resolvability, and approval boundaries.
