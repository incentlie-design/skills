#!/usr/bin/env python3
"""Validate the public eight-Skill repository contract using the standard library."""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


EXPECTED_NAMES = (
    "eng-repo-governance",
    "eng-workspace-governance",
    "eng-project-governance",
    "eng-agent-governance",
    "eng-closed-loop-decisions",
    "eng-pm",
    "eng-dev",
    "eng-qa-reviewer",
)
EXPECTED_DEPENDENCIES = {
    "eng-repo-governance": [],
    "eng-workspace-governance": ["eng-repo-governance"],
    "eng-project-governance": ["eng-workspace-governance"],
    "eng-agent-governance": ["eng-project-governance", "eng-repo-governance"],
    "eng-closed-loop-decisions": [],
    "eng-pm": [],
    "eng-dev": [],
    "eng-qa-reviewer": [],
}
ROUTING_COVERAGE = set(EXPECTED_NAMES[:5])


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter(text):
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    if not match:
        raise ValueError("missing frontmatter")
    values = {}
    for key in ("name", "description"):
        found = re.findall(r"^" + key + r":\s*(.+)$", match.group(1), re.M)
        if len(found) != 1:
            raise ValueError(f"expected exactly one {key}")
        value = found[0].strip()
        if value.startswith('"'):
            value = json.loads(value)
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1].replace("''", "'")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"empty {key}")
        values[key] = value
    return values


def dependency_errors(graph):
    errors = []
    names = set(graph)
    for name, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in names:
                errors.append(f"{name}: missing dependency {dependency}")
    visiting = set()
    visited = set()

    def visit(name):
        if name in visiting:
            errors.append(f"dependency cycle at {name}")
            return
        if name in visited:
            return
        visiting.add(name)
        for dependency in graph.get(name, []):
            if dependency in names:
                visit(dependency)
        visiting.remove(name)
        visited.add(name)

    for name in graph:
        visit(name)
    return errors


def link_errors(path, root):
    errors = []
    text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    for raw_target in re.findall(r"\]\(([^)]+)\)", text):
        target = raw_target.strip().strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith("#") or " " in target:
            continue
        resolved = (path.parent / unquote(parsed.path)).resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            errors.append(f"{path.relative_to(root)}: link escapes repository: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{path.relative_to(root)}: broken link: {target}")
    return errors


def validate(root):
    root = Path(root).resolve()
    errors = []
    routing_scenarios_validated = 0

    try:
        registry = read_json(root / "registry.json")
        entries = registry["skills"]
        names = tuple(entry["name"] for entry in entries)
        if registry.get("schema_version") != 1:
            errors.append("registry schema_version must be 1")
        if names != EXPECTED_NAMES:
            errors.append(f"registry must contain the exact ordered eight Skills: {EXPECTED_NAMES}")
        graph = {entry["name"]: entry.get("dependencies", []) for entry in entries}
        if graph != EXPECTED_DEPENDENCIES:
            errors.append("registry dependency graph does not match the ownership design")
        errors.extend(dependency_errors(graph))

        actual_dirs = {
            str(path.parent.relative_to(root))
            for path in (root / "skills").glob("*/*/SKILL.md")
        }
        expected_dirs = {f"skills/engineering/{name}" for name in EXPECTED_NAMES}
        if actual_dirs != expected_dirs:
            errors.append(f"active Skill directories mismatch: {sorted(actual_dirs ^ expected_dirs)}")

        for entry in entries:
            name = entry["name"]
            folder = root / entry["path"]
            if entry.get("category") != "engineering" or entry.get("path") != f"skills/engineering/{name}":
                errors.append(f"{name}: noncanonical registry path or category")
                continue
            try:
                skill_text = (folder / "SKILL.md").read_text(encoding="utf-8")
                fm = frontmatter(skill_text)
            except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
                errors.append(f"{name}: {exc}")
                continue
            if fm["name"] != name:
                errors.append(f"{name}: frontmatter name mismatch")
            if len(fm["description"]) > 1024:
                errors.append(f"{name}: description is too long")
            if "../../../docs/governance-contract.md" not in skill_text:
                errors.append(f"{name}: shared contract is not referenced")

        discovery = root / ".agents/skills"
        actual_links = {path.name for path in discovery.iterdir()} if discovery.exists() else set()
        if actual_links != set(EXPECTED_NAMES):
            errors.append(f"discovery links mismatch: {sorted(actual_links ^ set(EXPECTED_NAMES))}")
        for name in EXPECTED_NAMES:
            link = discovery / name
            expected = root / "skills/engineering" / name
            if not link.is_symlink() or link.resolve() != expected.resolve():
                errors.append(f"{name}: missing or incorrect discovery symlink")
            elif os.path.isabs(os.readlink(link)):
                errors.append(f"{name}: discovery symlink must be relative")

        routing = read_json(root / "tests/routing_scenarios.json")
        scenarios = routing.get("scenarios", [])
        if routing.get("schema_version") != 1 or not scenarios:
            errors.append("routing scenarios must contain versioned cases")
        scenario_ids = set()
        covered = set()
        for scenario in scenarios:
            scenario_error_count = len(errors)
            required = {"id", "request", "expected_route", "expected_owner_actions", "stop", "forbid"}
            if not required.issubset(scenario):
                errors.append("routing scenario missing required fields")
                continue
            if any(not isinstance(scenario[field], str) or not scenario[field].strip() for field in ("id", "request", "stop")):
                errors.append("routing scenario needs a nonempty id, request, and stop condition")
                continue
            if scenario["id"] in scenario_ids:
                errors.append(f"duplicate routing scenario id {scenario['id']}")
            scenario_ids.add(scenario["id"])
            route = scenario["expected_route"]
            if not isinstance(route, list) or len(route) != len(set(route)) or not set(route).issubset(EXPECTED_NAMES):
                errors.append(f"{scenario['id']}: invalid expected route")
            else:
                covered.update(route)
            for field in ("expected_owner_actions", "forbid"):
                value = scenario[field]
                if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
                    errors.append(f"{scenario['id']}: invalid {field}")
            if len(errors) == scenario_error_count:
                routing_scenarios_validated += 1
        if not ROUTING_COVERAGE.issubset(covered):
            errors.append("routing scenarios do not cover all five governance and decision Skills")

        markdown_paths = list(root.glob("*.md")) + list((root / "docs").rglob("*.md")) + list((root / "skills").rglob("*.md"))
        for path in markdown_paths:
            errors.extend(link_errors(path, root))
            for routed_name in re.findall(r"\beng-[a-z0-9]+(?:-[a-z0-9]+)+\b", path.read_text(encoding="utf-8")):
                if routed_name not in EXPECTED_NAMES:
                    errors.append(f"{path.relative_to(root)}: unknown active routing name {routed_name}")

        private_root_patterns = (
            "/" + "Users" + "/",
            "/" + "home" + "/",
            "C:" + "\\" + "Users" + "\\",
        )
        authored_paths = markdown_paths + list((root / "contracts").rglob("*.json")) + list((root / "skills").rglob("*.json")) + [root / "registry.json", root / "tests/routing_scenarios.json"]
        for path in authored_paths:
            text = path.read_text(encoding="utf-8")
            if any(pattern in text for pattern in private_root_patterns):
                errors.append(f"{path.relative_to(root)}: contains an absolute personal path")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid required repository artifact: {exc}")

    return {
        "status": "pass" if not errors else "fail",
        "skills_checked": len(EXPECTED_NAMES),
        "behavior_cases_executed": 0,
        "routing_scenarios_validated": routing_scenarios_validated,
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = validate(args.root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
