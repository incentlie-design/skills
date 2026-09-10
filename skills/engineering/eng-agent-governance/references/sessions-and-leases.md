# Delegation, Sessions, and result handoff

These are constraints on chosen coordination actions, not a scheduler or a required lifecycle.

## Responsibility and independence

An assignment is bounded work with an identifiable executor and expected output. The user request and existing conversation may supply this information; do not require a second assignment database. Reference a canonical WorkItem when one exists and is relevant, without mirroring its state.

PIC, PM, DEV, QA, Spec, and Reviewer are capability labels. Combining compatible capabilities does not need a new Session or an artificial approval hop. Required independent judgment must come from an executor independent of the subject being judged, not merely a differently named task.

When delegation creates nested coordination, make each aggregate scope's responsibility clear and avoid circular responsibility. This does not require a hierarchy for independent peer tasks or grant the coordinator additional authority.

## Creating or reusing a Session

- Use the runtime's supported creation, lookup, and reuse mechanisms within their authorization rules. Retain the returned identifier in the existing task context so subsequent operations address the same target.
- A pending creation is not a failed creation. Do not submit an equivalent creation again merely because setup is incomplete or a list omits the task. Use a supported lookup or wait; if resolution is unavailable, report that limitation instead of inventing an identifier or relying on private runtime storage.
- Keep a setup handle distinct from a usable Session identifier. Do not pass a handle to an operation that requires the resolved identifier unless that operation explicitly supports it.
- Splitting work does not require one branch per Session. Read-only collaborators need no write worktree; concurrent repository writers follow repository isolation constraints.

Titles are navigation labels. Use a requested naming convention when supplied; otherwise use a concise stable name. When a project provides a structured grammar, put the primary capability and bounded goal first, followed by only the locator fields the project defines. For example, a project may bind `ROLE · goal · milestone · #issue@rN`; its project rule owns the allowed roles, milestone vocabulary, tracker identity and parser. Validate with that project parser before create or deliberate rebind when available. Do not turn the example into a universal cross-project format.

A title records the context selected for that Session; it does not follow provider status. Keep an older-revision Session identifiable as such. Reuse it for a changed assignment only after impact review, then rename it before new work and preserve the handoff in existing context. Do not impose status icons, branch phases, synchronization timestamps, commits, running/done markers, or a title state machine. A title grants no authority and proves no independence; a missing or stale title does not block artifact handoff.

## Collecting and using results

Provide the expected output location or return destination when it matters to retrieval. Use existing artifacts, task results, or messages rather than a mandatory push-and-acknowledge protocol. Cross-task communication still follows the tool's authorization boundary.

A failed callback does not invalidate a completed artifact and does not justify rerunning the producer. The coordinator can retrieve and inspect the result through an authorized read mechanism. If neither delivery nor retrieval is available, report the missing input without claiming it was received.

Wait or read only as needed to satisfy the current request. A first-completion wait accounts for that result, not every outstanding dependency. An aggregate completion claim must cover its required outputs or explicitly name the gap. This does not require all child Sessions to end, a persistent child roster, or continuous polling. Do not claim background monitoring unless a supported mechanism is active.

## Shared ownership and stopping

For an actual exclusive shared resource, identify its owner and scope before conflicting writes. Use the existing resource's coordination mechanism where available; introduce lease records only when needed or required by project policy. If a lease is used, its expiry or review condition and release/transfer must be explicit. An expired record alone is not proof that the former writer stopped.

When blocked or stopped, preserve available output and report the affected work and any resources still held. Do not recursively create replacements to bypass an unchanged blocker. Evidence can survive a Session ending; Session status is not project acceptance.

Repository cleanup and Session archival are separate actions. Perform them only under an explicit request or an applicable configured user preference, with their respective checks. A bare merge-status statement such as “已合并” is not universal cleanup or archival authority; honor an existing explicit preference without asking for it again. Neither action is required to make a usable result complete.
