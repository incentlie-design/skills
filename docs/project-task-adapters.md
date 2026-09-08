# Project task-adapter binding and SDK

[project.yaml](../project.yaml) selects one task adapter for the project. It does **not** create a database, authenticate a GitHub or Jira client, start a mirror, or make the adapter available to a new Session. Those are execution-environment responsibilities.

The canonical file uses JSON-compatible YAML so the standard-library validator can parse it deterministically:

~~~sh
python3 scripts/validate_project.py
~~~

The validator applies [project.schema.json](../contracts/project.schema.json), rejects unknown and sensitive fields, verifies the unique system-of-record binding, and checks the capabilities required by project governance.

## Core and environment boundary

| skill-creator core | Execution environment/runtime |
| --- | --- |
| project.yaml schema and adapter selection | Resolve profile_ref |
| Provider-neutral TaskSource / TaskSink types | Database paths, credentials, accounts, and connections |
| Read-only dependency checker | Construct SQLite, GitHub Issues, Jira, or other clients/stores |
| Revision/conflict and WorkItem invariants | Provision schemas, initialize providers, and run mirrors |
| Contract tests | Provider integration and lifecycle tests |

The environment injects an already-resolved [AdapterDependency](../task_adapters/dependencies.py). The SDK compares its adapter id, binding, profile reference, contract version, capabilities, and structural TaskSource/TaskSink interfaces with project.yaml. The checker performs no lookup or write:

~~~python
from task_adapters import require_dependency

dependency = require_dependency(project_config, environment_dependency)
~~~

If the dependency is absent or incompatible, startup stops with the checker diagnostics. A Skill must not repair that condition by bootstrapping a provider.

## Project selection

The checked-in project selects SQLite without including its path or initialization settings:

~~~json
{
  "adapter_id": "sqlite",
  "binding": "sqlite@skill-creator-local",
  "profile_ref": "runtime:skill-creator/sqlite",
  "contract_version": 1,
  "required_capabilities": ["resolve", "fetch", "changes", "create", "update", "transition", "comment"]
}
~~~

The same schema selects GitHub Issues by changing the adapter binding and runtime profile:

~~~json
{
  "adapter_id": "github-issues",
  "binding": "github-issues@skill-creator-github",
  "profile_ref": "runtime:skill-creator/github-issues",
  "contract_version": 1,
  "required_capabilities": ["resolve", "fetch", "changes", "create", "update", "transition", "comment"]
}
~~~

For that second selection, the environment owns repository/account selection, authentication, GitHub client creation, and any provider-specific setup. profile_ref is an opaque reference to that environment configuration, never a credential container.

At Session start:

1. Validate project.yaml.
2. Ask the environment for the selected profile_ref.
3. Run require_dependency against the injected dependency.
4. Use only the returned provider-neutral source/sink interfaces.

Editing project.yaml therefore changes the requested binding, but it takes effect only when the Session environment supplies a matching dependency.

## Contract invariants

A TaskSource exposes resolve, fetch, and changes. A TaskSink may expose create, update, transition, and comment. Every sink call receives an immutable WriteRequest with the adapter binding, operation, payload, authorization evidence, and expected_revision.

Provider external ids and revisions are opaque. The selected adapter issues its own external id and binds it to one stable work_item_ref. A revision conflict returns fresh read evidence; the caller re-reads, assesses impact, and stops until a new decision instead of retrying as a blind overwrite.

One WorkItem has exactly one system_of_record. Project governance may decide that Jira, GitHub Issues, or another source is a mirror and define direction and migration semantics. The runtime owns starting and operating that mirror. A running mirror never becomes a second write authority merely because it is available.

Status mapping translates the five project states without creating another project or Agent state machine. Agent lifecycle remains owned by eng-agent-governance through the [governance contract](governance-contract.md).

## Version 1 to version 2

Schema version 2 is intentionally breaking. It removes SQLite-specific kind, config.database, atomic-numbering settings, fixed local WorkItem reference formatting, and configurable revision syntax. Replace them with profile_ref, contract_version, and required_capabilities; move all provider construction and initialization settings to the execution environment.

Consumers reject unsupported schema or adapter-contract versions rather than guessing. Increment config_revision whenever a project changes its binding or status mapping. Changing adapter_id, binding, or task_space_id is an explicit system-of-record migration, not a cosmetic edit. No version-1 compatibility shim or provider bootstrap remains in core.
