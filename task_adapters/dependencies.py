"""Read-only validation for environment-injected task-adapter dependencies."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .contracts import TaskSink, TaskSource


TASK_ADAPTER_CONTRACT_VERSION = 1
SOURCE_CAPABILITIES = frozenset({"resolve", "fetch", "changes"})
SINK_CAPABILITIES = frozenset({"create", "update", "transition", "comment"})


@dataclass(frozen=True)
class AdapterDependency:
    """An already-resolved adapter supplied by the execution environment."""

    adapter_id: str
    binding: str
    profile_ref: str
    contract_version: int
    capabilities: frozenset[str]
    available: bool = True
    source: TaskSource | None = None
    sink: TaskSink | None = None
    detail: str = ""


@dataclass(frozen=True)
class DependencyCheck:
    ok: bool
    errors: tuple[str, ...]


class DependencyUnavailable(RuntimeError):
    """The selected project adapter is not compatible with the environment."""

    def __init__(self, check: DependencyCheck):
        self.check = check
        super().__init__("; ".join(check.errors))


def check_dependency(
    project_config: Mapping[str, Any],
    dependency: AdapterDependency | None,
) -> DependencyCheck:
    """Compare project selection with one environment-supplied dependency.

    This function is intentionally read-only. It never resolves profiles,
    authenticates clients, provisions stores, or starts mirrors.
    """

    errors: list[str] = []
    task_system = project_config.get("task_system")
    selected = task_system.get("selected_adapter") if isinstance(task_system, Mapping) else None
    if not isinstance(selected, Mapping):
        return DependencyCheck(False, ("project config has no selected task adapter",))

    required_value = selected.get("required_capabilities")
    if not isinstance(required_value, list) or not all(
        isinstance(capability, str) for capability in required_value
    ):
        errors.append("project adapter capabilities are invalid")
        required = frozenset()
    else:
        required = frozenset(required_value)

    selected_version = selected.get("contract_version")
    if selected_version != TASK_ADAPTER_CONTRACT_VERSION:
        errors.append(
            f"unsupported task-adapter contract version {selected_version!r}; "
            f"SDK supports {TASK_ADAPTER_CONTRACT_VERSION}"
        )

    if dependency is None:
        profile_ref = selected.get("profile_ref")
        errors.append(f"runtime dependency {profile_ref!r} was not injected")
        return DependencyCheck(False, tuple(errors))

    expected = {
        "adapter_id": selected.get("adapter_id"),
        "binding": selected.get("binding"),
        "profile_ref": selected.get("profile_ref"),
        "contract_version": selected_version,
    }
    actual = {
        "adapter_id": dependency.adapter_id,
        "binding": dependency.binding,
        "profile_ref": dependency.profile_ref,
        "contract_version": dependency.contract_version,
    }
    for field, expected_value in expected.items():
        if actual[field] != expected_value:
            errors.append(
                f"runtime {field} {actual[field]!r} does not match project {expected_value!r}"
            )

    if not dependency.available:
        suffix = f": {dependency.detail}" if dependency.detail else ""
        errors.append(f"runtime dependency is unavailable{suffix}")

    missing = required - dependency.capabilities
    if missing:
        errors.append(f"runtime dependency is missing capabilities {sorted(missing)}")

    if dependency.available and required & SOURCE_CAPABILITIES:
        if dependency.source is None or not isinstance(dependency.source, TaskSource):
            errors.append("runtime dependency does not provide a TaskSource")
    if dependency.available and required & SINK_CAPABILITIES:
        if dependency.sink is None or not isinstance(dependency.sink, TaskSink):
            errors.append("runtime dependency does not provide a TaskSink")

    return DependencyCheck(not errors, tuple(errors))


def require_dependency(
    project_config: Mapping[str, Any],
    dependency: AdapterDependency | None,
) -> AdapterDependency:
    """Return a compatible injected dependency or raise a blocking diagnostic."""

    check = check_dependency(project_config, dependency)
    if not check.ok:
        raise DependencyUnavailable(check)
    assert dependency is not None
    return dependency
