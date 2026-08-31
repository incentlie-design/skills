#!/usr/bin/env python3
"""Replay the explicitly sourced parent-goal intake, using real local files, without completing it."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/pm.py"
SPEC = importlib.util.spec_from_file_location("pm", SCRIPT)
pm = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pm)


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(*args):
    result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                            text=True, capture_output=True, timeout=20)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    snapshot = pm.read_json(args.snapshot)
    pm.require(snapshot["mode"] == "real" and
               snapshot["main_task_id"] == "01a05360-3ad2-7211-a3b5-48d7fe3189df",
               "this rehearsal requires the explicitly delegated real parent snapshot")
    pm.validate(snapshot)
    args.output.mkdir(parents=True, exist_ok=False)
    at = pm.now()
    for artifact in snapshot["artifacts"]:
        if artifact["path"]:
            path = pm.local_path(Path(snapshot["repo"]), artifact["path"])
            if path.is_file():
                artifact["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    snapshot["sources"].append({
        "id": "SRC-LOCAL-INTAKE", "kind": "file", "locator": snapshot["repo"],
        "source_revision": pm.digest(snapshot["artifacts"]), "session_id": "delegated-session:PM-SKILL-001",
        "observed_at": at, "completeness": "complete",
        "note": "Actual local file observation only; does not refresh the parent task observation"
    })
    filled = args.output / "snapshot-intake.json"
    write(filled, snapshot)
    state = args.output / "ledger.json"
    intake = json.loads(run("init", "--snapshot", filled, "--state", state,
                            "--event-id", "real-intake-001", "--reason", "explicit parent handoff and local files"))
    before = json.loads(run("query", "--state", state, "--node", "TASK-008"))
    refreshed = copy.deepcopy(snapshot)
    refreshed["sources"].append({
        "id": "SRC-LOCAL-RECONCILE", "kind": "file", "locator": snapshot["repo"],
        "source_revision": "local-candidate-observed-1", "session_id": "delegated-session:PM-SKILL-001",
        "observed_at": pm.now(), "completeness": "partial",
        "note": "Local candidate files exist; parent goal body and full approval remain unavailable"
    })
    refreshed["source_id"] = "SRC-LOCAL-RECONCILE"
    for node in refreshed["nodes"]:
        if node["kind"] == "task" and node["id"] != "TASK-008":
            node["status"] = "review"
            node["source_id"] = "SRC-LOCAL-RECONCILE"
    refreshed_path = args.output / "snapshot-refresh.json"
    write(refreshed_path, refreshed)
    update = json.loads(run("refresh", "--snapshot", refreshed_path, "--state", state,
                            "--expected-revision", 1, "--event-id", "real-reconcile-002",
                            "--reason", "files prepared; independent acceptance pending"))
    report = json.loads(run("query", "--state", state, "--node", "TASK-008"))
    write(args.output / "query.json", report)
    (args.output / "dag.mmd").write_text(run("dag", "--state", state), encoding="utf-8")
    (args.output / "index.md").write_text(run("index", "--state", state), encoding="utf-8")
    assert before["goal_status"] == report["goal_status"] == "incomplete"
    assert report["source_freshness"] == "partial"
    assert report["focus"]["status"] == "blocked"
    assert len(report["focus"]["blocked_by"]) == 7
    assert report["evidence"] == {}
    assert "done" not in {n["reported_status"] for n in report["nodes"].values()}
    assert all(report["index"][category] for category in pm.CATEGORIES)
    assert any(a["id"] == "A-PARENT-REVIEW" and a["availability"] == "missing"
               for a in report["index"]["issues"])
    summary = {
        "mode": "real", "main_task_id": snapshot["main_task_id"], "goal_id_kind": "handoff-local-id",
        "native_goal_read_from_child": False, "intake_revision": intake["ledger_revision"],
        "refresh_revision": update["ledger_revision"], "artifact_revision": report["artifact_revision"],
        "goal_status": report["goal_status"], "source_freshness": report["source_freshness"],
        "task_counts": report["task_counts"], "acceptance_blocked_by": report["focus"]["blocked_by"],
        "acceptance_owner": report["focus"]["owner"], "all_four_index_layers": True,
        "fixture_evidence_used": False, "evidence_count": 0, "output": str(args.output.resolve())
    }
    write(args.output / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
