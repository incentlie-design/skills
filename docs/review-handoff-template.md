# Review and handoff information template

Use this template for human-facing Review, QA evidence, PR-feedback, and PM/DEV/PIC
handoffs. It defines information priority, not a lifecycle or mandatory report
shape. Keep the project's existing vocabulary and omit sections that have no
content.

## Information priority

The first screen must answer, in this order:

1. **Exact subject** — the immutable revision, commit, PR head, artifact identity,
   or decision revision actually judged or handed off.
2. **Conclusion or status** — the bounded result for that subject, without
   implying approval, acceptance, merge, or release.
3. **Material findings** — only findings that can change correctness, acceptance,
   risk, or the next action. Omit this heading when none exist.
4. **Required decision or action** — the owner, smallest next action, and
   observable recheck condition. Say `none` only when that prevents ambiguity.

Coverage, detailed evidence, residual risk, low-priority suggestions, history,
and appendices follow the opening block. A blocker or required decision must not
be hidden in those sections.

Reference project facts once by their authoritative locator. Do not repeat the
ticket body, lifecycle, assignment, permissions, or release facts merely to make
the report look complete.

## Short clean result

When the exact subject has no material finding and no evidence gap that changes
the conclusion, this is sufficient:

```text
Subject: <exact identity>
Conclusion: no_material_finding — <bounded scope>
Action: none
```

Add one sentence for an important unreviewed boundary only when it can change how
the result is consumed. Do not add empty findings, coverage tables, a zero-row
ledger, repeated metadata, or an appendix.

## Material result

Use the smallest subset that communicates the decision:

```text
Subject: <exact identity>
Conclusion: <request_changes | unable_to_conclude | blocked | review_ready | other project vocabulary>

Material findings:
- <severity + evidence locator + impact>

Required decision/action:
- Owner: <actual owner or unknown>
- Action: <smallest repair, proof, or decision>
- Recheck: <observable condition>
```

Then add only applicable detail:

- coverage and exclusions;
- evidence, commands, observations, or feedback-item ledger;
- residual risk and unverified assumptions;
- P3 suggestions/nits, history, or appendix.

Keep each finding independently actionable. Separate an observed defect from an
evidence gap or open product decision. Low-priority advice cannot be promoted to
a blocker by template placement.

## Capability-specific use

| Capability | Opening conclusion | Material content and required action | Detail that follows |
| --- | --- | --- | --- |
| PIC | Candidate/decision status for the exact subject | Cross-output conflict, missing owner/input, next human decision | Candidate inventory and detailed evidence |
| PM | Requirement/plan readiness for the exact source revision | Scope/AC gap or product decision, with decision owner | Acceptance coverage, work packages, assumptions |
| DEV | Candidate readiness for the exact tree or artifact | Implementation blocker, failed check, compatibility or decision need | Changed paths, checks, rollback/replacement detail |
| QA/Reviewer | Bounded verdict for the exact tested/reviewed subject | Material finding or missing proof, with recheck | Coverage, observations, exclusions, residual risk, P3/nits |
| PR feedback triage | Disposition status for the exact PR head | Unresolved material item and owner/action | Item ledger, reply drafts, lower-priority items |
| Wiki authoring | Derived-page candidate status for the exact source tuple | Source conflict, broken contract, or publication decision | Changed pages, render/link detail, informational TODOs |

These are content responsibilities, not separate actors, approval hops, or
mandatory Sessions. The applicable Skill and project authority still own each
decision and side effect.
