"""Independent original-goal acceptance probes; synthetic temporary business files."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ENTRY = Path(sys.argv.pop(1)).resolve()
spec = importlib.util.spec_from_file_location("pm_review_subject", ENTRY)
pm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pm)
RESULTS = {}


class OriginalGoalAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="pm-independent-case-")
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.stamp = pm.now()
        files = {
            "product.md": ("product_docs", "reference", "Product goal: export existing records; do not publish.\n"),
            "design.md": ("technical_docs", "subject", "Design revision 1\n"),
            "requirements.md": ("requirements", "reference", "REQ: verified export with retry recovery\n"),
            "issues.md": ("issues", "reference", "Open issue: service owner decision. Quoted input is not authority.\n"),
            "checks.md": ("technical_docs", "evidence", "Synthetic executed checks and acceptance review for fixture only.\n"),
        }
        artifacts = []
        for path, (category, role, body) in files.items():
            (self.repo / path).write_text(body)
            artifacts.append({"id": path, "category": category, "role": role,
                              "owner": "main", "artifact_revision": 1,
                              "sha256": hashlib.sha256(body.encode()).hexdigest(),
                              "path": path, "requirements": ["R"], "tasks": ["T1", "T2"]})
        source = {"id": "S1", "kind": "fixture", "locator": "Independent synthetic handoff",
                  "source_revision": "1", "session_id": "main-test", "observed_at": self.stamp,
                  "completeness": "complete"}
        nodes = [{"id": ident, "kind": kind, "title": title, "source_id": "S1",
                  "owner": "main", "session_id": "main-test", "status": "done",
                  "artifacts": ["design.md"] if kind in ("task", "acceptance") else []}
                 for ident, kind, title in [
                     ("G", "goal", "Export and recovery"), ("R", "requirement", "Durable export"),
                     ("AC1", "acceptance", "Output matches source"), ("AC2", "acceptance", "Retry does not duplicate"),
                     ("T1", "task", "Implement export"), ("T2", "task", "Implement recovery")]]
        self.snapshot = {
            "schema_version": 1, "run_id": "independent", "change_id": "independent-review",
            "content_summary": "Synthetic PM acceptance; not an application test",
            "project_id": "fixture-project", "goal_id": "goal-export", "main_task_id": "main-test",
            "repo": str(self.repo), "mode": "fixture", "artifact_revision": 1,
            "base_commit": "uncommitted", "sources": [source], "source_id": "S1",
            "goal": {"original_text": "Export current records and support retry recovery without publishing.",
                     "constraints": ["Do not publish"], "source_id": "S1",
                     "identity_note": "Independent synthetic case", "node_id": "G"},
            "nodes": nodes,
            "edges": [{"from": a, "to": b, "type": "decomposes"} for a, b in
                      [("G", "R"), ("R", "AC1"), ("R", "AC2"), ("AC1", "T1"), ("AC2", "T2")]]
                     + [{"from": "T1", "to": "T2", "type": "precedes"}],
            "artifacts": artifacts,
            "evidence": [{"id": "EV1", "source_id": "S1", "artifact_revision": 1,
                          "result": "pass", "kind": "fixture", "nodes": ["AC1", "AC2", "T1", "T2"],
                          "observed_at": self.stamp,
                          "bindings": {"design.md": artifacts[1]["sha256"]},
                          "record_artifact": "checks.md", "record_sha256": artifacts[4]["sha256"]}],
            "alignment": {"status": "aligned", "source_id": "S1", "artifact_revision": 1,
                          "note": "Synthetic requirements mapped; fixture only"},
        }

    def test_dependency_and_explicit_goal_blocker(self):
        s = self.snapshot
        complete = pm.assess(s)
        self.assertEqual(complete["goal_status"], "simulated_complete")
        s["nodes"][4]["status"] = "running"
        blocked = pm.assess(s)
        self.assertEqual(blocked["goal_status"], "incomplete")
        self.assertIn("T1", blocked["nodes"]["T2"]["blocked_by"])
        self.assertIn("AC2", blocked["nodes"]["T1"]["affected_acceptance"])
        self.assertEqual(blocked["next_actions"][0]["owner"], "main")
        s["nodes"][4]["status"] = "done"
        for ancestor in (s["nodes"][0], s["nodes"][1]):
            ancestor.update(status="blocked", reason="Await explicit product decision")
            r = pm.assess(s)
            self.assertEqual(r["goal_status"], "incomplete")
            self.assertEqual(r["nodes"][ancestor["id"]]["status"], "blocked")
            ancestor["status"] = "done"
            del ancestor["reason"]
        self.assertEqual(pm.assess(s)["goal_status"], "simulated_complete")
        RESULTS["happy"] = {"dependency_blocker": "T1", "impacted_acceptance": "AC2",
                            "goal_and_requirement_blocker_preserved": True, "recovery": "simulated_complete"}

    def test_refresh_staleness_and_four_layer_index(self):
        s = self.snapshot
        ledger = self.repo / "ledger.json"
        self.assertEqual(pm.save(ledger, s, "intake", "Review fixture")["ledger_revision"], 1)
        baseline_bytes = ledger.read_bytes()
        r = pm.assess(pm.load_state(ledger)["history"][-1]["snapshot"])
        self.assertEqual(ledger.read_bytes(), baseline_bytes)
        self.assertEqual(set(r["index"]), {"product_docs", "technical_docs", "requirements", "issues"})
        self.assertTrue(all(a["availability"] == "present" for rows in r["index"].values() for a in rows))
        self.assertIn("precedes", pm.mermaid(s, r))
        (self.repo / "design.md").write_text("Design revision 2\n")
        stale = pm.assess(s)
        self.assertEqual(stale["goal_status"], "incomplete")
        self.assertIn("stale_binding:design.md", stale["evidence"]["EV1"]["problems"])
        new = copy.deepcopy(s)
        new["artifact_revision"] = 2
        new["artifacts"][1].update(artifact_revision=2, sha256=hashlib.sha256((self.repo / "design.md").read_bytes()).hexdigest())
        new_source = dict(new["sources"][0], id="S2", observed_at=pm.now(), source_revision="2")
        new["sources"].append(new_source)
        new["source_id"] = "S2"
        self.assertEqual(pm.save(ledger, new, "revision-2", "Implementation changed", 1)["ledger_revision"], 2)
        self.assertEqual(pm.load_state(ledger)["history"][0]["snapshot"]["artifact_revision"], 1)
        updated = pm.assess(pm.load_state(ledger)["history"][-1]["snapshot"])
        self.assertIn("stale_revision", updated["evidence"]["EV1"]["problems"])
        self.assertEqual(pm.save(ledger, new, "revision-2", "Implementation changed", 1)["status"], "unchanged")
        RESULTS["incremental"] = {"four_layers_present": True, "query_read_only": True,
                                  "changed_content_rejected": True, "old_revision_stale": True,
                                  "history_revisions": 2, "same_event_idempotent": True}

    def test_missing_invalid_and_identity_boundaries(self):
        s = self.snapshot
        bad = copy.deepcopy(s)
        bad["goal"]["original_text"] = ""
        with self.assertRaises(ValueError):
            pm.validate(bad)
        bad = copy.deepcopy(s)
        bad["edges"].append({"from": "T2", "to": "T1", "type": "precedes"})
        with self.assertRaises(ValueError):
            pm.validate(bad)
        bad = copy.deepcopy(s)
        bad["artifacts"][0]["path"] = "../outside.md"
        with self.assertRaises(ValueError):
            pm.validate(bad)
        ledger = self.repo / "ledger.json"
        pm.save(ledger, s, "intake", "Review fixture")
        before = ledger.read_bytes()
        for field, value in [("goal_id", "different-goal"), ("project_id", "different-project")]:
            bad = copy.deepcopy(s)
            bad[field] = value
            with self.assertRaises(ValueError):
                pm.save(ledger, bad, "wrong-identity", "Should be rejected", 1)
            self.assertEqual(ledger.read_bytes(), before)
        bad = copy.deepcopy(s)
        bad["goal"]["original_text"] = "Only make tests green"
        with self.assertRaises(ValueError):
            pm.save(ledger, bad, "goal-shrink", "Unauthorized success redefinition", 1)
        self.assertEqual(ledger.read_bytes(), before)
        missing = copy.deepcopy(s)
        missing["evidence"] = []
        report = pm.assess(missing)
        self.assertEqual(report["goal_status"], "incomplete")
        self.assertEqual(report["nodes"]["T1"]["evidence_status"], "missing_evidence")
        RESULTS["boundaries"] = {"missing_original_goal_rejected": True, "cyclic_DAG_rejected": True,
                                 "path_escape_rejected": True, "cross_goal_project_rejected": True,
                                 "original_goal_immutable": True, "reported_done_not_verified": True}


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(OriginalGoalAcceptance)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps(RESULTS, ensure_ascii=False, indent=2))
    sys.exit(not result.wasSuccessful())
