#!/usr/bin/env python3
"""Validate ten engineering Skills plus the optional content catalog using the standard library."""

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
    "eng-wiki-authoring",
    "eng-pr-feedback-triage",
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
    "eng-wiki-authoring": [],
    "eng-pr-feedback-triage": [],
}
ROUTING_COVERAGE = set(EXPECTED_NAMES[:5]) | {"eng-pr-feedback-triage"}
VISUAL_CONTRACT_LINK = "../../../docs/prd-td-visual-contract.md"
VISUAL_CONTRACT_SKILLS = {"eng-pm", "eng-dev", "eng-qa-reviewer"}
CONTENT_CONTRACT_LINK = "../../../docs/content-production-contract.md"
IO_CONTRACT_LINK = "../../../docs/content-skill-io.md"
CONTENT_R_IDS = {"R1", "R2", "R3", "R4", "R5", "R6"}
CONTENT_INDEX_LIMIT = 200
CONTENT_INDEX_REQUIRED = (
    "id",
    "title",
    "url",
    "type",
    "category",
    "quality",
    "r_alignment",
    "include",
    "security",
    "why",
)
CONTENT_INCLUDE = {"yes", "maybe", "no"}
CONTENT_SECURITY = {"none", "review", "exclude"}
SECRETISH = re.compile(r"(api[_-]?key|secret[_-]?key|begin [a-z ]*private key|sk-[a-z0-9]{16,})", re.I)
REQUIREMENT_TEMPLATE_LINK = "../../../docs/requirement-reader-first-template.md"
REQUIREMENT_TEMPLATE_SECTIONS = (
    "# Reader-first Requirement template",
    "## One-page review",
    "## Core business flows",
    "## Acceptance criteria",
    "## Ownership boundaries",
    "## Decisions requested now",
    "## Next artifacts and stop conditions",
    "## Visual index",
)
FULL_VISUAL_TEMPLATE_SECTIONS = (
    "# PRD and TD visual template",
    "`full-visual-design-package`",
    "| Format profile | `full-visual-design-package` |",
)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


UNQUOTED_UNSAFE = re.compile(r":\s|#|^[\s]*[&*!%@`{,|?>]")


def frontmatter(text):
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    if not match:
        raise ValueError("missing frontmatter")
    values = {}
    for key in ("name", "description"):
        found = re.findall(r"^" + key + r":\s*(.+)$", match.group(1), re.M)
        if len(found) != 1:
            raise ValueError(f"expected exactly one {key}")
        raw = found[0].strip()
        if raw.startswith('"'):
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{key} is not a valid quoted JSON string: {exc}") from exc
        elif raw.startswith("'") and raw.endswith("'"):
            value = raw[1:-1].replace("''", "'")
        else:
            if UNQUOTED_UNSAFE.search(raw):
                raise ValueError(
                    f"{key} has unquoted YAML-unsafe characters; wrap the value in double quotes"
                )
            value = raw
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
    content_names = []
    index_count = 0

    try:
        registry = read_json(root / "registry.json")
        entries = registry["skills"]
        names = tuple(entry["name"] for entry in entries)
        if registry.get("schema_version") != 1:
            errors.append("registry schema_version must be 1")
        if names != EXPECTED_NAMES:
            errors.append(f"registry must contain the exact ordered ten Skills: {EXPECTED_NAMES}")
        graph = {entry["name"]: entry.get("dependencies", []) for entry in entries}
        if graph != EXPECTED_DEPENDENCIES:
            errors.append("registry dependency graph does not match the ownership design")
        errors.extend(dependency_errors(graph))

        engineering_dirs = {
            str(path.parent.relative_to(root))
            for path in (root / "skills" / "engineering").glob("*/SKILL.md")
        }
        expected_engineering = {f"skills/engineering/{name}" for name in EXPECTED_NAMES}
        if engineering_dirs != expected_engineering:
            errors.append(
                f"engineering Skill directories mismatch: {sorted(engineering_dirs ^ expected_engineering)}"
            )
        foreign_dirs = {
            str(path.parent.relative_to(root))
            for path in (root / "skills").glob("*/*/SKILL.md")
            if path.parts[-3] not in {"engineering", "content"}
        }
        if foreign_dirs:
            errors.append(f"unsupported Skill category directories: {sorted(foreign_dirs)}")
        content_dirs = sorted(
            path.parent
            for path in (root / "skills" / "content").glob("*/SKILL.md")
        ) if (root / "skills" / "content").exists() else []
        content_names = []
        for folder in content_dirs:
            name = folder.name
            content_names.append(name)
            try:
                skill_text = (folder / "SKILL.md").read_text(encoding="utf-8")
                fm = frontmatter(skill_text)
            except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
                errors.append(f"{name}: {exc}")
                continue
            if fm["name"] != name:
                errors.append(f"{name}: frontmatter name mismatch")
            if not name.startswith("content-"):
                errors.append(f"{name}: content Skill name must start with content-")
            if len(fm["description"]) > 1024:
                errors.append(f"{name}: description is too long")
            if CONTENT_CONTRACT_LINK not in skill_text:
                errors.append(f"{name}: content production contract is not referenced")
            if IO_CONTRACT_LINK not in skill_text:
                errors.append(f"{name}: content I/O contract is not referenced")
            if SECRETISH.search(skill_text):
                errors.append(f"{name}: looks like it embeds a secret")
        io_dir = root / "skills" / "content" / "io"
        if content_dirs:
            for required in ("fields.json", "skills.json", "roles.json", "envelope.schema.json"):
                if not (io_dir / required).exists():
                    errors.append(f"content I/O catalog missing {required}")
            if (io_dir / "fields.json").exists() and (io_dir / "skills.json").exists() and (io_dir / "roles.json").exists():
                field_book = read_json(io_dir / "fields.json")
                skill_book = read_json(io_dir / "skills.json")
                role_book = read_json(io_dir / "roles.json")
                field_names = set((field_book.get("fields") or {}).keys())
                role_names = set((role_book.get("roles") or {}).keys())
                listed = skill_book.get("skills") or {}
                if set(listed) != set(content_names):
                    errors.append(
                        f"content I/O skills.json mismatch: {sorted(set(listed) ^ set(content_names))}"
                    )
                known_kinds = set()
                for skill_name, spec in listed.items():
                    if not isinstance(spec, dict):
                        errors.append(f"{skill_name}: I/O spec must be an object")
                        continue
                    for key in ("r_alignment", "roles", "required_inputs", "optional_inputs", "outputs", "forbidden"):
                        if key not in spec:
                            errors.append(f"{skill_name}: missing I/O key {key}")
                    for field in list(spec.get("required_inputs") or []) + list(spec.get("optional_inputs") or []):
                        if field not in field_names:
                            errors.append(f"{skill_name}: unknown field {field}")
                    for role in spec.get("roles") or []:
                        if role not in role_names:
                            errors.append(f"{skill_name}: unknown role {role}")
                    if set(spec.get("r_alignment") or []) - CONTENT_R_IDS:
                        errors.append(f"{skill_name}: I/O r_alignment must be R1–R6")
                    outputs = spec.get("outputs") or []
                    if not isinstance(outputs, list) or not outputs:
                        errors.append(f"{skill_name}: outputs must be a nonempty list")
                    kinds = []
                    for item in outputs:
                        kind = item.get("artifact_kind") if isinstance(item, dict) else None
                        if not kind:
                            errors.append(f"{skill_name}: output missing artifact_kind")
                            continue
                        kinds.append(kind)
                        for consumer in item.get("consumers") or []:
                            if consumer not in role_names:
                                errors.append(f"{skill_name}: unknown consumer role {consumer}")
                    if len(kinds) != len(set(kinds)):
                        errors.append(f"{skill_name}: duplicate artifact_kind")
                    known_kinds.update(kinds)
                    skill_text = (root / "skills" / "content" / skill_name / "SKILL.md").read_text(encoding="utf-8")
                    for field in spec.get("required_inputs") or []:
                        if f"`{field}`" not in skill_text:
                            errors.append(f"{skill_name}: SKILL.md missing required field `{field}`")
                    for kind in kinds:
                        if f"`{kind}`" not in skill_text:
                            errors.append(f"{skill_name}: SKILL.md missing artifact_kind `{kind}`")
                    method = skill_text.split("## 方法", 1)
                    if len(method) != 2:
                        errors.append(f"{skill_name}: SKILL.md missing ## 方法")
                    else:
                        method_body = method[1].split("\n## ", 1)[0]
                        stages = [line for line in method_body.splitlines() if line.startswith("### ")]
                        if len(stages) < 3:
                            errors.append(
                                f"{skill_name}: method must fan out into at least 3 ### stages, found {len(stages)}"
                            )
                    for item in outputs:
                        for field in item.get("payload_fields") or []:
                            if f"`{field}`" not in skill_text:
                                errors.append(f"{skill_name}: SKILL.md missing payload field `{field}`")
                for role, body in (role_book.get("roles") or {}).items():
                    for skill_name in body.get("skills") or []:
                        if skill_name not in listed:
                            errors.append(f"role {role}: unknown skill {skill_name}")
                        elif role not in (listed[skill_name].get("roles") or []):
                            errors.append(f"role {role}: skill {skill_name} does not list this role")
        if len(content_names) != len(set(content_names)):
            errors.append("duplicate content Skill directory names")

        content_registry_path = root / "skills" / "content" / "registry.json"
        if content_dirs and not content_registry_path.exists():
            errors.append("content catalog is missing skills/content/registry.json")
        content_registry_names = []
        if content_registry_path.exists():
            content_registry = read_json(content_registry_path)
            if content_registry.get("schema_version") != 1:
                errors.append("content registry schema_version must be 1")
            if content_registry.get("catalog") != "content":
                errors.append("content registry catalog must be 'content'")
            entries_c = content_registry.get("skills")
            if not isinstance(entries_c, list):
                errors.append("content registry skills must be a list")
                entries_c = []
            for entry in entries_c:
                if not isinstance(entry, dict):
                    errors.append("content registry entry must be an object")
                    continue
                name = entry.get("name")
                path = entry.get("path")
                alignment = entry.get("r_alignment")
                status = entry.get("status")
                if entry.get("category") != "content":
                    errors.append(f"{name}: content registry category must be content")
                if not isinstance(name, str) or not name.startswith("content-"):
                    errors.append(f"{name}: invalid content registry name")
                    continue
                if path != f"skills/content/{name}":
                    errors.append(f"{name}: content registry path must be skills/content/{name}")
                if not isinstance(alignment, list) or not alignment or set(alignment) - CONTENT_R_IDS:
                    errors.append(f"{name}: r_alignment must be a nonempty subset of R1–R6")
                if status not in {"draft", "active", "deprecated"}:
                    errors.append(f"{name}: invalid content status")
                content_registry_names.append(name)
            if len(content_registry_names) != len(set(content_registry_names)):
                errors.append("content registry names are not unique")
            if set(content_registry_names) != set(content_names):
                errors.append(
                    f"content registry/directories mismatch: {sorted(set(content_registry_names) ^ set(content_names))}"
                )

        index_path = root / "skills" / "content" / "index.json"
        index_count = 0
        if content_dirs and not index_path.exists():
            errors.append("content catalog is missing skills/content/index.json")
        if index_path.exists():
            index = read_json(index_path)
            if index.get("schema_version") != 1:
                errors.append("content index schema_version must be 1")
            entries_i = index.get("entries")
            if not isinstance(entries_i, list):
                errors.append("content index entries must be a list")
                entries_i = []
            if len(entries_i) > CONTENT_INDEX_LIMIT:
                errors.append(f"content index exceeds {CONTENT_INDEX_LIMIT} entries")
            ids = []
            urls = []
            for entry in entries_i:
                if not isinstance(entry, dict):
                    errors.append("content index entry must be an object")
                    continue
                missing = [key for key in CONTENT_INDEX_REQUIRED if key not in entry]
                if missing:
                    errors.append(f"content index entry missing {missing}")
                    continue
                ids.append(entry["id"])
                urls.append(entry["url"])
                if not isinstance(entry["title"], str) or not entry["title"].strip():
                    errors.append(f"{entry['id']}: empty title")
                if not isinstance(entry["url"], str) or not entry["url"].startswith(("https://", "http://")):
                    errors.append(f"{entry['id']}: url must be http(s)")
                if entry["include"] not in CONTENT_INCLUDE:
                    errors.append(f"{entry['id']}: invalid include")
                if entry["security"] not in CONTENT_SECURITY:
                    errors.append(f"{entry['id']}: invalid security")
                alignment = entry["r_alignment"]
                if not isinstance(alignment, list) or set(alignment) - CONTENT_R_IDS:
                    errors.append(f"{entry['id']}: r_alignment must be R1–R6")
                if SECRETISH.search(json.dumps(entry, ensure_ascii=False)):
                    errors.append(f"{entry['id']}: looks like it embeds a secret")
            if len(ids) != len(set(ids)):
                errors.append("content index ids are not unique")
            if len(urls) != len(set(urls)):
                errors.append("content index urls are not unique")
            index_count = len(entries_i)

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
            if name in VISUAL_CONTRACT_SKILLS and VISUAL_CONTRACT_LINK not in skill_text:
                errors.append(f"{name}: PRD/TD visual contract is not referenced")
            if name == "eng-pm":
                if REQUIREMENT_TEMPLATE_LINK not in skill_text:
                    errors.append("eng-pm: reader-first Requirement template is not referenced")
                if "## Requirement format profiles" not in skill_text:
                    errors.append("eng-pm: Requirement format profiles are missing")
                if "`full-visual-design-package`" not in skill_text or "`reader-first-requirement`" not in skill_text:
                    errors.append("eng-pm: Requirement profile markers are incomplete")

        visual_contract = (root / "docs" / "prd-td-visual-contract.md").read_text(encoding="utf-8")
        if (
            "## Artifact profiles" not in visual_contract
            or "### `full-visual-design-package`" not in visual_contract
            or "### `reader-first-requirement`" not in visual_contract
        ):
            errors.append("PRD/TD visual contract: selectable Requirement profiles are incomplete")

        requirement_template = (root / "docs" / "requirement-reader-first-template.md").read_text(encoding="utf-8")
        for section in REQUIREMENT_TEMPLATE_SECTIONS:
            if section not in requirement_template:
                errors.append(f"reader-first Requirement template: missing section {section}")

        full_visual_template = (root / "docs" / "prd-td-visual-template.md").read_text(encoding="utf-8")
        for section in FULL_VISUAL_TEMPLATE_SECTIONS:
            if section not in full_visual_template:
                errors.append(f"full visual template: missing section {section}")

        discovery = root / ".agents/skills"
        actual_links = {path.name for path in discovery.iterdir()} if discovery.exists() else set()
        missing_engineering = set(EXPECTED_NAMES) - actual_links
        if missing_engineering:
            errors.append(f"missing engineering discovery links: {sorted(missing_engineering)}")
        extra_links = actual_links - set(EXPECTED_NAMES)
        unexpected_extra = extra_links - set(content_names)
        if unexpected_extra:
            errors.append(f"unexpected discovery links: {sorted(unexpected_extra)}")
        for name in EXPECTED_NAMES:
            link = discovery / name
            expected = root / "skills/engineering" / name
            if not link.is_symlink() or link.resolve() != expected.resolve():
                errors.append(f"{name}: missing or incorrect discovery symlink")
            elif os.path.isabs(os.readlink(link)):
                errors.append(f"{name}: discovery symlink must be relative")
        for name in extra_links & set(content_names):
            link = discovery / name
            expected = root / "skills" / "content" / name
            if not link.is_symlink() or link.resolve() != expected.resolve():
                errors.append(f"{name}: missing or incorrect content discovery symlink")
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
            errors.append("routing scenarios do not cover all governance and advisory Skills")

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
        authored_paths = (
            markdown_paths
            + list((root / "contracts").rglob("*.json"))
            + list((root / "skills").rglob("*.json"))
            + [root / "registry.json", root / "tests/routing_scenarios.json"]
        )
        for path in authored_paths:
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            if any(pattern in text for pattern in private_root_patterns):
                errors.append(f"{path.relative_to(root)}: contains an absolute personal path")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid required repository artifact: {exc}")
        content_names = []
        index_count = 0

    return {
        "status": "pass" if not errors else "fail",
        "skills_checked": len(EXPECTED_NAMES) + len(content_names),
        "engineering_skills_checked": len(EXPECTED_NAMES),
        "content_skills_checked": len(content_names),
        "content_index_entries": index_count,
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
