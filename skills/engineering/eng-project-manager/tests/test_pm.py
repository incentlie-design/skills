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


def managed_fixture(repo):
    snapshot = fixture(repo)
    nodes = pm.keyed(snapshot["nodes"])
    for nid, output, objective in (
            ("TASK-001", "A-CODE", "Produce the validator for accepted and rejected inputs"),
            ("TASK-002", "A-RECORD", "Produce a consumer verification record")):
        node = nodes[nid]
        node["artifacts"] = sorted(set(node["artifacts"] + [output]))
        node["work_package"] = {
            "objective": objective, "done_when": "Both agreed input classes have recorded results",
            "input_artifacts": ["A-PRODUCT"], "output_artifacts": [output],
            "write_scope": ["implementation.txt" if nid == "TASK-001" else "evidence.txt"],
            "stop_conditions": ["Stop on budget exhaustion or changed acceptance scope"]}
    # A shared task covers two acceptance branches; resource totals must not duplicate it.
    for original, new_id, title in (("REQ-001", "REQ-002", "Handle rejected input"),
                                    ("AC-001", "AC-002", "Rejected input leaves state unchanged")):
        node = copy.deepcopy(nodes[original])
        node.update(id=new_id, title=title)
        snapshot["nodes"].append(node)
    snapshot["edges"] += [{"from": a, "to": b, "type": "decomposes"} for a, b in
                          (("G", "REQ-002"), ("REQ-002", "AC-002"),
                           ("AC-002", "TASK-001"), ("AC-002", "TASK-002"))]
    assignments = []
    for aid, tid, agent, session, role, output, limit in (
            ("ASN-001", "TASK-001", "agent-api", "session-api", "implementation", "A-CODE", 600),
            ("ASN-002", "TASK-002", "agent-review", "session-review", "review", "A-RECORD", 400)):
        assignments.append({
            "id": aid, "task_id": tid, "agent_id": agent, "session_id": session,
            "role": role, "status": "running" if aid == "ASN-001" else "assigned",
            "source_id": "SRC-001", "assigned_at": OBSERVED, "expected_artifacts": [output],
            "budget_limits": {"tokens": limit, "minutes": 10}})
    usage = []
    for uid, aid, metric, amount, observed in (
            ("U1", "ASN-001", "tokens", 100, "2026-08-31T03:10:00+00:00"),
            ("U2", "ASN-001", "tokens", 160, "2026-08-31T03:20:00+00:00"),
            ("U3", "ASN-002", "tokens", 40, "2026-08-31T03:20:00+00:00"),
            ("U4", "ASN-001", "minutes", 2, "2026-08-31T03:20:00+00:00"),
            ("U5", "ASN-002", "minutes", 1, "2026-08-31T03:20:00+00:00")):
        usage.append({"id": uid, "assignment_id": aid, "metric": metric, "amount": amount,
                      "kind": "observed", "source_id": "SRC-001", "observed_at": observed})
    snapshot["management"] = {
        "schema_version": 1, "goal_budget": {"limits": {"tokens": 1000, "minutes": 20}, "source_id": "SRC-001"},
        "assignments": assignments, "usage": usage,
        "deliveries": [{"id": "DEL-001", "assignment_id": "ASN-001", "artifact_id": "A-CODE",
                        "artifact_revision": 1, "sha256": file_hash(repo / "implementation.txt"),
                        "source_id": "SRC-001", "observed_at": "2026-08-31T03:20:00+00:00"}]}
    return snapshot


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

    def managed(self):
        path = self.repo / "managed"
        path.mkdir()
        return managed_fixture(path)

    def check_management_happy(self):
        snapshot = self.managed()
        report = self.query(snapshot)
        budget = report["management"]["goal_budget"]["tokens"]
        self.assertEqual(budget["current_used"], 200)  # 160 + 40, not 100 + 160 + 40
        self.assertEqual(budget["remaining_to_goal_limit"], 800)
        package = report["goal_dag"]["work_packages"][0]
        self.assertEqual({a["id"] for a in package["acceptance"]}, {"AC-001", "AC-002"})
        self.assertEqual(package["objective_basis"], "work_package")
        self.assertEqual(package["output_artifacts"], ["A-CODE"])
        self.assertEqual(package["current_assignment_ids"], ["ASN-001"])
        self.assertEqual(report["management"]["assignments"][0]["assets"][0]["delivery_status"], "current")
        state = Path(snapshot["repo"]) / "ledger.json"
        source = state.with_name("snapshot.json")
        source.write_text(json.dumps(snapshot), encoding="utf-8")
        self.cli("init", "--snapshot", source, "--state", state,
                 "--event-id", "managed-intake", "--reason", "fixture assignment intake")
        before = state.read_bytes()
        focused = json.loads(self.cli("query", "--state", state, "--agent", "agent-api",
                                     "--session", "session-api", "--at", AT))["assignment_focus"]
        self.assertEqual(focused["task_ids"], ["TASK-001"])
        self.assertEqual(focused["budget"]["tokens"]["current_used"], 160)
        self.cli("brief", "--state", state, "--at", AT)
        self.cli("dag", "--state", state, "--at", AT)
        self.assertEqual(before, state.read_bytes())
        moved = copy.deepcopy(snapshot)
        moved["sources"].append({**snapshot["sources"][0], "id": "SRC-TRANSFER",
                                 "source_revision": "transfer-1", "observed_at": "2026-08-31T03:30:00+00:00"})
        moved["source_id"] = "SRC-TRANSFER"
        management = moved["management"]
        management["decision"] = {"approved_by": "fixture-main", "source_id": "SRC-TRANSFER",
                                   "reason": "Transfer remaining implementation scope to agent-next"}
        management["assignments"][0].update(status="released", reason="Handed over", source_id="SRC-TRANSFER")
        management["assignments"].append({
            **snapshot["management"]["assignments"][0], "id": "ASN-003", "agent_id": "agent-next",
            "session_id": "session-next", "status": "assigned", "source_id": "SRC-TRANSFER",
            "assigned_at": "2026-08-31T03:30:00+00:00", "budget_limits": {"tokens": 440, "minutes": 8}})
        for metric in ("tokens", "minutes"):
            management["usage"].append({"id": "ZERO-" + metric, "assignment_id": "ASN-003",
                                        "metric": metric, "amount": 0, "kind": "observed",
                                        "source_id": "SRC-TRANSFER", "observed_at": "2026-08-31T03:30:00+00:00"})
        source.write_text(json.dumps(moved), encoding="utf-8")
        self.cli("refresh", "--snapshot", source, "--state", state, "--expected-revision", 1,
                 "--event-id", "transfer", "--reason", "sourced reassignment")
        final = self.query(moved)
        rows = pm.keyed(final["management"]["assignments"])
        self.assertEqual(rows["ASN-001"]["budget"]["tokens"]["current_used"], 160)
        self.assertEqual(rows["ASN-003"]["budget"]["tokens"]["current_used"], 0)
        self.assertEqual(rows["ASN-001"]["assets"][0]["delivery_status"], "current")
        self.assertEqual(rows["ASN-003"]["assets"][0]["delivery_status"], "unreported")
        self.assertEqual(final["management"]["goal_budget"]["tokens"]["current_used"], 200)
        self.assertEqual(final["management"]["goal_budget"]["tokens"]["unallocated"], 0)
        self.assertEqual(final["goal_dag"]["work_packages"][0]["current_assignment_ids"], ["ASN-003"])
        history = pm.load_state(state)["history"]
        self.assertEqual(history[0]["snapshot"]["management"]["assignments"][0]["status"], "running")
        self.assertEqual(history[-1]["snapshot"]["artifact_revision"], 1)
        print(json.dumps({"case": "PM-001-management", "goal_used_tokens": 200, "goal_remaining_tokens": 800,
                          "agent_api_used": 160, "agent_next_used": 0, "shared_AC_no_double_count": True,
                          "old_asset_owner": "ASN-001", "current_assignment": "ASN-003"}))

    def check_management_missing(self):
        legacy = self.query(self.snapshot)
        self.assertEqual(legacy["management"]["recording_status"], "not_recorded")
        snapshot = self.managed()
        unknown = copy.deepcopy(snapshot)
        unknown["management"]["usage"] = []
        unknown["management"]["assignments"][0].update(agent_id=None, session_id=None)
        report = self.query(unknown)
        first = report["management"]["assignments"][0]
        self.assertIsNone(first["budget"]["tokens"]["current_used"])
        self.assertIsNone(first["budget"]["tokens"]["remaining"])
        self.assertIsNone(report["management"]["goal_budget"]["tokens"]["current_used"])
        self.assertIn("assignee_identity_incomplete", report["management"]["alerts"][0]["reasons"])
        unknown["management"]["usage"].append({
            "id": "EST", "assignment_id": "ASN-001", "metric": "tokens", "amount": 580,
            "kind": "estimated", "source_id": "SRC-001", "observed_at": "2026-08-31T03:20:00+00:00"})
        estimate = self.query(unknown)["management"]["assignments"][0]["budget"]["tokens"]
        self.assertEqual(estimate["estimated_used"], 580)
        self.assertEqual(estimate["status"], "estimated_only")
        self.assertIsNone(estimate["current_used"])
        spent = copy.deepcopy(snapshot)
        spent["management"]["usage"].append({
            "id": "OVER", "assignment_id": "ASN-001", "metric": "tokens", "amount": 601,
            "kind": "observed", "source_id": "SRC-001", "observed_at": "2026-08-31T03:30:00+00:00"})
        over = self.query(spent)
        self.assertEqual(over["management"]["assignments"][0]["budget"]["tokens"]["remaining"], -1)
        self.assertEqual(over["management"]["assignments"][0]["budget"]["tokens"]["status"], "over_budget")
        self.assertEqual(over["nodes"]["TASK-001"]["reported_status"], "running")
        allocated = copy.deepcopy(snapshot)
        allocated["management"]["goal_budget"]["limits"]["tokens"] = 900
        self.assertEqual(self.query(allocated)["management"]["goal_budget"]["tokens"]["status"], "overallocated")
        stale = pm.assess(snapshot, "2026-09-02T04:00:00+00:00")
        self.assertIsNone(stale["management"]["assignments"][0]["budget"]["tokens"]["remaining"])
        self.assertEqual(stale["management"]["assignments"][0]["budget"]["tokens"]["usage_freshness"], "stale")
        (Path(snapshot["repo"]) / "implementation.txt").unlink()
        asset = self.query(snapshot)["management"]["assignments"][0]["assets"][0]
        self.assertEqual(asset["availability"], "missing")
        self.assertEqual(asset["delivery_status"], "stale_or_unverified")
        print(json.dumps({"case": "PM-002-management", "unknown_remaining": None,
                          "estimate_not_charged": estimate["current_used"],
                          "assignment_overrun": 1, "stale_remaining": None, "missing_asset": asset["availability"]}))

    def check_management_boundary(self):
        snapshot = self.managed()
        state = Path(snapshot["repo"]) / "ledger.json"
        pm.save(state, snapshot, "original", "fixture")
        before = state.read_bytes()
        for limit in (-1, True, float("nan")):
            wrong = copy.deepcopy(snapshot)
            wrong["management"]["assignments"][0]["budget_limits"]["tokens"] = limit
            with self.assertRaisesRegex(ValueError, "budget"):
                pm.save(state, wrong, "bad", "invalid budget", 1)
        wrong = copy.deepcopy(snapshot)
        wrong["management"]["assignments"][0]["task_id"] = "OTHER-GOAL-TASK"
        with self.assertRaisesRegex(ValueError, "outside goal"):
            pm.save(state, wrong, "outside", "foreign task", 1)
        wrong = copy.deepcopy(snapshot)
        wrong["management"]["assignments"].append({**wrong["management"]["assignments"][0], "id": "DUP"})
        with self.assertRaisesRegex(ValueError, "multiple active"):
            pm.save(state, wrong, "double", "parallel writers", 1)
        wrong = copy.deepcopy(snapshot)
        wrong["management"]["assignments"][0]["agent_id"] = "different-agent"
        with self.assertRaisesRegex(ValueError, "identity immutable"):
            pm.save(state, wrong, "overwrite", "erase assignee", 1)
        wrong = copy.deepcopy(snapshot)
        wrong["management"]["goal_budget"]["limits"]["tokens"] = 2000
        with self.assertRaisesRegex(ValueError, "management decision"):
            pm.save(state, wrong, "budget", "unapproved budget", 1)
        wrong = copy.deepcopy(snapshot)
        wrong["management"]["usage"][0]["amount"] = 90
        with self.assertRaisesRegex(ValueError, "immutable"):
            pm.save(state, wrong, "usage", "rewrite usage", 1)
        wrong = copy.deepcopy(snapshot)
        wrong["management"]["usage"].append({
            **wrong["management"]["usage"][1], "id": "LOWER", "amount": 90,
            "observed_at": "2026-08-31T03:40:00+00:00"})
        with self.assertRaisesRegex(ValueError, "regressed"):
            pm.save(state, wrong, "lower", "reset cumulative counter", 1)
        wrong = copy.deepcopy(snapshot)
        pm.keyed(wrong["nodes"])["TASK-001"]["work_package"]["done_when"] = "Only happy path matters"
        with self.assertRaisesRegex(ValueError, "revision bump"):
            pm.save(state, wrong, "goal", "weaken work objective", 1)
        self.assertEqual(before, state.read_bytes())
        print(json.dumps({"case": "PM-003-management", "invalid_budget": "rejected",
                          "double_assignment": "rejected", "identity_overwrite": "rejected",
                          "budget_without_decision": "rejected", "usage_rewrite_or_reset": "rejected",
                          "work_objective_change_without_revision": "rejected", "ledger_unchanged": True}))

    def test_happy(self):
        self.check_management_happy()
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
        self.check_management_missing()
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
        self.check_management_boundary()
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
