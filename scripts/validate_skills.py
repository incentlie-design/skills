#!/usr/bin/env python3
"""Read-only repository contract check. Not an LLM behavior evaluator or full YAML parser."""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

PREFIXES = {"meta": "meta", "personal": "personal", "engineering": "eng", "product": "product", "content": "content"}
REQUIRED = {"schema_version", "name", "version", "category", "status", "summary", "owners", "tags", "dependencies", "input_contract", "output_contract"}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def scalar(value):
    """Repository SKILL entrypoints use single-line scalars; reject unsupported YAML."""
    value = value.strip()
    if value.startswith('"'):
        return json.loads(value)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    if not value or value[0] in "[{}>|&*!" or ": " in value or " #" in value:
        raise ValueError("Use a one-line quoted name/description scalar")
    return value


def frontmatter(text):
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    if not match:
        raise ValueError("Missing frontmatter")
    result = {}
    for key in ("name", "description"):
        values = re.findall(r"^" + key + r":\s*(.*)$", match.group(1), re.M)
        if len(values) != 1:
            raise ValueError("Expected exactly one " + key)
        result[key] = scalar(values[0])
        if not isinstance(result[key], str) or not result[key].strip():
            raise ValueError("Empty or non-string " + key)
    return result


def within(path, root):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def dependency_errors(entries):
    names = {e["name"] for e in entries}
    graph = {e["name"]: e.get("dependencies", []) for e in entries}
    errors = []
    for name, deps in graph.items():
        for dep in deps:
            if dep not in names:
                errors.append(f"{name}: missing dependency {dep}")
    active, done = set(), set()

    def visit(name):
        if name in active:
            errors.append(f"dependency cycle at {name}")
            return
        if name in done:
            return
        active.add(name)
        for dep in graph.get(name, []):
            if dep in names:
                visit(dep)
        active.remove(name)
        done.add(name)

    for name in graph:
        visit(name)
    return errors


def link_errors(path, root):
    errors = []
    text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    for target in re.findall(r"\]\(([^)]+)\)", text):
        target = target.strip().strip("<>")
        parts = urlsplit(target)
        if parts.scheme or target.startswith("#"):
            continue
        if " " in target:
            continue  # Markdown titles are outside this minimal check.
        resolved = path.parent / unquote(parts.path)
        if not within(resolved, root):
            errors.append(f"{path.relative_to(root)}: link escapes repository: {target}")
        elif not resolved.exists():
            errors.append(f"{path.relative_to(root)}: broken link: {target}")
    return errors


def validate(root, selected=None, check_discovery=False):
    root = Path(root).resolve()
    errors = []
    count = cases_count = 0
    try:
        registry = read_json(root / "registry.json")
        if registry.get("schema_version") != 1:
            raise ValueError("registry schema_version must be 1")
        entries = registry["skills"]
        if not isinstance(entries, list) or not entries:
            raise ValueError("registry.skills must be a non-empty array")
        names = [entry["name"] for entry in entries]
        if len(names) != len(set(names)):
            errors.append("Duplicate skill name in registry")
        errors += dependency_errors(entries)
        if selected and not set(selected).issubset(names):
            errors.append("Unknown --skill name")
        for entry in entries:
            name = entry["name"]
            category = entry["category"]
            if selected and name not in selected:
                continue
            count += 1
            folder = root / entry["path"]
            if entry["path"] != f"skills/{category}/{name}" or not within(folder, root):
                errors.append(f"{name}: noncanonical path")
                continue
            try:
                md = (folder / "SKILL.md").read_text(encoding="utf-8")
                fm = frontmatter(md)
                meta = read_json(folder / "skill.json")
                if REQUIRED - meta.keys():
                    raise ValueError("Missing metadata keys: " + str(sorted(REQUIRED - meta.keys())))
                if meta["schema_version"] != 1:
                    errors.append(f"{name}: unsupported skill schema_version")
                if fm["name"] != name or meta["name"] != name or meta["category"] != category:
                    errors.append(f"{name}: name/category mismatch")
                if category not in PREFIXES or not name.startswith(PREFIXES.get(category, "?") + "-"):
                    errors.append(f"{name}: category prefix mismatch")
                if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)+", name) or len(name) >= 64:
                    errors.append(f"{name}: invalid name")
                if len(fm["description"]) > 1024 or any(c in fm["description"] for c in "<>"):
                    errors.append(f"{name}: invalid description")
                if not re.fullmatch(r"\d+\.\d+\.\d+", meta["version"]):
                    errors.append(f"{name}: invalid version")
                if meta["status"] not in ("draft", "active", "deprecated"):
                    errors.append(f"{name}: invalid status")
                for key in ("owners", "tags"):
                    if not isinstance(meta[key], list) or not meta[key] or not all(isinstance(x, str) and x.strip() for x in meta[key]):
                        errors.append(f"{name}: invalid {key}")
                for key in ("summary", "input_contract", "output_contract"):
                    if not isinstance(meta[key], str) or not meta[key].strip():
                        errors.append(f"{name}: invalid {key}")
                if sorted(meta["dependencies"]) != sorted(entry.get("dependencies", [])):
                    errors.append(f"{name}: registry/metadata dependency mismatch")
                cases = read_json(folder / "tests/cases.json")
                if not isinstance(cases, list) or len(cases) < 3:
                    raise ValueError("Expected at least three behavior cases")
                kinds, ids = set(), set()
                for case in cases:
                    if not {"id", "kind", "prompt", "expect"}.issubset(case):
                        raise ValueError("Case missing required fields")
                    if case["id"] in ids:
                        errors.append(f"{name}: duplicate case id")
                    ids.add(case["id"])
                    kinds.add(case["kind"])
                    if not isinstance(case["prompt"], str) or not case["prompt"].strip():
                        errors.append(f"{name}: empty prompt")
                    if not isinstance(case["expect"], list) or not case["expect"] or not all(isinstance(x, str) and x.strip() for x in case["expect"]):
                        errors.append(f"{name}: empty/non-string assertions")
                if not {"happy", "missing_input", "boundary"}.issubset(kinds):
                    errors.append(f"{name}: missing happy/missing_input/boundary coverage")
                cases_count += len(cases)
                for path in folder.rglob("*.md"):
                    errors += link_errors(path, root)
                if check_discovery:
                    link = root / ".agents/skills" / name
                    if not link.is_symlink() or link.resolve() != folder.resolve():
                        errors.append(f"{name}: missing/incorrect discovery symlink")
            except (OSError, ValueError, KeyError, TypeError) as exc:
                errors.append(f"{name}: {exc}")
        if not selected:
            actual = {str(p.parent.relative_to(root)) for p in (root / "skills").glob("*/*/SKILL.md")}
            declared = {e["path"] for e in entries}
            if actual != declared:
                errors.append(f"Registry/file mismatch: {sorted(actual ^ declared)}")
            for doc in ("AGENTS.md", "README.md"):
                text = (root / doc).read_text(encoding="utf-8")
                for name in names:
                    if name not in text:
                        errors.append(f"{doc}: skill not registered: {name}")
                errors += link_errors(root / doc, root)
            for path in (root / "skills").rglob(".git"):
                errors.append(f"Nested repository forbidden: {path.relative_to(root)}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"Invalid registry or required root document: {exc}")
    return {"status": "fail" if errors else "pass", "skills_checked": count, "cases_defined": cases_count,
            "behavior_cases_executed": 0, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--skill", action="append")
    parser.add_argument("--check-discovery", action="store_true")
    args = parser.parse_args()
    report = validate(args.root, args.skill, args.check_discovery)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
