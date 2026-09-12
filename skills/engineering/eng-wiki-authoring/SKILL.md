---
name: eng-wiki-authoring
description: Author or restructure dual-track project wikis from exact canonical sources, using audience-aware information architecture, selective diagrams, validation, and derived-build provenance. Use for wiki/docs work; do not own product or architecture truth, require Archify, or perform Git/publication work.
---

# Wiki authoring

Own the bounded wiki/docs authoring artifact. Compile exact canonical sources into
readable derived pages without writing any slice of the
[shared governance contract](../../../docs/governance-contract.md), changing
product/architecture meaning, or taking over publication and Git decisions.

## Select the bounded documentation outcome

- Identify the audience, question/task, exact source tuple, existing site
  conventions, requested pages, target navigation, and observable review check.
- Separate user/operator and developer/contributor reading paths when their goals
  or vocabulary differ. A page has one primary audience; link to a counterpart
  instead of mixing both narratives.
- Use the lightest Diátaxis page type that matches intent: tutorial for guided
  learning, how-to for a bounded task, explanation/concept for why and mental
  model, reference for exact searchable contracts.
- Preserve the current IA for a scoped page edit. Create or restructure a broader
  skeleton only when the request actually needs navigation work; do not require a
  fixed dual-tree catalog or placeholder pages for every project.

## Compile sources without creating another owner

- Map each claim to an accepted exact source such as Issue/Requirement,
  Architecture/ADR, schema/API, code/CLI output, Git/PR/CI, or release evidence.
  Use a Source → Page map when several sources/pages make ownership ambiguous;
  otherwise direct links are enough.
- Keep `implemented`, `merged`, `accepted`, `released`, and `published` distinct.
  Missing evidence is `unknown`, not an inference from a title or status.
- Reference generated/API material from its executable source and generation
  path. Learn/concept pages may omit edge detail; Reference must match the
  selected exact contract.
- Do not copy mutable project state, role lifecycle, assignments, approval rules,
  or runtime/provider configuration into reusable page boilerplate.

## Shape pages for their reader

Use only sections that serve the page's task:

| Type | Useful shape |
| --- | --- |
| Tutorial | outcome → prerequisites → guided steps → observed result → cleanup/next |
| How-to | goal → prerequisites → minimal steps → verification → recovery/limits |
| Explanation/concept | question → mental model → boundaries/trade-offs → examples → next |
| Reference | exact subject/version → syntax/fields/contracts → examples → limits/links |

Navigation paths and front matter follow the site's existing conventions. When a
new convention is required, prefer stable paths, explicit audience/type, and a
source/as-of locator. Do not impose one framework, directory tree, weight scheme,
page count, or mandatory glossary on every wiki.

## Select diagrams by ambiguity

Apply the [visual documentation contract](../../../docs/prd-td-visual-contract.md).
A wiki diagram exists only to remove a material reader ambiguity in scope,
ownership, relationship, order, state, data/trust flow, runtime topology, or
failure/recovery.

- Reuse an accepted canonical diagram when it already answers the question. If a
  reader-specific simplification is needed, label it derived and preserve exact
  provenance; it must not silently change names, directions, cardinalities,
  states, or ownership.
- Choose the smallest view and one question per figure. Map it to the relevant
  body heading, goal, risk, AC, decision, or source fact and retain editable
  source. A short table or prose can be the better visual decision.
- Use `Diagram: N/A — <specific reason>` when the bounded page has no material
  visual ambiguity. Do not require a diagram inventory, a fixed family set,
  Figure numbering, global color files, or duplicated user/developer figures
  unless the target site's contract needs them.
- Validate changed visuals with available project tooling and inspect readability,
  clipping, labels, direction, contrast, and narrow layouts where relevant.

## Archify and publication boundary

Project authorship does not depend on Archify. An asynchronous derived-document
build MAY choose Archify as a presentation transform after exact canonical source
is frozen. The build must:

- mark the output derived and retain source commit/path provenance;
- keep canonical editable diagram/design source outside Archify;
- avoid writing generated interpretations back to canonical source;
- validate the derived render against the source and discard or block it on a
  semantic mismatch.

Archify availability is never a blocker for canonical docs or project diagrams.
Publisher, schedule, credentials, hosting target, and live state belong to the
owning runtime. Authoring a page candidate does not authorize publication.

## Review and handoff

Lead with the exact source tuple/target pages and candidate status, then material
source conflicts, broken reader paths, semantic/render failures, or required
owner/action. Put changed-page inventory, mapping detail, render/link evidence,
residual risk, and informational TODOs later using the
[review and handoff priority](../../../docs/review-handoff-template.md). A small
clean page change needs no full site ledger, empty checklist, or repeated project
history.

Review only applicable checks: factual provenance, audience/task fit, terminology,
links/navigation, runnable examples, reference fidelity, accessibility, rendering,
and source/target freshness. Stop when the bounded candidate is reviewable, or on
a source conflict, missing meaning owner, target drift, required validation gap,
publication-authority gap, or scope expansion. Report the affected action without
blocking unrelated authorized authoring.
