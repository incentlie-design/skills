# Bug submission and test reports

Read when recording a defect, reporting test execution, or documenting a retest. These are evidence requirements, not a new workflow, task system, or mandatory file schema. Reuse the project's issue fields, report location, status vocabulary, and CI artifacts. A small check may use a concise Markdown record; reference shared facts instead of copying them into every bug and case.

## Identify what was actually tested

Both bugs and reports must supply or reference the relevant facts below. Mark unavailable facts as unknown and explain their effect on reproduction or the conclusion; do not invent them. Omit inapplicable environment details rather than dumping the entire machine configuration.

| Evidence | Required meaning |
| --- | --- |
| Subject and version | Repository/component, source branch or detached HEAD, and full tested commit SHA; release/tag and build, image digest, or deployment identity when applicable. For non-Git subjects use an immutable artifact identity. Branch names and mutable version labels alone are insufficient. |
| Actual execution target | Local worktree or CI/deployed target, and evidence tying that target to the tested version. A local checkout does not prove which build a remote endpoint serves. Distinguish source PR head, CI merge commit, and deployed build if they differ; capture each participating component's version for cross-component checks. |
| Local modifications | Clean/dirty state when testing local source. If dirty, retain the relevant patch or content identity, including untracked inputs. Label evidence as that modified snapshot, not as a clean-commit result. |
| Test baseline | Acceptance/requirement reference, case or suite revision, and test-code commit if different from the subject. Identify relevant config, feature flags, fixture/data version, and seed where they affect the result. |
| Environment | Local/CI/test/staging/production identity; mock/live boundaries; relevant OS, runtime, browser/device, dependency/service versions, and prerequisites. Record safe configuration references, never credentials or sensitive raw data. Recording production evidence does not authorize production actions. |
| Run and evidence | Execution time with timezone, executor or existing CI job/run link, command and selector or manual procedure, and locatable logs/results/screenshots/traces. Report authoring time is not execution time. |

For a shared or remote environment, note observed deployment/configuration changes during the run. Split evidence by target version or mark the mixed result inconclusive; never bind the entire run to an assumed single commit. A report's own file revision is separate from its tested-subject and test-suite revisions.

## Bug submission

Keep one independently actionable defect per record. Link related symptoms or duplicates when existing records are available; do not require a tracker lookup to document a new observation.

| Field | Minimum useful content |
| --- | --- |
| Locator and title | Existing issue ID/link, or a report section/path while drafting; component + trigger + observed failure, not merely “test failed.” |
| Impact and severity | Affected behavior/users/data and observed extent; severity with its basis. Use project levels; absent those, describe critical/high/medium/low impact. Scheduling priority is a separate triage decision, not inferred from severity. |
| Subject and environment | The version/environment block above, or a direct link to it; include the failing case and run/report reference. |
| Reproduction | Preconditions, minimal sanitized input/data, numbered steps or exact command, and observed frequency such as 2 of 3 attempts. Label single observations and intermittent failures honestly; do not invent repeat runs. |
| Expected versus actual | Expected behavior with its requirement/contract source; actual assertion, output, error, or state change. Attach the smallest relevant evidence with timestamps or trace IDs when useful. |
| Follow-up | Suggested repair area or missing proof, known workaround and limitations if any, known responsible owner or “unassigned,” and an observable retest condition. Separate suspected cause from established facts; root-cause certainty is not required to report a defect. |

- Missing credentials, unavailable infrastructure, and unexecuted checks are blockers or evidence gaps, not automatically product bugs. If intended behavior is unresolved, record the observation and decision needed instead of inventing an expected result.
- Drafting a bug does not file it externally. For an authorized tracker create/update, route the canonical write through `eng-project-governance`; reuse the selected system and its revision checks. If unavailable or unauthorized, deliver a locatable draft and explicitly say it was not submitted. Do not create a mirror, install an adapter, or require a tracker for local reporting.
- Before an authorized submission, check for a known duplicate when accessible and preserve the original evidence. After submission, report the actual returned issue link/ID; do not call a planned write successful.
- For a retest, reference the original bug, fixed candidate/build, actual tested version/environment, repeated reproduction steps, related regression scope, and new evidence. Preserve earlier failures. Record reproduced/not reproduced/blocked with the observed attempt count; a merged fix or one lucky rerun does not prove closure. QA supplies the retest conclusion; a tracker status change remains a separately authorized project action.

## Test report

The report must let a reader answer: what was tested, where, which cases were covered, what actually ran, what failed or remains unknown, and where the proof is.

1. **Report identity and objective:** stable path/link or existing report/run ID, author and report date/time, check type and bounded purpose, acceptance references, and the tested-version/environment block. Revisions or reruns must remain distinguishable without overwriting earlier failure evidence; no new numbering service is required.
2. **Scope and coverage:** included modules/behaviors and explicit exclusions. Map in-scope criteria and risks to case IDs/names or suite selectors. Identify relevant success, boundary, rejection, recovery, and regression checks only where the change warrants them; distinguish planned coverage from actual execution.
3. **Execution and results:** commands/selectors or manual steps; actual observations and per-case outcomes with evidence links. Group cases only when a linked detailed result preserves their individual outcomes. Include durations/timeouts when relevant and all attempts for retried or flaky cases.
4. **Summary and gaps:** reconcile counts for planned/selected, executed, passed, failed, blocked, skipped, and not run using the project's meanings. Give each selected case one final reported outcome, with partial/flaky attempts annotated separately. State exclusions and reasons separately, and keep retry attempts distinct from unique case counts. For percentages, name the numerator and denominator; test pass rate, requirement coverage, and measured code coverage are different claims. Never manufacture a coverage percentage from a test count.
5. **Bugs and residual risk:** link observed defects with severity and their affected criteria; separately list environment blockers, untested areas, unresolved decisions, and reused/stale evidence with its source and reuse rationale.
6. **Bounded conclusion and follow-up:** say which scope/version passed, failed, or could not be evaluated; identify the smallest required retest or missing proof and known next owner. State whether this is self-check or an independent evaluation when that distinction matters. A test report does not itself approve release, merge, or project closure.

Use the project's result vocabulary while preserving these distinctions: **passed** requires an observed satisfied assertion; **failed** is an observed assertion violation; **blocked** means a prerequisite prevented evaluation; **skipped** means a deliberate exclusion with a reason; **not run** means no execution evidence. If a runner uses different labels, explain the mapping. An aborted partial run must account for remaining selected cases rather than counting them as passed. Zero discovered tests, an exit code alone, or a passing subset cannot establish full-scope acceptance; mock evidence cannot establish live-system acceptance.

A compact case table is sufficient when no existing detailed report is available:

| Criterion/risk | Case/selector | Expected observation | Outcome and actual observation | Evidence or reason not evaluated |
| --- | --- | --- | --- | --- |

Do not rerun or broaden tests merely to fill a report field. State missing evidence and limit the conclusion; retain the supplied scope, authority, and proportional verification budget.
