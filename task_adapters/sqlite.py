"""Transactional, project-scoped SQLite task adapter."""

from __future__ import annotations

import json
import re
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .contracts import (
    ABSENT_REVISION,
    ChangeSet,
    InvalidRequest,
    InvalidTransition,
    ResolveResult,
    RevisionConflict,
    TaskChange,
    TaskNotFound,
    TaskSnapshot,
    WriteRequest,
    WriteResult,
)


_IDENTITY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_BINDING = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._-]*@[A-Za-z0-9][A-Za-z0-9._-]*$"
)
_PREFIX = re.compile(r"^[A-Z][A-Z0-9]*$")
_RESERVED_FIELDS = {"work_item_ref", "system_of_record", "comments"}
_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class InitializationResult:
    created: bool
    project_id: str
    task_space_id: str
    adapter_binding: str
    next_number: int


class ConfigurationConflict(Exception):
    """The database is already bound to a different project task space."""


class SQLiteTaskAdapter:
    """One SQLite database bound to exactly one project task space."""

    def __init__(
        self,
        database: str | Path,
        *,
        project_id: str,
        task_space_id: str,
        adapter_binding: str,
        status_map: Mapping[str, str],
        number_prefix: str = "TASK",
        number_width: int = 6,
        number_start: int = 1,
        timeout: float = 5.0,
    ):
        for name, value in {
            "project_id": project_id,
            "task_space_id": task_space_id,
        }.items():
            if not isinstance(value, str) or not _IDENTITY.fullmatch(value):
                raise ValueError(f"invalid {name}: {value!r}")
        if not isinstance(adapter_binding, str) or not _BINDING.fullmatch(adapter_binding):
            raise ValueError(f"invalid adapter_binding: {adapter_binding!r}")
        if adapter_binding.partition("@")[0] != "local-sqlite":
            raise ValueError("adapter_binding must select the local-sqlite adapter")
        if adapter_binding.rpartition("@")[2] != task_space_id:
            raise ValueError("adapter_binding task space must match task_space_id")
        if not isinstance(number_prefix, str) or not _PREFIX.fullmatch(number_prefix):
            raise ValueError(f"invalid number_prefix: {number_prefix!r}")
        if number_width < 1:
            raise ValueError("number_width must be positive")
        if number_start < 1:
            raise ValueError("number_start must be positive")
        if not status_map or any(
            not isinstance(key, str)
            or not key
            or not isinstance(value, str)
            or not value
            for key, value in status_map.items()
        ):
            raise ValueError("status_map must contain non-empty canonical and adapter statuses")

        self.database = Path(database)
        self.project_id = project_id
        self.task_space_id = task_space_id
        self.adapter_binding = adapter_binding
        self.adapter_id = adapter_binding.partition("@")[0]
        self.status_map = dict(status_map)
        self.number_prefix = number_prefix
        self.number_width = number_width
        self.number_start = number_start
        self.timeout = timeout

    def initialize(self) -> InitializationResult:
        self.database.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            for statement in _SCHEMA:
                connection.execute(statement)

            existing = connection.execute(
                "SELECT schema_version, project_id, task_space_id, adapter_binding, status_map, "
                "number_prefix, number_width, number_start, next_number "
                "FROM task_space WHERE singleton = 1"
            ).fetchone()
            created = existing is None
            if created:
                connection.execute(
                    "INSERT INTO task_space "
                    "(singleton, schema_version, project_id, task_space_id, adapter_binding, "
                    "status_map, number_prefix, number_width, number_start, next_number) "
                    "VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        _SCHEMA_VERSION,
                        self.project_id,
                        self.task_space_id,
                        self.adapter_binding,
                        _json(self.status_map),
                        self.number_prefix,
                        self.number_width,
                        self.number_start,
                        self.number_start,
                    ),
                )
                next_number = self.number_start
            else:
                actual = tuple(existing[:8])
                expected = (
                    _SCHEMA_VERSION,
                    self.project_id,
                    self.task_space_id,
                    self.adapter_binding,
                    _json(self.status_map),
                    self.number_prefix,
                    self.number_width,
                    self.number_start,
                )
                if actual != expected:
                    connection.rollback()
                    raise ConfigurationConflict(
                        "database binding differs from the requested project task space"
                    )
                next_number = existing[8]
            connection.commit()

        return InitializationResult(
            created=created,
            project_id=self.project_id,
            task_space_id=self.task_space_id,
            adapter_binding=self.adapter_binding,
            next_number=next_number,
        )

    def resolve(self, external_id: str) -> ResolveResult:
        with closing(self._connect_initialized()) as connection:
            row = connection.execute(
                "SELECT work_item_ref, revision FROM tasks WHERE external_id = ?", (external_id,)
            ).fetchone()
            if row is None:
                raise TaskNotFound(external_id)
            return ResolveResult(row[0], _revision(row[1]))

    def fetch(self, work_item_ref: str) -> TaskSnapshot:
        with closing(self._connect_initialized()) as connection:
            return self._snapshot(connection, work_item_ref)

    def changes(self, work_item_ref: str, since_revision: str) -> ChangeSet:
        since = _revision_number(since_revision)
        with closing(self._connect_initialized()) as connection:
            task = self._task_row(connection, work_item_ref)
            if since > task[5]:
                raise InvalidRequest(
                    f"since_revision {since_revision!r} is newer than {_revision(task[5])!r}"
                )
            rows = connection.execute(
                "SELECT task_revision, operation, changed_fields, payload, "
                "authorization_evidence, occurred_at FROM task_changes "
                "WHERE task_number = ? AND task_revision > ? ORDER BY task_revision",
                (task[0], since),
            ).fetchall()
            return ChangeSet(
                work_item_ref=work_item_ref,
                changes=tuple(
                    TaskChange(
                        revision=_revision(row[0]),
                        operation=row[1],
                        changed_fields=tuple(json.loads(row[2])),
                        payload=json.loads(row[3]),
                        authorization_evidence=json.loads(row[4]),
                        occurred_at=row[5],
                    )
                    for row in rows
                ),
                current_revision=_revision(task[5]),
            )

    def create(self, request: WriteRequest) -> WriteResult:
        self._validate_request(request, "create")
        if request.expected_revision != ABSENT_REVISION:
            raise InvalidRequest(f"create expected_revision must be {ABSENT_REVISION!r}")

        payload = _copy_json_object(request.payload)
        if set(payload) != {"binding_key", "fields"}:
            raise InvalidRequest("create payload must contain exactly binding_key and fields")
        binding_key = payload["binding_key"]
        fields = payload["fields"]
        if not isinstance(binding_key, str) or not binding_key.strip():
            raise InvalidRequest("binding_key must be a non-empty string")
        if not isinstance(fields, dict):
            raise InvalidRequest("fields must be an object")
        self._validate_fields(fields, creating=True)

        with closing(self._connect_initialized()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            duplicate = connection.execute(
                "SELECT work_item_ref FROM tasks WHERE binding_key = ?", (binding_key,)
            ).fetchone()
            if duplicate is not None:
                snapshot = self._snapshot(connection, duplicate[0])
                connection.commit()
                return WriteResult("duplicate", False, snapshot.revision, snapshot)

            next_number = connection.execute(
                "SELECT next_number FROM task_space WHERE singleton = 1"
            ).fetchone()[0]
            external_id = f"{self.number_prefix}-{next_number:0{self.number_width}d}"
            work_item_ref = f"local:{self.task_space_id}:{external_id}"
            connection.execute(
                "UPDATE task_space SET next_number = ? WHERE singleton = 1", (next_number + 1,)
            )
            connection.execute(
                "INSERT INTO tasks "
                "(task_number, external_id, work_item_ref, binding_key, fields, revision) "
                "VALUES (?, ?, ?, ?, ?, 1)",
                (next_number, external_id, work_item_ref, binding_key, _json(fields)),
            )
            self._record_change(
                connection,
                next_number,
                1,
                request,
                tuple(sorted(fields)),
                payload,
            )
            snapshot = self._snapshot(connection, work_item_ref)
            connection.commit()

        return WriteResult("created", True, snapshot.revision, snapshot)

    def update(self, work_item_ref: str, request: WriteRequest) -> WriteResult:
        self._validate_request(request, "update")
        payload = _copy_json_object(request.payload)
        if set(payload) != {"fields"} or not isinstance(payload["fields"], dict):
            raise InvalidRequest("update payload must contain exactly one fields object")
        updates = payload["fields"]
        if not updates:
            raise InvalidRequest("update fields must not be empty")
        self._validate_fields(updates, creating=False)

        with self._write_transaction(work_item_ref, request) as (connection, task):
            fields = json.loads(task[4])
            fields.update(updates)
            revision = task[5] + 1
            connection.execute(
                "UPDATE tasks SET fields = ?, revision = ?, "
                "updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') "
                "WHERE task_number = ?",
                (_json(fields), revision, task[0]),
            )
            self._record_change(
                connection, task[0], revision, request, tuple(sorted(updates)), payload
            )
            snapshot = self._snapshot(connection, work_item_ref)

        return WriteResult("updated", True, snapshot.revision, snapshot)

    def transition(self, work_item_ref: str, request: WriteRequest) -> WriteResult:
        self._validate_request(request, "transition")
        payload = _copy_json_object(request.payload)
        if set(payload) != {"status"} or not isinstance(payload["status"], str):
            raise InvalidRequest("transition payload must contain exactly one string status")
        if payload["status"] not in self.status_map:
            raise InvalidTransition(payload["status"])

        with self._write_transaction(work_item_ref, request) as (connection, task):
            fields = json.loads(task[4])
            fields["status"] = payload["status"]
            revision = task[5] + 1
            connection.execute(
                "UPDATE tasks SET fields = ?, revision = ?, "
                "updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') "
                "WHERE task_number = ?",
                (_json(fields), revision, task[0]),
            )
            self._record_change(connection, task[0], revision, request, ("status",), payload)
            snapshot = self._snapshot(connection, work_item_ref)

        return WriteResult("transitioned", True, snapshot.revision, snapshot)

    def comment(self, work_item_ref: str, request: WriteRequest) -> WriteResult:
        self._validate_request(request, "comment")
        payload = _copy_json_object(request.payload)
        if set(payload) != {"body"} or not isinstance(payload["body"], str):
            raise InvalidRequest("comment payload must contain exactly one string body")
        if not payload["body"].strip():
            raise InvalidRequest("comment body must not be empty")

        with self._write_transaction(work_item_ref, request) as (connection, task):
            revision = task[5] + 1
            connection.execute(
                "INSERT INTO task_comments (task_number, task_revision, body) VALUES (?, ?, ?)",
                (task[0], revision, payload["body"]),
            )
            connection.execute(
                "UPDATE tasks SET revision = ?, "
                "updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') "
                "WHERE task_number = ?",
                (revision, task[0]),
            )
            self._record_change(connection, task[0], revision, request, ("comments",), payload)
            snapshot = self._snapshot(connection, work_item_ref)

        return WriteResult("commented", True, snapshot.revision, snapshot)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=self.timeout, isolation_level=None)
        connection.execute("PRAGMA foreign_keys = ON")
        connection.row_factory = sqlite3.Row
        return connection

    def _connect_initialized(self) -> sqlite3.Connection:
        if not self.database.is_file():
            raise InvalidRequest("adapter is not initialized")
        connection = self._connect()
        try:
            row = connection.execute(
                "SELECT schema_version, project_id, task_space_id, adapter_binding, status_map, "
                "number_prefix, number_width, number_start "
                "FROM task_space WHERE singleton = 1"
            ).fetchone()
        except sqlite3.OperationalError as error:
            connection.close()
            raise InvalidRequest("adapter is not initialized") from error
        expected = (
            _SCHEMA_VERSION,
            self.project_id,
            self.task_space_id,
            self.adapter_binding,
            _json(self.status_map),
            self.number_prefix,
            self.number_width,
            self.number_start,
        )
        if row is None or tuple(row) != expected:
            connection.close()
            raise ConfigurationConflict(
                "database binding differs from the requested project task space"
            )
        return connection

    def _validate_request(self, request: WriteRequest, operation: str) -> None:
        if request.adapter_binding != self.adapter_binding:
            raise InvalidRequest("request adapter_binding does not match this adapter")
        if request.operation != operation:
            raise InvalidRequest(f"request operation must be {operation!r}")
        if not request.authorization_evidence:
            raise InvalidRequest("authorization_evidence must not be empty")
        _copy_json_object(request.authorization_evidence)
        if not isinstance(request.expected_revision, str) or not request.expected_revision:
            raise InvalidRequest("expected_revision must be a non-empty string")
        if operation != "create":
            if request.expected_revision == ABSENT_REVISION:
                raise InvalidRequest("non-create writes require an rN expected_revision")
            _revision_number(request.expected_revision)

    def _validate_fields(self, fields: Mapping[str, Any], *, creating: bool) -> None:
        if any(not isinstance(field, str) or not field for field in fields):
            raise InvalidRequest("field names must be non-empty strings")
        if set(fields) & _RESERVED_FIELDS:
            raise InvalidRequest("fields contain adapter-owned values")
        if "status" in fields and not creating:
            raise InvalidRequest("status changes must use transition")
        if creating:
            if not isinstance(fields.get("status"), str):
                raise InvalidRequest("create fields must contain a string status")
            if fields["status"] not in self.status_map:
                raise InvalidTransition(fields["status"])
        _copy_json_object(fields)

    def _write_transaction(self, work_item_ref: str, request: WriteRequest):
        return _WriteTransaction(self, work_item_ref, request)

    def _task_row(self, connection: sqlite3.Connection, work_item_ref: str) -> sqlite3.Row:
        row = connection.execute(
            "SELECT task_number, external_id, work_item_ref, binding_key, fields, revision, "
            "created_at, updated_at FROM tasks WHERE work_item_ref = ?",
            (work_item_ref,),
        ).fetchone()
        if row is None:
            raise TaskNotFound(work_item_ref)
        return row

    def _snapshot(self, connection: sqlite3.Connection, work_item_ref: str) -> TaskSnapshot:
        task = self._task_row(connection, work_item_ref)
        comments = connection.execute(
            "SELECT body, task_revision, created_at FROM task_comments "
            "WHERE task_number = ? ORDER BY comment_id",
            (task[0],),
        ).fetchall()
        revision = _revision(task[5])
        fields = json.loads(task[4])
        fields.update(
            {
                "work_item_ref": task[2],
                "system_of_record": {
                    "adapter_id": self.adapter_id,
                    "external_id": task[1],
                    "revision": revision,
                },
                "comments": tuple(
                    {
                        "body": comment[0],
                        "revision": _revision(comment[1]),
                        "created_at": comment[2],
                    }
                    for comment in comments
                ),
            }
        )
        return TaskSnapshot(
            work_item_ref=task[2],
            canonical_fields=fields,
            revision=revision,
            source_evidence={
                "adapter_binding": self.adapter_binding,
                "project_id": self.project_id,
                "task_space_id": self.task_space_id,
                "external_id": task[1],
                "binding_key": task[3],
            },
        )

    @staticmethod
    def _record_change(
        connection: sqlite3.Connection,
        task_number: int,
        revision: int,
        request: WriteRequest,
        changed_fields: tuple[str, ...],
        payload: Mapping[str, Any],
    ) -> None:
        connection.execute(
            "INSERT INTO task_changes "
            "(task_number, task_revision, operation, changed_fields, payload, "
            "authorization_evidence) VALUES (?, ?, ?, ?, ?, ?)",
            (
                task_number,
                revision,
                request.operation,
                _json(changed_fields),
                _json(payload),
                _json(request.authorization_evidence),
            ),
        )


class _WriteTransaction:
    def __init__(
        self, adapter: SQLiteTaskAdapter, work_item_ref: str, request: WriteRequest
    ):
        self.adapter = adapter
        self.work_item_ref = work_item_ref
        self.request = request
        self.connection: sqlite3.Connection | None = None

    def __enter__(self) -> tuple[sqlite3.Connection, sqlite3.Row]:
        self.connection = self.adapter._connect_initialized()
        try:
            self.connection.execute("BEGIN IMMEDIATE")
            task = self.adapter._task_row(self.connection, self.work_item_ref)
            current_revision = _revision(task[5])
            if self.request.expected_revision == current_revision:
                return self.connection, task
            current = self.adapter._snapshot(self.connection, self.work_item_ref)
        except Exception:
            self.connection.rollback()
            self.connection.close()
            self.connection = None
            raise
        self.connection.rollback()
        self.connection.close()
        self.connection = None
        raise RevisionConflict(self.request.expected_revision, current)

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        assert self.connection is not None
        try:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
        finally:
            self.connection.close()
        return False


def _revision(number: int) -> str:
    return f"r{number}"


def _revision_number(revision: str) -> int:
    if revision == ABSENT_REVISION:
        return 0
    if not isinstance(revision, str) or not re.fullmatch(r"r[1-9][0-9]*", revision):
        raise InvalidRequest(f"invalid revision: {revision!r}")
    return int(revision[1:])


def _json(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as error:
        raise InvalidRequest("payload must contain JSON-compatible values") from error


def _copy_json_object(value: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise InvalidRequest("value must be an object")
    copied = json.loads(_json(value))
    if not isinstance(copied, dict):
        raise InvalidRequest("value must be an object")
    return copied


_SCHEMA = (
    """
    CREATE TABLE IF NOT EXISTS task_space (
        singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
        schema_version INTEGER NOT NULL CHECK (schema_version > 0),
        project_id TEXT NOT NULL,
        task_space_id TEXT NOT NULL,
        adapter_binding TEXT NOT NULL,
        status_map TEXT NOT NULL,
        number_prefix TEXT NOT NULL,
        number_width INTEGER NOT NULL CHECK (number_width > 0),
        number_start INTEGER NOT NULL CHECK (number_start > 0),
        next_number INTEGER NOT NULL CHECK (next_number > 0)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS tasks (
        task_number INTEGER PRIMARY KEY,
        external_id TEXT NOT NULL UNIQUE,
        work_item_ref TEXT NOT NULL UNIQUE,
        binding_key TEXT NOT NULL UNIQUE,
        fields TEXT NOT NULL,
        revision INTEGER NOT NULL CHECK (revision > 0),
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
        updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS task_comments (
        comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_number INTEGER NOT NULL REFERENCES tasks(task_number),
        task_revision INTEGER NOT NULL,
        body TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
        UNIQUE (task_number, task_revision)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS task_changes (
        task_number INTEGER NOT NULL REFERENCES tasks(task_number),
        task_revision INTEGER NOT NULL,
        operation TEXT NOT NULL,
        changed_fields TEXT NOT NULL,
        payload TEXT NOT NULL,
        authorization_evidence TEXT NOT NULL,
        occurred_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
        PRIMARY KEY (task_number, task_revision)
    )
    """,
)
