#!/usr/bin/env python3
"""Validate the bounded project.yaml task-system binding without dependencies."""

import argparse
import json
import re
import sys
from pathlib import Path


FORBIDDEN_KEY_PARTS = (
    "account",
    "api_key",
    "connection",
    "credential",
    "email",
    "password",
    "secret",
    "token",
    "username",
)


def _matches_type(value, expected):
    return {
        "array": lambda: isinstance(value, list),
        "integer": lambda: isinstance(value, int) and not isinstance(value, bool),
        "object": lambda: isinstance(value, dict),
        "string": lambda: isinstance(value, str),
    }.get(expected, lambda: False)()


def _resolve_ref(root_schema, ref):
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported schema reference: {ref}")
    node = root_schema
    for part in ref[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def _validate_node(value, rule, root_schema, path, errors):
    if "$ref" in rule:
        rule = _resolve_ref(root_schema, rule["$ref"])
    if "type" in rule and not _matches_type(value, rule["type"]):
        errors.append(f"{path}: expected {rule['type']}")
        return
    if "const" in rule and value != rule["const"]:
        errors.append(f"{path}: expected {rule['const']!r}")
    if "enum" in rule and value not in rule["enum"]:
        errors.append(f"{path}: expected one of {rule['enum']!r}")
    if isinstance(value, str):
        if len(value) < rule.get("minLength", 0):
            errors.append(f"{path}: value is too short")
        if "pattern" in rule and re.fullmatch(rule["pattern"], value) is None:
            errors.append(f"{path}: value does not match {rule['pattern']}")
    if isinstance(value, int) and not isinstance(value, bool):
        if value < rule.get("minimum", value):
            errors.append(f"{path}: value is below {rule['minimum']}")
    if isinstance(value, dict):
        properties = rule.get("properties", {})
        for name in rule.get("required", []):
            if name not in value:
                errors.append(f"{path}: missing required property {name}")
        if rule.get("additionalProperties") is False:
            for name in value.keys() - properties.keys():
                errors.append(f"{path}: unexpected property {name}")
        for name, child in value.items():
            if name in properties:
                _validate_node(child, properties[name], root_schema, f"{path}.{name}", errors)
    if isinstance(value, list):
        if len(value) < rule.get("minItems", 0):
            errors.append(f"{path}: too few items")
        for index, child in enumerate(value):
            _validate_node(child, rule.get("items", {}), root_schema, f"{path}[{index}]", errors)


def _walk_keys(value, path="$"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield path, key
            yield from _walk_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_keys(child, f"{path}[{index}]")


def _semantic_errors(config, schema):
    errors = []
    if schema.get("x-owner") != "eng-project-governance":
        errors.append("schema: x-owner must be eng-project-governance")
    if schema.get("x-canonical-file") != "project.yaml":
        errors.append("schema: canonical filename must be project.yaml")
    if schema.get("x-syntax") != "json-compatible-yaml":
        errors.append("schema: syntax must be json-compatible-yaml")
    policy = schema.get("x-version-policy", {})
    if policy.get("current") != config.get("schema_version"):
        errors.append("$.schema_version: does not match the schema version policy")

    for path, key in _walk_keys(config):
        normalized = key.lower()
        if any(part in normalized for part in FORBIDDEN_KEY_PARTS):
            errors.append(f"{path}.{key}: credentials or personal connection fields are forbidden")

    task_system = config.get("task_system", {})
    selected = task_system.get("selected_adapter", {})
    expected_binding = f"{selected.get('adapter_id')}@{config.get('task_space_id')}"
    if selected.get("binding") != expected_binding:
        errors.append("$.task_system.selected_adapter.binding: must bind the selected adapter to task_space_id")
    sor = task_system.get("system_of_record", {})
    if sor.get("adapter_binding") != selected.get("binding"):
        errors.append("$.task_system.system_of_record: must name the one selected adapter binding")

    database = selected.get("config", {}).get("database")
    if isinstance(database, str):
        db_path = Path(database)
        if db_path.is_absolute() or ".." in db_path.parts:
            errors.append("$.task_system.selected_adapter.config.database: must be a project-relative path")
    return errors


def validate(root, config_path=None, schema_path=None):
    root = Path(root).resolve()
    config_path = Path(config_path) if config_path else root / "project.yaml"
    schema_path = Path(schema_path) if schema_path else root / "contracts/project.schema.json"
    errors = []
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        config = json.loads(config_path.read_text(encoding="utf-8"))
        _validate_node(config, schema, schema, "$", errors)
        errors.extend(_semantic_errors(config, schema))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid project artifact: {exc}")
    return {
        "status": "pass" if not errors else "fail",
        "config": str(config_path),
        "schema": str(schema_path),
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--config", type=Path)
    parser.add_argument("--schema", type=Path)
    args = parser.parse_args()
    report = validate(args.root, args.config, args.schema)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
