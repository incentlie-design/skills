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

The report must let a reader answer what exact subject was tested, the bounded
conclusion, what materially failed or remains unknown, the required action, what
was covered, and where the proof is. Present that decision path before execution
detail:

1. **Exact subject and bounded conclusion:** stable report/run locator, tested
   commit/artifact and environment identity, purpose, conclusion, and whether the
   work is self-check or independent. Revisions/reruns remain distinguishable.
2. **Material findings and required action:** observed defects, blockers, or
   evidence gaps with affected acceptance/risk, owner, smallest retest/repair or
   decision, and observable recheck. Omit the findings section when none exist.
3. **Scope and coverage:** included behaviors and explicit exclusions. Map only
   applicable criteria/risks to cases/selectors and distinguish planned coverage
   from actual execution.
4. **Execution and evidence:** commands/selectors or manual steps, actual
   observations, per-case outcomes, locatable evidence, and relevant attempts,
   durations, or timeouts.
5. **Counts and residual risk:** when aggregation is useful, reconcile unique
   selected, executed, passed, failed, blocked, skipped, and not-run cases. Keep
   attempts separate. Name percentage numerators/denominators; pass rate,
   requirement coverage, and code coverage are different claims. Put P3/nits,
   history, and appendices last.

A small clean check may use the short form from the review/handoff template plus
the command/evidence locator. It need not contain an empty finding table, every
possible count, a full environment dump, or a repeated ticket narrative. A test
report does not itself approve release, merge, or project closure.

Use the project's result vocabulary while preserving these distinctions: **passed** requires an observed satisfied assertion; **failed** is an observed assertion violation; **blocked** means a prerequisite prevented evaluation; **skipped** means a deliberate exclusion with a reason; **not run** means no execution evidence. If a runner uses different labels, explain the mapping. An aborted partial run must account for remaining selected cases rather than counting them as passed. Zero discovered tests, an exit code alone, or a passing subset cannot establish full-scope acceptance; mock evidence cannot establish live-system acceptance.

A compact case table is sufficient when no existing detailed report is available:

| Criterion/risk | Case/selector | Expected observation | Outcome and actual observation | Evidence or reason not evaluated |
| --- | --- | --- | --- | --- |

Do not rerun or broaden tests merely to fill a report field. State missing evidence and limit the conclusion; retain the supplied scope, authority, and proportional verification budget.
