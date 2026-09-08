"""Canonical task operations mapped to provider tools or SDK methods.

This module contains routing data only. It never installs plugins, creates
clients, authenticates accounts, or initializes provider state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


TASK_ADAPTER_CONTRACT_VERSION = 1
CANONICAL_OPERATIONS = (
    "resolve",
    "fetch",
    "changes",
    "create",
    "update",
    "transition",
    "comment",
)


@dataclass(frozen=True)
class OperationCall:
    tool: str
    fixed_arguments: tuple[tuple[str, Any], ...] = ()


@dataclass(frozen=True)
class AdapterMapping:
    dependency: str
    target_scheme: str
    operations: Mapping[str, tuple[OperationCall, ...]]


@dataclass(frozen=True)
class ToolCheck:
    ok: bool
    missing: tuple[str, ...]


ADAPTER_MAPPINGS: Mapping[str, AdapterMapping] = {
    "sqlite": AdapterMapping(
        dependency="sdk",
        target_scheme="task-space",
        operations={
            "resolve": (OperationCall("TaskSource.resolve"),),
            "fetch": (OperationCall("TaskSource.fetch"),),
            "changes": (OperationCall("TaskSource.changes"),),
            "create": (OperationCall("TaskSink.create"),),
            "update": (OperationCall("TaskSink.update"),),
            "transition": (OperationCall("TaskSink.transition"),),
            "comment": (OperationCall("TaskSink.comment"),),
        },
    ),
    "github-issues": AdapterMapping(
        dependency="plugin:github",
        target_scheme="github",
        operations={
            "resolve": (
                OperationCall("search_issues"),
                OperationCall("issue_read", (("method", "get"),)),
            ),
            "fetch": (OperationCall("issue_read", (("method", "get"),)),),
            "changes": (
                OperationCall("issue_read", (("method", "get"),)),
                OperationCall("issue_read", (("method", "get_comments"),)),
            ),
            "create": (OperationCall("issue_write", (("method", "create"),)),),
            "update": (OperationCall("issue_write", (("method", "update"),)),),
            "transition": (OperationCall("issue_write", (("method", "update"),)),),
            "comment": (OperationCall("add_issue_comment"),),
        },
    ),
    "gitlab-issues": AdapterMapping(
        dependency="plugin:gitlab",
        target_scheme="gitlab",
        operations={
            "resolve": (
                OperationCall("list_work_items", (("types", ("ISSUE",)),)),
                OperationCall("get_work_item"),
            ),
            "fetch": (OperationCall("get_work_item"),),
            "changes": (OperationCall("get_work_item", (("include", ("notes",)),)),),
            "create": (OperationCall("save_work_item", (("type_name", "Issue"),)),),
            "update": (OperationCall("save_work_item"),),
            "transition": (OperationCall("save_work_item"),),
            "comment": (OperationCall("save_note"),),
        },
    ),
}


def get_mapping(adapter_id: str) -> AdapterMapping:
    """Return the configured operation map or reject an unknown adapter."""

    try:
        return ADAPTER_MAPPINGS[adapter_id]
    except KeyError as exc:
        raise ValueError(f"unknown task adapter {adapter_id!r}") from exc


def get_operation_calls(adapter_id: str, operation: str) -> tuple[OperationCall, ...]:
    """Return the ordered provider calls for one canonical operation."""

    mapping = get_mapping(adapter_id)
    try:
        return mapping.operations[operation]
    except KeyError as exc:
        raise ValueError(
            f"task adapter {adapter_id!r} does not map operation {operation!r}"
        ) from exc


def check_tools(
    adapter_id: str,
    operations: Iterable[str],
    available_tools: Iterable[str],
) -> ToolCheck:
    """Check mapped tools without installing, authenticating, or creating them."""

    mapping = get_mapping(adapter_id)
    available = set(available_tools)
    namespace = mapping.dependency.partition(":")[2]
    missing = {
        call.tool
        for operation in operations
        for call in get_operation_calls(adapter_id, operation)
        if call.tool not in available
        and not any(
            name.endswith(f"__{namespace}__{call.tool}")
            for name in available
            if namespace
        )
    }
    return ToolCheck(not missing, tuple(sorted(missing)))
