# Project task-adapter mappings

[`project.yaml`](../project.yaml) selects a task adapter and target. It does not install a plugin, authenticate an account, create a client, initialize storage, or start a mirror.

The file is JSON-compatible YAML so it can be validated without a YAML dependency:

~~~sh
python3 scripts/validate_project.py
~~~

## Selection

The checked-in project selects an environment-provided SQLite implementation without specifying its database path:

~~~json
{
  "adapter_id": "sqlite",
  "binding": "sqlite@skill-creator-local",
  "target_ref": "task-space:skill-creator-local",
  "contract_version": 1
}
~~~

GitHub Issues instead uses `adapter_id: github-issues` and a `github:owner/repository` target. GitLab Issues uses `adapter_id: gitlab-issues` and a `gitlab:group/project` target. Targets identify project task spaces, not accounts, tokens, or connection profiles.

## Execution

The provider-neutral [`TaskSource` and `TaskSink`](../task_adapters/contracts.py) define the canonical operations. [`task_adapters.mappings`](../task_adapters/mappings.py) maps those operations to SQLite SDK methods or provider tools. The Project Skill keeps the human-readable table in [work items and adapters](../skills/engineering/eng-project-governance/references/work-items-and-adapters.md).

For each operation:

1. Validate `project.yaml` and resolve its adapter mapping.
2. Check that the mapped SDK methods or plugin tools are available in the current Session.
3. Invoke them with `target_ref` and the canonical payload.
4. A missing mapped tool is a transport diagnostic. Use an already authorized same-provider transport only as described in the Project Skill reference; otherwise stop the dependent operation. Never silently change the system of record or bootstrap a client.

`check_tools` checks the listed SDK/plugin mapping only. It neither discovers alternate transports nor proves their concurrency guarantees. A browser/CLI write must state its actual revision checks and limits; a read followed by save is not atomic compare-and-set. Cross-project work may explicitly retain its initiating canonical ticket without changing this repository’s default task-space configuration.

Plugin installation, authentication, and permissions belong to the Codex environment. SQLite storage and initialization belong to its external implementation. Project governance owns the system of record and any mirror or migration decision.

## Contract and migration

Provider external ids and revisions are opaque. Writes carry the selected binding, authorization evidence, and expected revision. A conflict causes a fresh read and a new decision rather than a blind retry.

Schema version 2 removes the version-1 SQLite path, numbering, binding-format, and revision-format settings. Consumers reject unsupported schema or adapter-contract versions. Changing the adapter, binding, target, or task-space identity is an explicit system-of-record migration.
