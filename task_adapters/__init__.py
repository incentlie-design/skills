"""Provider-neutral task adapter contracts and local implementations."""

from .contracts import (
    ABSENT_REVISION,
    ChangeSet,
    InvalidRequest,
    InvalidTransition,
    ResolveResult,
    RevisionConflict,
    TaskChange,
    TaskNotFound,
    TaskSink,
    TaskSnapshot,
    TaskSource,
    WriteRequest,
    WriteResult,
)
from .sqlite import ConfigurationConflict, InitializationResult, SQLiteTaskAdapter

__all__ = [
    "ABSENT_REVISION",
    "ChangeSet",
    "ConfigurationConflict",
    "InitializationResult",
    "InvalidRequest",
    "InvalidTransition",
    "ResolveResult",
    "RevisionConflict",
    "SQLiteTaskAdapter",
    "TaskChange",
    "TaskNotFound",
    "TaskSink",
    "TaskSnapshot",
    "TaskSource",
    "WriteRequest",
    "WriteResult",
]
