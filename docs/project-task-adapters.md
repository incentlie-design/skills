# Project task-adapter mappings and SDK

[project.yaml](../project.yaml) selects one task adapter and target for the project. The selected mapping translates the canonical task operations to the GitHub or GitLab tools already exposed in the current Session, or to the SQLite SDK interface. The project file does **not** install a plugin, authenticate an account, create a client, initialize storage, or start a mirror.

The canonical file uses JSON-compatible YAML so the standard-library validator can parse it deterministically:

~~~sh
python3 scripts/validate_project.py
~~~

The validator applies [project.schema.json](../contracts/project.schema.json), rejects unknown and sensitive fields, and verifies the unique system-of-record binding.

## Core and environment boundary

| skill-creator core | Execution environment/runtime |
| --- | --- |
| project.yaml schema, adapter selection, and target | Install and authenticate plugins |
| Provider-neutral TaskSource / TaskSink types | Database paths, credentials, accounts, and connections |
| Canonical-operation to provider-tool mappings | Expose provider tools to the Session |
| Revision/conflict and WorkItem invariants | Provision schemas, initialize providers, and run mirrors |
| Mapping contract tests | Provider integration and lifecycle tests |

The [mapping registry](../task_adapters/mappings.py) contains no provider client. It only resolves a canonical operation to ordered tool calls:

~~~python
from task_adapters import check_tools, get_operation_calls

calls = get_operation_calls("github-issues", "create")
# (OperationCall(tool="issue_write", fixed_arguments=(("method", "create"),)),)
check = check_tools("github-issues", ("create",), session_tool_names)
~~~

Before using a route, the Skill checks whether the current Session exposes the mapped tool in the selected plugin namespace. A missing tool is a dependency error. The Skill reports it and stops instead of repairing the environment or choosing another provider.

## Project selection

The checked-in project selects SQLite without including its path or initialization settings:

~~~json
{
  "adapter_id": "sqlite",
  "binding": "sqlite@skill-creator-local",
  "target_ref": "task-space:skill-creator-local",
  "contract_version": 1
}
~~~

The same schema selects GitHub Issues by changing the adapter binding and target:

~~~json
{
  "adapter_id": "github-issues",
  "binding": "github-issues@skill-creator-github",
  "target_ref": "github:incentlie-design/skills",
  "contract_version": 1
}
~~~

GitLab Issues uses `adapter_id: gitlab-issues` and a `gitlab:group/project` target. `target_ref` identifies the project-owned task space; it is not an account, token, connection profile, or client configuration.

At Session start:

1. Validate project.yaml.
2. Resolve the selected adapter in the mapping registry.
3. Check that the mapped tools needed by the requested operation are available in the current Session.
4. Invoke those tools with the selected target and canonical payload.

For example, canonical `create` maps to `issue_write(method=create)` for GitHub and `save_work_item(type_name=Issue)` for GitLab. SQLite maps the same operation to `TaskSink.create`. Editing project.yaml changes which mapping is used; the selected plugin must already be installed, authenticated, and available to that Session.

## Contract invariants

A TaskSource exposes resolve, fetch, and changes. A TaskSink may expose create, update, transition, and comment. Every sink call receives an immutable WriteRequest with the adapter binding, operation, payload, authorization evidence, and expected_revision.

Provider external ids and revisions are opaque. The selected adapter issues its own external id and binds it to one stable work_item_ref. A revision conflict returns fresh read evidence; the caller re-reads, assesses impact, and stops until a new decision instead of retrying as a blind overwrite.

One WorkItem has exactly one system_of_record. Project governance may decide that Jira, GitHub Issues, or another source is a mirror and define direction and migration semantics. The runtime owns starting and operating that mirror. A running mirror never becomes a second write authority merely because it is available.

Status mapping translates the five project states without creating another project or Agent state machine. Agent lifecycle remains owned by eng-agent-governance through the [governance contract](governance-contract.md).

## Version 1 to version 2

Schema version 2 is intentionally breaking. It removes SQLite-specific kind, config.database, atomic-numbering settings, fixed local WorkItem reference formatting, and configurable revision syntax. Replace them with adapter identity, target_ref, and contract_version; move plugin connections and provider construction to the execution environment.

Consumers reject unsupported schema or adapter-contract versions rather than guessing. Increment config_revision whenever a project changes its binding or status mapping. Changing adapter_id, binding, or task_space_id is an explicit system-of-record migration, not a cosmetic edit. No version-1 compatibility shim or provider bootstrap remains in core.
