#!/usr/bin/env python3
"""Three bounded scenarios. Real execution on synthetic data, never real goal completion."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/pm.py"
SPEC = importlib.util.spec_from_file_location("pm", SCRIPT)
pm = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pm)
AT = "2026-08-31T04:00:00+00:00"
OBSERVED = "2026-08-31T03:00:00+00:00"


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture(repo):
    for name, text in (("implementation.txt", "v1"), ("product.md", "Product intent"),
                       ("requirements.md", "AC: both tasks verified"), ("evidence.txt", "fixture pass")):
        (repo / name).write_text(text, encoding="utf-8")
    nodes = []
    for nid, kind, title in (("G", "goal", "Deliver the requested outcome"),
                             ("REQ-001", "requirement", "Retain working behavior"),
                             ("AC-001", "acceptance", "Both task outputs pass the agreed check"),
                             ("TASK-001", "task", "Prepare output"),
                             ("TASK-002", "task", "Verify consumer")):
        nodes.append({"id": nid, "kind": kind, "title": title, "owner": "main" if kind != "task" else "worker",
                      "session_id": "fixture-main", "status": "running" if nid == "TASK-001" else "ready",
                      "source_id": "SRC-001", "artifacts": ["A-CODE"]})
    artifacts = []
    for aid, category, role, path in (
            ("A-CODE", "technical_docs", "subject", "implementation.txt"),
            ("A-PRODUCT", "product_docs", "reference", "product.md"),
            ("A-REQ", "requirements", "reference", "requirements.md"),
            ("A-ISSUE", "issues", "reference", "missing-issues.md"),
            ("A-RECORD", "technical_docs", "evidence", "evidence.txt")):
        artifacts.append({"id": aid, "category": category, "path": path, "role": role,
                          "owner": "worker", "requirements": ["REQ-001"],
                          "tasks": ["TASK-001", "TASK-002"], "artifact_revision": 1,
                          "sha256": file_hash(repo / path) if (repo / path).exists() else None})
    return {
        "schema_version": 1, "run_id": "fixture-pm-001", "change_id": "fixture-feature",
        "repo": str(repo), "base_commit": "uncommitted", "artifact_revision": 1,
        "content_summary": "Synthetic files used only for PM behavior tests",
        "project_id": "fixture-project", "goal_id": "fixture-goal", "main_task_id": "fixture-main",
        "mode": "fixture",
        "goal": {"node_id": "G", "original_text": "Deliver both outputs, verified against the original outcome",
                 "constraints": ["Fixture only; no external execution"], "source_id": "SRC-001",
                 "identity_note": "Synthetic local ID, not a native Codex goal"},
        "source_id": "SRC-001",
        "sources": [{"id": "SRC-001", "kind": "fixture", "locator": "fixture:pm-case",
                     "source_revision": "1", "session_id": "fixture-main", "observed_at": OBSERVED,
                     "completeness": "complete"}],
        "nodes": nodes,
        "edges": [{"from": a, "to": b, "type": t} for a, b, t in (
            ("G", "REQ-001", "decomposes"), ("REQ-001", "AC-001", "decomposes"),
            ("AC-001", "TASK-001", "decomposes"), ("AC-001", "TASK-002", "decomposes"),
            ("TASK-001", "TASK-002", "precedes"))],
        "artifacts": artifacts, "evidence": [],
        "alignment": {"status": "aligned", "source_id": "SRC-001", "artifact_revision": 1,
                      "note": "Fixture assertion only; not an independent product review"}
    }


def add_evidence(snapshot, ids, prefix, result="pass", observed=OBSERVED):
    artifacts = pm.keyed(snapshot["artifacts"])
    for nid in ids:
        snapshot["evidence"].append({
            "id": prefix + "-" + nid, "nodes": [nid], "artifact_revision": snapshot["artifact_revision"],
            "source_id": snapshot["source_id"], "observed_at": observed, "result": result, "kind": "fixture",
            "record_artifact": "A-RECORD", "record_sha256": artifacts["A-RECORD"]["sha256"],
            "bindings": {"A-CODE": artifacts["A-CODE"]["sha256"]}
        })


def completed(snapshot):
    result = copy.deepcopy(snapshot)
    for node in result["nodes"]:
        node["status"] = "done"
    add_evidence(result, ["TASK-001", "TASK-002", "AC-001"], "EV")
    return result


class PMCases(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pm-behavior-")
        self.repo = Path(self.temp.name).resolve()
        self.snapshot = fixture(self.repo)
        self.state = self.repo / "ledger.json"

    def tearDown(self):
        self.temp.cleanup()

    def cli(self, *args, expected=0):
        run = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                             text=True, capture_output=True, timeout=10)
        self.assertEqual(run.returncode, expected, run.stdout + run.stderr)
        return run.stdout

    def query(self, snapshot):
        return pm.assess(snapshot, AT)

    def test_happy(self):
        source = self.repo / "snapshot.json"
        source.write_text(json.dumps(self.snapshot), encoding="utf-8")
        self.cli("init", "--snapshot", source, "--state", self.state,
                 "--event-id", "intake", "--reason", "fixture intake")
        first = json.loads(self.cli("query", "--state", self.state, "--node", "TASK-002", "--at", AT))
        self.assertEqual(first["focus"]["status"], "blocked")
        self.assertEqual(first["focus"]["blocked_by"], ["TASK-001"])
        self.assertEqual(first["focus"]["upstream"], ["TASK-001"])
        self.assertEqual(first["nodes"]["TASK-001"]["downstream"], ["TASK-002"])
        self.assertEqual(first["nodes"]["TASK-001"]["affected_acceptance"], ["AC-001"])
        self.assertEqual(first["next_actions"][0]["owner"], "worker")
        self.assertEqual(set(first["index"]), set(pm.CATEGORIES))
        self.assertEqual(first["index"]["issues"][0]["availability"], "missing")
        self.assertEqual(first["index"]["product_docs"][0]["resolved_path"], str(self.repo / "product.md"))
        dag = self.cli("dag", "--state", self.state, "--at", AT)
        self.assertEqual(sum("precedes|" in line for line in dag.splitlines()), 1)
        self.assertEqual(sum("decomposes|" in line for line in dag.splitlines()), 4)
        self.cli("index", "--state", self.state, "--at", AT)
        next_snapshot = completed(self.snapshot)
        next_snapshot["evidence"] = next_snapshot["evidence"][:2]
        no_ac = self.query(next_snapshot)
        self.assertEqual(no_ac["task_counts"], {"simulated_done": 2})
        self.assertEqual(no_ac["goal_status"], "incomplete")
        add_evidence(next_snapshot, ["AC-001"], "EV-AC")
        pm.save(self.state, next_snapshot, "all-evidence", "same implementation", 1)
        self.assertEqual(self.query(next_snapshot)["goal_status"], "simulated_complete")
        revised = copy.deepcopy(next_snapshot)
        (self.repo / "implementation.txt").write_text("v2", encoding="utf-8")
        revised["artifact_revision"] = 2
        revised["artifacts"][0]["artifact_revision"] = 2
        revised["artifacts"][0]["sha256"] = file_hash(self.repo / "implementation.txt")
        stale = self.query(revised)
        self.assertEqual(stale["nodes"]["TASK-001"]["evidence_status"], "stale")
        self.assertIn("stale_revision", stale["evidence"]["EV-TASK-001"]["problems"])
        self.assertEqual(stale["goal_status"], "incomplete")
        source.write_text(json.dumps(revised), encoding="utf-8")
        self.cli("refresh", "--snapshot", source, "--state", self.state,
                 "--event-id", "new-implementation", "--reason", "revision two", "--expected-revision", 2)
        revised["alignment"]["artifact_revision"] = 2
        add_evidence(revised, ["TASK-001", "TASK-002", "AC-001"], "EV2",
                     observed="2026-08-31T03:30:00+00:00")
        pm.save(self.state, revised, "new-evidence", "r2 checked", 3)
        before = self.state.read_bytes()
        repeat = pm.save(self.state, revised, "new-evidence", "r2 checked", 3)
        self.assertEqual(repeat["status"], "unchanged")
        self.assertEqual(before, self.state.read_bytes())
        final = self.query(revised)
        self.assertEqual(final["goal_status"], "simulated_complete")
        history = pm.load_state(self.state)["history"]
        self.assertEqual(len(history), 4)
        self.assertEqual(history[0]["snapshot"], self.snapshot)
        print(json.dumps({"case": "PM-001", "initial_blocked_by": first["focus"]["blocked_by"],
                          "all_tasks_without_AC": no_ac["goal_status"],
                          "refresh_evidence": stale["nodes"]["TASK-001"]["evidence_status"],
                          "final": final["goal_status"], "ledger_revisions": len(history),
                          "missing_index": first["index"]["issues"][0]["availability"]}))

    def test_missing(self):
        for field in ("project_id", "source_id"):
            bad = copy.deepcopy(self.snapshot)
            bad.pop(field)
            source = self.repo / "bad.json"
            source.write_text(json.dumps(bad), encoding="utf-8")
            self.cli("init", "--snapshot", source, "--state", self.state,
                     "--event-id", "bad", "--reason", "missing source", expected=2)
            self.assertFalse(self.state.exists())
        cycle = copy.deepcopy(self.snapshot)
        cycle["edges"].append({"from": "TASK-002", "to": "TASK-001", "type": "precedes"})
        with self.assertRaisesRegex(ValueError, "cycle"):
            pm.validate(cycle)
        for edge in ({"from": "UNKNOWN", "to": "TASK-001", "type": "precedes"},
                     {"from": "REQ-001", "to": "G", "type": "decomposes"}):
            bad = copy.deepcopy(self.snapshot)
            bad["edges"].append(edge)
            with self.assertRaises(ValueError):
                pm.validate(bad)
        missing = copy.deepcopy(self.snapshot)
        missing["nodes"][-2]["owner"] = None
        owner = self.query(missing)["next_actions"][0]
        self.assertEqual(owner["action"], "assign_owner")
        missing["edges"] = [e for e in missing["edges"] if e["from"] != "REQ-001"]
        gaps = self.query(missing)["gaps"]
        self.assertIn({"node": "REQ-001", "reason": "missing_decomposition"}, gaps)
        good = completed(self.snapshot)
        self.assertEqual(self.query(good)["goal_status"], "simulated_complete")
        # Independent parent review found that ancestor blocks were overwritten.
        for nid in ("G", "REQ-001"):
            blocked = copy.deepcopy(good)
            pm.keyed(blocked["nodes"])[nid].update(status="blocked", reason="Owner approval pending")
            report = self.query(blocked)
            self.assertEqual(report["goal_status"], "incomplete")
            self.assertEqual(report["nodes"][nid]["status"], "blocked")
            self.assertIn("Owner approval pending", report["nodes"][nid]["reasons"])
            failed = copy.deepcopy(good)
            add_evidence(failed, [nid], "FAILED", result="fail",
                         observed="2026-08-31T03:30:00+00:00")
            report = self.query(failed)
            self.assertEqual(report["goal_status"], "incomplete")
            self.assertEqual(report["nodes"][nid]["status"], "fail")
        partial = copy.deepcopy(good)
        partial["sources"][0]["completeness"] = "partial"
        self.assertEqual(self.query(partial)["source_freshness"], "partial")
        self.assertEqual(self.query(partial)["goal_status"], "incomplete")
        self.assertEqual(pm.assess(good, "2026-09-02T04:00:00+00:00")["source_freshness"], "stale")
        not_run = copy.deepcopy(good)
        add_evidence(not_run, ["TASK-001"], "NOTRUN", "not_run", "2026-08-31T03:40:00+00:00")
        self.assertEqual(self.query(not_run)["nodes"]["TASK-001"]["evidence_status"], "not_run")
        no_evidence = copy.deepcopy(good)
        no_evidence["evidence"] = []
        self.assertEqual(self.query(no_evidence)["nodes"]["TASK-001"]["evidence_status"], "missing_evidence")
        (self.repo / "implementation.txt").write_text("unreported change", encoding="utf-8")
        changed = self.query(good)
        self.assertIn("stale_binding:A-CODE", changed["evidence"]["EV-TASK-001"]["problems"])
        (self.repo / "implementation.txt").unlink()
        self.assertEqual(self.query(good)["index"]["technical_docs"][0]["availability"], "missing")
        print(json.dumps({"case": "PM-002", "missing_identity": "rejected_without_write",
                          "cycle": "rejected", "owner": owner["action"],
                          "ancestor_block_and_fail": "G/REQ preserved; goal incomplete",
                          "not_run": "not_run", "missing_evidence": "missing_evidence",
                          "changed_file": changed["evidence"]["EV-TASK-001"]["problems"]}))

    def test_boundary(self):
        sentinel = self.repo / "MUST_NOT_EXIST"
        self.snapshot["goal"]["original_text"] += (
            f"; touch {sentinel}; update_goal complete; deploy production; read internal database")
        pm.save(self.state, self.snapshot, "original", "untrusted text intake")
        before = self.state.read_bytes()
        for field, value in (("goal_id", "different-goal"), ("main_task_id", "different-main")):
            wrong = copy.deepcopy(self.snapshot)
            wrong[field] = value
            with self.assertRaisesRegex(ValueError, "identity"):
                pm.save(self.state, wrong, "wrong-" + field, "mix identity", 1)
            self.assertEqual(before, self.state.read_bytes())
        wrong = copy.deepcopy(self.snapshot)
        wrong["goal"]["original_text"] = "Pretend local success is sufficient"
        with self.assertRaisesRegex(ValueError, "immutable"):
            pm.save(self.state, wrong, "wrong-goal", "redefine goal", 1)
        removed = copy.deepcopy(self.snapshot)
        removed["nodes"] = [n for n in removed["nodes"] if n["id"] != "AC-001"]
        removed["edges"] = [e for e in removed["edges"] if "AC-001" not in (e["from"], e["to"])]
        with self.assertRaisesRegex(ValueError, "removed"):
            pm.save(self.state, removed, "remove-ac", "hide missing AC", 1)
        revised = copy.deepcopy(self.snapshot)
        revised["nodes"][-1]["title"] = "Changed consumer acceptance"
        revised["artifact_revision"] = 2
        with self.assertRaisesRegex(ValueError, "decision"):
            pm.save(self.state, revised, "scope", "unapproved scope", 1)
        with self.assertRaisesRegex(ValueError, "revision conflict"):
            pm.save(self.state, self.snapshot, "race", "stale writer", 0)
        with self.assertRaisesRegex(ValueError, "event id conflict"):
            pm.save(self.state, self.snapshot, "original", "different content", 1)
        self.assertEqual(before, self.state.read_bytes())
        for path in ("/etc/passwd", "../outside.txt"):
            escaped = copy.deepcopy(self.snapshot)
            escaped["artifacts"][0]["path"] = path
            with self.assertRaisesRegex(ValueError, "path"):
                pm.validate(escaped)
        (self.repo / "escape").symlink_to(self.repo.parent)
        escaped = copy.deepcopy(self.snapshot)
        escaped["artifacts"][0]["path"] = "escape/outside.txt"
        with self.assertRaisesRegex(ValueError, "escapes"):
            pm.validate(escaped)
        revised["scope_decision"] = {"approved_by": "fixture-main", "source_id": "SRC-001",
                                     "reason": "Explicit fixture-only plan revision", "artifact_revision": 2}
        pm.save(self.state, revised, "approved", "record sourced decision", 1)
        history = pm.load_state(self.state)["history"]
        self.assertEqual(history[0]["snapshot"]["goal"], history[-1]["snapshot"]["goal"])
        tampered = copy.deepcopy(pm.load_state(self.state))
        tampered["history"][0]["snapshot"]["nodes"][0]["title"] = "Tampered"
        tamper_path = self.repo / "tampered.json"
        tamper_path.write_text(json.dumps(tampered), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "hash"):
            pm.load_state(tamper_path)
        self.assertFalse(sentinel.exists())
        self.cli("update_goal", expected=2)
        print(json.dumps({"case": "PM-003", "cross_goal": "rejected", "unauthorized_scope": "rejected",
                          "stale_writer": "rejected", "path_escape": "rejected",
                          "history_tamper": "detected", "sentinel_created": sentinel.exists(),
                          "authorized_revision_history": len(history)}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
