"""Provider-neutral TaskSource and TaskSink contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol, runtime_checkable


ABSENT_REVISION = "absent"


@dataclass(frozen=True)
class ResolveResult:
    work_item_ref: str
    revision: str


@dataclass(frozen=True)
class TaskSnapshot:
    work_item_ref: str
    canonical_fields: Mapping[str, Any]
    revision: str
    source_evidence: Mapping[str, str]


@dataclass(frozen=True)
class TaskChange:
    revision: str
    operation: str
    changed_fields: tuple[str, ...]
    payload: Mapping[str, Any]
    authorization_evidence: Mapping[str, str]
    occurred_at: str


@dataclass(frozen=True)
class ChangeSet:
    work_item_ref: str
    changes: tuple[TaskChange, ...]
    current_revision: str


@dataclass(frozen=True)
class WriteRequest:
    adapter_binding: str
    operation: str
    payload: Mapping[str, Any]
    authorization_evidence: Mapping[str, str]
    expected_revision: str


@dataclass(frozen=True)
class WriteResult:
    outcome: str
    applied: bool
    revision: str
    snapshot: TaskSnapshot


class TaskAdapterError(Exception):
    """Base error for provider-neutral task adapters."""


class InvalidRequest(TaskAdapterError):
    """The request does not satisfy the adapter contract."""


class InvalidTransition(TaskAdapterError):
    """The requested status is not configured for this project."""


class TaskNotFound(TaskAdapterError):
    """The requested task does not exist in the bound task space."""


class RevisionConflict(TaskAdapterError):
    """A compare-and-swap write failed and includes fresh read evidence."""

    def __init__(self, expected_revision: str, current: TaskSnapshot):
        self.expected_revision = expected_revision
        self.current = current
        super().__init__(
            f"expected revision {expected_revision!r}, current revision is {current.revision!r}"
        )


@runtime_checkable
class TaskSource(Protocol):
    def resolve(self, external_id: str) -> ResolveResult: ...

    def fetch(self, work_item_ref: str) -> TaskSnapshot: ...

    def changes(self, work_item_ref: str, since_revision: str) -> ChangeSet: ...


@runtime_checkable
class TaskSink(Protocol):
    def create(self, request: WriteRequest) -> WriteResult: ...

    def update(self, work_item_ref: str, request: WriteRequest) -> WriteResult: ...

    def transition(self, work_item_ref: str, request: WriteRequest) -> WriteResult: ...

    def comment(self, work_item_ref: str, request: WriteRequest) -> WriteResult: ...
