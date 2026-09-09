---
name: eng-agent-governance
description: Constrain delegation, Session creation or reuse, assignment scope, independence, shared-resource ownership, explicit budgets, and result handoff. Use when those actions occur; do not prescribe workflow orchestration or manage the runtime's Session lifecycle.
---

# Agent governance

Own assignment responsibility and coordination constraints, not execution scheduling. The Agent chooses how to organize authorized work. A role is a capability, not a required separate Agent or Session. Use only the agent slice from [the shared governance contract](../../../docs/governance-contract.md) when structured coordination evidence is actually needed.

Read [delegation and result handoff](references/sessions-and-leases.md) when creating or reusing a Session, resolving shared ownership, or collecting delegated results.

## Delegating or splitting work

- Identify the bounded outcome, available inputs, expected output, executor, and read/write scope before dispatch. Resolve missing scope or authority when it could change the action; do not require a tracker item, adapter, formal role profile, Session record, or numeric budget merely to start useful work.
- Delegate only within the user's request and available tool permissions. Honor an explicit request for a new independent Session; do not substitute a rename or an internal subagent. Otherwise this Skill neither requires nor forbids splitting work.
- Preserve the current task and title when creating another task unless a change was requested. A parent relationship identifies coordination responsibility; it does not transfer permissions or approval rights.
- Enforce supplied independence requirements. The same Agent may perform compatible roles; self-check cannot satisfy required independent review. Missing independence blocks that conclusion, not unrelated implementation or analysis.

## Writing shared resources or consuming a budget

- Resolve competing writers before allowing overlapping writes. Repository branch/worktree isolation belongs to `eng-repo-governance`; do not duplicate it with mandatory file-lease bookkeeping.
- Use a lease only when an actual shared resource or project policy requires it. Record the resource, responsible owner, expiry or review condition, and release or transfer when that ownership ends. A stopped process does not prove the resource was released, and a lease grants no access permission.
- Honor explicit time, cost, token, or tool limits. Do not invent budgets or consumption numbers; absence of a numeric limit is not a startup blocker.

## Handing off or adopting results

- Make the output locatable and identify its scope, relevant revision, checks, remaining work, and material limitations. Reuse existing artifacts and messages; a separate record, callback, or receipt is not universally required.
- Base downstream work on the required artifact and evidence, not Session status or title. When a revision changes, assess its effect and suspend only actions whose input or evidence is no longer valid.
- When responsible for an aggregate result, account for the required inputs or explicitly report what is missing. One completed child does not prove that all required results are available; unrelated Sessions need not reach a terminal state.
- Report only observed progress. Do not equate execution completion, successful message delivery, acceptance, project closure, branch merge, or archival.

## Boundaries and stopping

Report the requested result and any affected blocker; do not manufacture a lifecycle transition or cleanup step to finish a response. Session naming and archival follow explicit user choices or a configured preference, not delivery gates. Project updates use `eng-project-governance`; Git mutations use `eng-repo-governance`. Neither loading this Skill nor ending a Session authorizes those actions.
