#!/usr/bin/env python3
"""Read-only, standard-library evidence gates. Not a code/model/release runner."""

import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


GRAPH = {
    "spec": (),
    "design": ("spec",),
    "test_plan": ("spec", "design"),
    "product_review": ("spec", "design", "test_plan"),
    "design_review": ("spec", "design", "test_plan"),
    "test_plan_review": ("spec", "design", "test_plan"),
    "implementation": ("product_review", "design_review", "test_plan_review"),
    "code_review": ("implementation",),
    "targeted_test": ("implementation",),
}
REVIEW_AUTHORS = {
    "product_review": "spec", "design_review": "design",
    "test_plan_review": "test_plan", "code_review": "implementation",
}
STATUSES = {"pass", "revise", "blocked"}
MAX_BYTES = 8 * 1024 * 1024


class GateError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise GateError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value, label, allow_empty=False):
    require(isinstance(value, list), f"{label}: expected list")
    require(allow_empty or bool(value), f"{label}: missing values")
    require(all(nonempty(item) for item in value), f"{label}: invalid value")
    require(len(set(value)) == len(value), f"{label}: duplicates")
    return value


def integer(value, label, low, high):
    require(type(value) is int and low <= value <= high, f"{label}: out of budget/range")


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(data.encode()).hexdigest()


def hash_value(value, label, lengths=(64,)):
    require(isinstance(value, str) and len(value) in lengths
            and re.fullmatch("[0-9a-f]+", value), f"{label}: expected full immutable hash")


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path):
    require(path.stat().st_size <= MAX_BYTES, "JSON exceeds local size budget")
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys)


def local_path(root, name):
    require(nonempty(name), "missing relative artifact path")
    path = PurePosixPath(name)
    require(not path.is_absolute() and ".." not in path.parts and ".git" not in path.parts
            and str(path) == name and "\\" not in name, f"unsafe artifact path: {name}")
    resolved = (root / name).resolve()
    require(resolved.is_relative_to(root.resolve()) and resolved.is_file(),
            f"missing or escaping artifact: {name}")
    require(resolved.stat().st_size <= MAX_BYTES, f"artifact too large: {name}")
    return resolved


def file_ref(root, name):
    return {"path": name, "sha256": hashlib.sha256(local_path(root, name).read_bytes()).hexdigest()}


def check_refs(root, refs, label):
    require(isinstance(refs, list) and bool(refs), f"{label}: missing evidence/artifacts")
    paths = []
    for ref in refs:
        require(isinstance(ref, dict), f"{label}: invalid reference")
        hash_value(ref["sha256"], label)
        require(file_ref(root, ref["path"]) == ref, f"{label}: stale content: {ref['path']}")
        paths.append(ref["path"])
    require(len(paths) == len(set(paths)), f"{label}: duplicate paths")
    return paths


def git_read(root, *args):
    # Only callers below supply the command vocabulary; JSON never supplies argv.
    result = subprocess.run(["git", "--no-optional-locks", "--no-pager", "-c", "core.fsmonitor=false",
                             "-C", str(root), *args], capture_output=True, timeout=5)
    require(result.returncode == 0, "Git pin/content check failed: " + args[0])
    return result.stdout


def check_git(root, base, head, checkout=True):
    require(Path(git_read(root, "rev-parse", "--show-toplevel").decode().strip()).resolve()
            == root.resolve(), "--repo must be the Git worktree root")
    for commit in (base, head):
        require(git_read(root, "rev-parse", "--verify", commit + "^{commit}").decode().strip()
                == commit, "commit pin does not resolve exactly")
    git_read(root, "merge-base", "--is-ancestor", base, head)
    if checkout:
        require(git_read(root, "rev-parse", "HEAD").decode().strip() == head, "checkout head changed")
        git_read(root, "diff", "--no-ext-diff", "--no-textconv", "--quiet", "HEAD", "--")


def check_common(doc, root, base, head, allow_mock):
    require(type(doc["schema_version"]) is int and doc["schema_version"] == 1, "unknown schema")
    for key in ("run_id", "change_id", "repo"):
        require(nonempty(doc[key]), f"missing {key}")
    require(doc["mode"] == "actual" or (allow_mock and doc["mode"] == "mock"),
            "mock/unknown mode cannot enter actual gates")
    hash_value(doc["base_commit"], "base_commit", (40, 64))
    hash_value(doc["head_commit"], "head_commit", (40, 64))
    require(doc["base_commit"] == base and doc["head_commit"] == head, "base/head pin changed")
    integer(doc["artifact_revision"], "artifact_revision", 1, 3)
    require(root.is_dir(), "missing target repo")


def feature_digest(doc):
    snapshot = copy.deepcopy(doc)
    snapshot.pop("retry_history", None)
    for node in snapshot["nodes"].values():
        node.pop("binding", None)
    return digest(snapshot)


def check_retries(doc, current, root, nodes):
    history = doc["retry_history"]
    require(isinstance(history, list) and len(history) <= 2, "maximum two conditional retries")
    require(doc["artifact_revision"] == len(history) + 1, "revision/retry history mismatch")
    previous = None
    seen = set()
    for index, retry in enumerate(history, 1):
        require(retry["status"] == "revise" and retry["failed_node"] in nodes,
                "retry needs a known revise node; blocked is not retryable")
        require(type(retry["from_revision"]) is int and type(retry["to_revision"]) is int
                and retry["from_revision"] == index and retry["to_revision"] == index + 1,
                "retry revision chain broken")
        for key in ("reason", "owner"):
            require(nonempty(retry[key]), f"retry missing {key}")
        before, after = retry["from_snapshot"], retry["to_snapshot"]
        hash_value(before, "retry from_snapshot")
        hash_value(after, "retry to_snapshot")
        require(before != after and after not in seen, "retry did not change content or loops")
        require(previous is None or previous == before, "retry snapshot chain broken")
        seen.update((before, after))
        previous = after
        check_refs(root, retry["evidence"], "retry evidence")
    require(previous is None or previous == current, "retry targets a stale snapshot")


def check_review(node, name, doc):
    review = node["review"]
    require(review["status"] in STATUSES and review["status"] == node["status"], "review status mismatch")
    require(nonempty(review["reviewer"]) and review["reviewer"] == node["owner"], "missing review owner")
    require(review["reviewer"] not in (doc["nodes"]["implementation"]["owner"],
                                      doc["nodes"][REVIEW_AUTHORS[name]]["owner"]),
            "implementer/author cannot sign own review")
    require(type(review["reviewed_revision"]) is int
            and review["reviewed_revision"] == doc["artifact_revision"], "stale review revision")
    require(review["scope"] == doc["scope"], "review scope mismatch")
    require(isinstance(review["findings"], list), "missing review findings")
    strings(review["non_blocking_suggestions"], "review suggestions", allow_empty=True)
    ids = set()
    for finding in review["findings"]:
        require(re.fullmatch(r"REV-\d{3,}", finding["id"]) and finding["id"] not in ids, "invalid finding ID")
        ids.add(finding["id"])
        require(finding["severity"] in {"blocking", "major", "minor"}, "unknown finding severity")
        for key in ("evidence", "impact", "minimal_fix", "owner", "acceptance"):
            require(nonempty(finding[key]), f"finding missing {key}")
        require(node["status"] != "pass" or finding["severity"] == "minor", "blocking finding cannot pass")


def check_test_report(report, revision, scope, ac, root, status):
    require(type(report["revision"]) is int and report["revision"] == revision, "stale test report revision")
    require(report["scope"] == scope, "test scope mismatch")
    require(nonempty(report["conclusion"]), "missing test conclusion")
    strings(report["gaps"], "test gaps", allow_empty=True)
    results = report["results"]
    require(isinstance(results, list) and bool(results), "missing test results")
    covered, ids = set(), set()
    for result in results:
        require(re.fullmatch(r"TC-\d{3,}", result["id"]) and result["id"] not in ids, "invalid test ID")
        ids.add(result["id"])
        require(result["status"] in {"pass", "fail", "blocked", "not_run"}, "unknown test status")
        mapped = strings(result["ac"], "test AC mapping")
        require(set(mapped) <= set(ac), "unknown AC in test result")
        covered.update(mapped)
        check_refs(root, result["evidence"], "test result")
        require(status != "pass" or result["status"] == "pass", "non-passing test cannot pass gate")
    require(status != "pass" or (covered == set(ac) and not report["gaps"]), "untested AC or test gap")


def blocked(error, trace=None):
    return {"status": "blocked", "reasons": [str(error)], "trace": trace or [],
            "retry_allowed": False, "release_authorized": False}


def evaluate_feature(doc, root, base, head, *, allow_mock=False, checkout=True):
    """Evaluate one supplied snapshot. Never generate artifacts or run test commands."""
    trace = []
    root = Path(root).resolve()
    try:
        check_common(doc, root, base, head, allow_mock)
        require(doc["kind"] == "feature", "not a feature manifest")
        scope = strings(doc["scope"], "scope")
        strings(doc["dependencies"], "dependencies", allow_empty=True)
        strings(doc["conflicts"], "conflicts", allow_empty=True)
        require(doc["change_id"] not in doc["dependencies"], "feature depends on itself")
        require(nonempty(doc["rollback"]), "missing rollback plan")
        require(isinstance(doc["ac"], list) and bool(doc["ac"]), "missing AC")
        ac = []
        for item in doc["ac"]:
            require(re.fullmatch(r"AC-\d{3,}", item["id"]) and nonempty(item["criterion"]), "invalid AC")
            ac.append(item["id"])
        strings(ac, "AC IDs")
        nodes = doc["nodes"]
        require(set(nodes) == set(GRAPH), "missing/unknown required feature nodes")
        binding = feature_digest(doc)
        check_retries(doc, binding, root, GRAPH)
        revision = doc["artifact_revision"]
        for name, parents in GRAPH.items():
            node = nodes[name]
            require(node["status"] in STATUSES, f"{name}: unknown status")
            require(type(node["artifact_revision"]) is int and node["artifact_revision"] == revision
                    and node["binding"] == binding,
                    f"{name}: stale revision/content binding")
            for field in ("owner", "next_owner"):
                require(nonempty(node[field]), f"{name}: missing {field}")
            artifacts = check_refs(root, node["artifacts"], name)
            evidence = check_refs(root, node["evidence"], name + " evidence")
            expected_inputs = {parent: {"artifact_revision": revision,
                                        "artifacts": nodes[parent]["artifacts"]} for parent in parents}
            require(node["inputs"] == expected_inputs
                    and all(type(source["artifact_revision"]) is int for source in node["inputs"].values()),
                    f"{name}: stale/missing upstream inputs")
            read_set = strings(node["read_set"], name + " read_set")
            write_set = strings(node["write_set"], name + " write_set", allow_empty=True)
            required_reads = set(evidence) | {ref["path"] for parent in parents for ref in nodes[parent]["artifacts"]}
            require(required_reads <= set(read_set), f"{name}: incomplete read_set")
            require(set(write_set) <= set(artifacts), f"{name}: write_set escapes artifacts")
            actions = strings(node["allowed_actions"], name + " allowed_actions")
            require(set(actions) <= {"read", "write_local"}, f"{name}: unauthorized action")
            require(not write_set or "write_local" in actions, f"{name}: undeclared write action")
            strings(node["unresolved_issues"], name + " unresolved_issues", allow_empty=True)
            require(node["status"] != "pass" or not node["unresolved_issues"], f"{name}: unresolved issues")
            if name in REVIEW_AUTHORS or name == "targeted_test":
                require(not write_set and actions == ["read"], f"{name}: assessment must be read-only")
            if name in REVIEW_AUTHORS:
                check_review(node, name, doc)
            if name == "targeted_test":
                check_test_report(node["test_report"], revision, scope, ac, root, node["status"])
            trace.append({"node": name, "status": node["status"]})
            if node["status"] != "pass":
                return {"status": node["status"], "reasons": [f"{name}: {node['status']}"],
                        "next_owner": node["next_owner"], "trace": trace,
                        "retry_allowed": node["status"] == "revise" and revision < 3,
                        "release_authorized": False}
        require(set(ref["path"] for ref in nodes["implementation"]["artifacts"]) == set(scope),
                "implementation artifacts must exactly cover write scope")
        if doc["mode"] == "actual":
            check_git(root, base, head, checkout)
            changed = set(filter(None, git_read(root, "diff", "--no-ext-diff", "--no-textconv",
                                               "--name-only", "-z", base, head, "--").decode().split("\0")))
            require(changed == set(scope), "declared scope differs from committed diff")
            for ref in nodes["implementation"]["artifacts"]:
                blob = git_read(root, "show", head + ":" + ref["path"])
                require(hashlib.sha256(blob).hexdigest() == ref["sha256"], "implementation not at pinned commit")
        candidate = {key: copy.deepcopy(doc[key]) for key in
                     ("schema_version", "run_id", "change_id", "repo", "base_commit", "artifact_revision",
                      "mode", "scope", "ac", "dependencies", "conflicts", "rollback")}
        candidate.update({"status": "candidate", "commit": head, "baseline": base,
                          "review_evidence": {name: nodes[name]["evidence"] for name in REVIEW_AUTHORS},
                          "test_evidence": nodes["targeted_test"]["test_report"],
                          "source_digest": binding, "source": copy.deepcopy(doc), "release_authorized": False})
        return {"status": "candidate", "candidate": candidate, "trace": trace,
                "retry_allowed": False, "release_authorized": False}
    except (ValueError, KeyError, TypeError, AttributeError, OSError, subprocess.SubprocessError) as error:
        return blocked(error, trace)


def candidate_order(candidates):
    require(isinstance(candidates, list) and bool(candidates), "empty candidate set")
    indexed = {item["change_id"]: item for item in candidates}
    require(len(indexed) == len(candidates), "duplicate candidate IDs")
    for item in candidates:
        require(set(item["dependencies"]) <= set(indexed), "missing candidate dependency")
        require(not set(item["conflicts"]) & set(indexed), "declared candidate conflict")
    owners = {}
    for item in candidates:
        for path in item["scope"]:
            require(path not in owners, f"same-file conflict: {path}")
            owners[path] = item["change_id"]
    order = []
    pending = set(indexed)
    while pending:
        ready = sorted(name for name in pending if set(indexed[name]["dependencies"]) <= set(order))
        require(bool(ready), "candidate dependency cycle")
        order.extend(ready)
        pending.difference_update(ready)
    return order


def release_digest(doc):
    # Validation results/usage are post-freeze evidence, never part of their own binding.
    fields = ("schema_version", "kind", "mode", "run_id", "change_id", "repo", "base_commit",
              "head_commit", "artifact_revision", "integration_owner", "version_plan",
              "validation_scope", "budget", "rollback", "candidates")
    snapshot = {key: doc[key] for key in fields}
    snapshot["dependency_order"] = candidate_order(doc["candidates"])
    return digest(snapshot)


def check_version(plan):
    require(plan["level"] in {"patch", "minor", "major"}, "unknown version compatibility level")
    versions = []
    for key in ("from", "to"):
        require(isinstance(plan[key], str) and re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", plan[key]),
                "v1 version plan requires stable x.y.z SemVer")
        versions.append(tuple(map(int, plan[key].split("."))))
    old, new = versions
    level = {"major": 0, "minor": 1, "patch": 2}[plan["level"]]
    require(new[:level] == old[:level] and new[level] > old[level]
            and all(value == 0 for value in new[level + 1:]), "version bump disagrees with compatibility")
    require(nonempty(plan["migration"]), "missing migration/compatibility explanation")


def evaluate_release(doc, root, base, head, *, allow_mock=False):
    """Revalidate candidates and an externally produced frozen integration snapshot."""
    root = Path(root).resolve()
    try:
        check_common(doc, root, base, head, allow_mock)
        require(doc["kind"] == "release", "not an integration manifest")
        require(nonempty(doc["integration_owner"]) and nonempty(doc["rollback"]), "missing owner/rollback")
        check_version(doc["version_plan"])
        validation_scope = strings(doc["validation_scope"], "validation_scope")
        order = candidate_order(doc["candidates"])
        for candidate in doc["candidates"]:
            require(candidate["mode"] == doc["mode"] and candidate["repo"] == doc["repo"], "mixed mode/repo candidate")
            require(candidate["baseline"] == base, "candidate baseline changed")
            checked = evaluate_feature(candidate["source"], root, base, candidate["commit"],
                                       allow_mock=allow_mock, checkout=False)
            require(checked["status"] == "candidate", "invalid/stale candidate: " + candidate["change_id"]
                    + " " + "; ".join(checked.get("reasons", [])))
            require(checked["candidate"] == candidate, "candidate differs from its source evidence")
        frozen = release_digest(doc)
        require(doc["freeze_digest"] == frozen, "stale freeze: candidates/base/head/version/plan changed")
        check_retries(doc, frozen, root, {"integration_validation"})
        budget, usage = doc["budget"], doc["usage"]
        integer(budget["max_attempts"], "integration max_attempts", 1, 2)
        integer(budget["max_minutes"], "integration max_minutes", 1, 10)
        integer(usage["attempts"], "integration attempts", 1, budget["max_attempts"])
        require(usage["attempts"] == doc["artifact_revision"], "integration attempt/revision mismatch")
        require(type(usage["minutes"]) in (int, float) and 0 <= usage["minutes"] <= budget["max_minutes"],
                "integration time budget exhausted/invalid")
        report = doc["validation"]
        require(report["status"] in STATUSES, "unknown integration validation status")
        require(report["freeze_digest"] == frozen and report["head_commit"] == head
                and type(report["revision"]) is int and report["revision"] == doc["artifact_revision"],
                "stale integration evidence")
        require(nonempty(report["reviewer"]) and report["reviewer"] != doc["integration_owner"],
                "integration validation requires an independent reviewer")
        check_refs(root, report["evidence"], "integration evidence")
        require(report["scope"] == validation_scope, "integration validation scope mismatch")
        require(isinstance(report["results"], dict) and set(report["results"]) == set(validation_scope),
                "missing/unknown integration check")
        require(all(value in {"pass", "fail", "blocked", "not_run"} for value in report["results"].values()),
                "unknown integration check status")
        require(report["status"] != "pass" or all(value == "pass" for value in report["results"].values()),
                "non-passing integration check")
        if doc["mode"] == "actual":
            check_git(root, base, head)
            for item in doc["candidates"]:
                git_read(root, "merge-base", "--is-ancestor", item["commit"], head)
        if report["status"] != "pass":
            return {"status": report["status"], "reasons": ["integration_validation: " + report["status"]],
                    "next_owner": doc["integration_owner"],
                    "retry_allowed": report["status"] == "revise" and usage["attempts"] < budget["max_attempts"],
                    "release_authorized": False}
        manifest = {key: copy.deepcopy(doc[key]) for key in
                    ("schema_version", "run_id", "change_id", "repo", "base_commit", "head_commit",
                     "artifact_revision", "mode", "freeze_digest", "version_plan", "validation_scope", "rollback")}
        manifest.update({"candidate_commits": {item["change_id"]: item["commit"] for item in doc["candidates"]},
                         "dependency_order": order, "conclusion": "frozen evidence passed; no merge or release performed",
                         "validation": report, "release_authorized": False})
        return {"status": "integration_ready", "manifest": manifest, "release_authorized": False}
    except (ValueError, KeyError, TypeError, AttributeError, OSError, subprocess.SubprocessError) as error:
        return blocked(error)


def make_demo_feature(root, descriptor, evidence_path):
    """Synthetic fixture factory, deliberately hard-coded to mock mode."""
    artifacts = [file_ref(root, descriptor["path"])]
    evidence = [file_ref(root, evidence_path)]
    doc = {"schema_version": 1, "kind": "feature", "mode": "mock", "run_id": "mock-" + descriptor["change_id"],
           "change_id": descriptor["change_id"], "repo": "mock-repo", "base_commit": "a" * 40,
           "head_commit": ("b" if descriptor["change_id"] == "alpha" else "c") * 40,
           "artifact_revision": 1, "scope": [descriptor["path"]],
           "ac": [{"id": "AC-001", "criterion": "Synthetic demonstration only"}],
           "dependencies": descriptor["dependencies"], "conflicts": [], "rollback": "Retain baseline; no operations",
           "retry_history": [], "nodes": {}}
    for name, parents in GRAPH.items():
        is_review = name in REVIEW_AUTHORS
        readonly = is_review or name == "targeted_test"
        node = {"status": "pass", "owner": "mock-reviewer-" + name if readonly else "mock-implementer",
                "next_owner": "mock-coordinator", "artifact_revision": 1,
                "artifacts": copy.deepcopy(artifacts), "evidence": copy.deepcopy(evidence),
                "inputs": {parent: {"artifact_revision": 1, "artifacts": copy.deepcopy(artifacts)} for parent in parents},
                "read_set": [descriptor["path"], evidence_path], "write_set": [] if readonly else [descriptor["path"]],
                "allowed_actions": ["read"] if readonly else ["read", "write_local"], "unresolved_issues": []}
        if is_review:
            node["review"] = {"status": "pass", "reviewer": node["owner"], "reviewed_revision": 1,
                              "scope": doc["scope"], "findings": [], "non_blocking_suggestions": []}
        if name == "targeted_test":
            node["test_report"] = {"revision": 1, "scope": doc["scope"], "gaps": [], "conclusion": "MOCK pass",
                                   "results": [{"id": "TC-001", "ac": ["AC-001"], "status": "pass", "evidence": evidence}]}
        doc["nodes"][name] = node
    binding = feature_digest(doc)
    for node in doc["nodes"].values():
        node["binding"] = binding
    return doc


def demo_documents(root):
    fixture = read_json(root / "examples/pipeline/fixture.json")
    require(fixture["fixture"] is True, "demo requires explicit fixture")
    features = [make_demo_feature(root, item, fixture["evidence"]) for item in fixture["features"]]
    candidates = []
    for feature in features:
        result = evaluate_feature(feature, root, feature["base_commit"], feature["head_commit"], allow_mock=True)
        require(result["status"] == "candidate", "broken demo fixture: " + str(result.get("reasons")))
        candidates.append(result["candidate"])
    release = {"schema_version": 1, "kind": "release", "mode": "mock", "run_id": "mock-window-1",
               "change_id": "mock-batch", "repo": "mock-repo", "base_commit": "a" * 40, "head_commit": "d" * 40,
               "artifact_revision": 1, "candidates": candidates, "integration_owner": "mock-integrator",
               "version_plan": {"from": "0.1.0", "to": "0.2.0", "level": "minor", "migration": "MOCK additive plan"},
               "validation_scope": ["contract-smoke"], "budget": {"max_attempts": 2, "max_minutes": 10},
               "usage": {"attempts": 1, "minutes": 0}, "rollback": "Keep main unchanged; no operations",
               "retry_history": []}
    frozen = release_digest(release)
    release["freeze_digest"] = frozen
    release["validation"] = {"status": "pass", "revision": 1, "head_commit": release["head_commit"],
                             "freeze_digest": frozen, "reviewer": "mock-independent-reviewer",
                             "scope": release["validation_scope"], "results": {"contract-smoke": "pass"},
                             "evidence": [file_ref(root, fixture["evidence"])]}
    return features, release


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="synthetic fixtures only; does not run development or release")
    demo.add_argument("kind", choices=("feature", "release"))
    demo.add_argument("--show-input", action="store_true", help="print the mock input schema, not a successful gate result")
    fingerprint = sub.add_parser("fingerprint", help="print a binding only; NOT a validation or approval")
    fingerprint.add_argument("kind", choices=("feature", "release"))
    fingerprint.add_argument("manifest", type=Path)
    for kind in ("feature", "release"):
        command = sub.add_parser(kind, help="read-only actual evidence gate")
        command.add_argument("manifest", type=Path)
        command.add_argument("--repo", type=Path, required=True)
        command.add_argument("--base", required=True, help="trusted full commit pin")
        command.add_argument("--head", required=True, help="trusted full commit pin")
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            root = Path(__file__).resolve().parents[1]
            features, release = demo_documents(root)
            doc = features[0] if args.kind == "feature" else release
            evaluator = evaluate_feature if args.kind == "feature" else evaluate_release
            result = doc if args.show_input else evaluator(doc, root, doc["base_commit"], doc["head_commit"], allow_mock=True)
            result = {"fixture": True, "notice": "MOCK ONLY; no code/model/test command/merge/release executed", "result": result}
            code = 0 if args.show_input or result["result"]["status"] in {"candidate", "integration_ready"} else 2
        elif args.command == "fingerprint":
            doc = read_json(args.manifest)
            value = feature_digest(doc) if args.kind == "feature" else release_digest(doc)
            result, code = {"fingerprint": value, "validated": False, "release_authorized": False}, 0
        else:
            doc = read_json(args.manifest)
            evaluator = evaluate_feature if args.command == "feature" else evaluate_release
            result = evaluator(doc, args.repo, args.base, args.head)
            code = 0 if result["status"] in {"candidate", "integration_ready"} else 2
    except (ValueError, KeyError, TypeError, AttributeError, OSError, subprocess.SubprocessError) as error:
        result, code = blocked(error), 2
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
