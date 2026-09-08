# Research basis and derived decision principles

Use this reference to explain or challenge a material zero-to-one product or architecture recommendation. The sources support a direction; they do not make one architecture universally correct. Record local constraints and distinguish source findings from the design inference applied here.

## Synthesis

| Source idea | Derived rule for `ClosureDecision` | Limit |
| --- | --- | --- |
| Validated learning and Build–Measure–Learn | Define the observable learning loop before selecting architecture. Prefer the least product that can exercise it. | A weak metric can close the wrong loop; require a signal tied to the user or business outcome. |
| Small batches and frequent working delivery | Slice vertically so value and feedback cross the whole path early; avoid large horizontal foundation batches. | Batch size cannot remove mandatory safety, integration, or regulatory work. |
| Bounded rationality and satisficing | Use explicit acceptance thresholds and stop searching when one path meets them. Do not optimize an unknowable future system. | Satisficing is not permission to ignore a known severe risk. |
| Choice-response information cost | Keep the active option set small and default reversible choices. | Hick's experiments concern perceptual choice; applying them to team architecture decisions is an analogy, not direct causal evidence. |
| One-way and two-way doors | Deliberate on costly irreversible choices; move bounded reversible choices forward with enough evidence to learn. | Reversibility must include data, customers, contracts, and operations—not just source-code rollback. |
| YAGNI and evolutionary design | Reject presumptive features and abstractions, while keeping current code malleable and easy to change. | Neglecting maintainability makes deferral expensive and is not YAGNI. |
| Coarse architecture before stable boundaries | Prefer fewer deployable parts while the domain and product are uncertain; split after a measured need or stable boundary appears. | This is contextual advice, not a universal monolith rule; team structure or known constraints may justify early separation. |
| Accidental complexity avoidance | Minimize unnecessary state, code volume, control flow, sources of truth, and coordination paths. | Essential domain complexity remains and should be exposed clearly rather than hidden. |
| Rational documentation after iterative discovery | Allow design to emerge through evidence, then record the current rationale, rejected alternatives, and invalidation triggers cleanly. | Documentation must remain accurate; “we iterated” is not an excuse for an untraceable decision. |

## Primary and author sources

- Eric Ries, [The Lean Startup methodology](https://theleanstartup.com/principles): frames a startup as an experiment and uses Build–Measure–Learn plus an MVP to begin actionable learning quickly.
- DORA, [Working in small batches](https://dora.dev/capabilities/working-in-small-batches/): reports that small batches shorten feedback and course-correction time and are associated with software-delivery and organizational performance.
- [Principles behind the Agile Manifesto](https://agilemanifesto.org/principles): emphasizes early/frequent working software, technical excellence, reflection, and simplicity as maximizing work not done.
- Herbert A. Simon, [A Behavioral Model of Rational Choice](https://academic.oup.com/qje/article-abstract/69/1/99/1919737), 1955: replaces assumed global rationality with decision behavior compatible with limited information and computation.
- W. E. Hick, [On the Rate of Gain of Information](https://journals.sagepub.com/doi/10.1080/17470215208416600), 1952: relates choice-reaction time to information and uncertainty; this Skill uses it only as a bounded analogy for option load.
- AWS, [Elements of Amazon's Day 1 Culture](https://aws.amazon.com/executive-insights/content/how-amazon-defines-and-operationalizes-a-day-1-culture/): distinguishes irreversible one-way doors from reversible two-way doors and recommends faster action for the latter.
- Martin Fowler, [Yagni](https://martinfowler.com/bliki/Yagni.html): details build, delay, carry, and repair costs of presumptive features while stressing that YAGNI depends on a malleable, healthy codebase.
- Martin Fowler, [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html): argues that early distributed-system premiums can slow feedback while boundaries remain uncertain, and explicitly treats the recommendation as contextual rather than settled law.
- Ben Moseley and Peter Marks, [Out of the Tar Pit](https://worrydream.com/refs/Moseley_2006_-_Out_of_the_Tar_Pit.pdf), 2006: identifies complexity—especially state, code volume, and control flow—as a central obstacle to understanding software.
- David L. Parnas and Paul C. Clements, [A Rational Design Process: How and Why to Fake It](https://doi.org/10.1109/TSE.1986.6312940), 1986: explains why real design does not follow a perfectly rational top-down sequence and why maintained, rationalized documentation still matters.

## Decision review questions

Use only the questions that can change the recommendation:

1. What is the first complete actor-to-evidence loop?
2. Which single unknown is most likely to invalidate it?
3. Which decisions are truly irreversible outside the codebase?
4. What can safely use a default until an observable trigger occurs?
5. Which component, handoff, state, or abstraction can be removed now?
6. What keeps the thin path clean enough to replace or extend?
7. What result will cause the next product or architecture decision?
