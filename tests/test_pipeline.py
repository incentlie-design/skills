"""Bounded behavioral tests. Synthetic attestations are NOT real business approvals."""

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location("pipeline", ROOT / "scripts/pipeline.py")
pipeline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pipeline)


def bind(doc):
    value = pipeline.feature_digest(doc)
    for node in doc["nodes"].values():
        node["binding"] = value
    return doc


def advance(doc):
    old = copy.deepcopy(doc)
    revised = copy.deepcopy(doc)
    revision = revised["artifact_revision"] + 1
    revised["artifact_revision"] = revision
    for node in revised["nodes"].values():
        node["artifact_revision"] = revision
        for source in node["inputs"].values():
            source["artifact_revision"] = revision
        if "review" in node:
            node["review"]["reviewed_revision"] = revision
        if "test_report" in node:
            node["test_report"]["revision"] = revision
    bind(revised)
    revised["retry_history"].append({
        "from_revision": old["artifact_revision"], "to_revision": revision,
        "from_snapshot": pipeline.feature_digest(old), "to_snapshot": pipeline.feature_digest(revised),
        "status": "revise", "failed_node": "code_review", "reason": "Targeted repair with preserved evidence",
        "owner": "test-owner", "evidence": old["nodes"]["code_review"]["evidence"],
    })
    return revised


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pipeline-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "examples/pipeline", self.root / "examples/pipeline")
        self.features, self.release = pipeline.demo_documents(self.root)
        self.feature = self.features[0]

    def feature_result(self, doc=None):
        doc = self.feature if doc is None else doc
        return pipeline.evaluate_feature(doc, self.root, doc["base_commit"], doc["head_commit"], allow_mock=True)

    def release_result(self, doc=None):
        doc = self.release if doc is None else doc
        return pipeline.evaluate_release(doc, self.root, doc["base_commit"], doc["head_commit"], allow_mock=True)

    def test_feature_success_requires_all_nodes_and_preserves_contract(self):
        result = self.feature_result()
        self.assertEqual(result["status"], "candidate")
        self.assertEqual([item["node"] for item in result["trace"]], list(pipeline.GRAPH))
        candidate = result["candidate"]
        self.assertEqual(candidate["commit"], self.feature["head_commit"])
        self.assertEqual(candidate["scope"], self.feature["scope"])
        self.assertEqual(candidate["source_digest"], pipeline.feature_digest(self.feature))
        self.assertFalse(candidate["release_authorized"])

    def test_missing_unknown_and_blocked_never_pass(self):
        for mutation in ("missing_node", "unknown_node", "missing_status", "unknown_status", "blocked", "missing_evidence"):
            with self.subTest(mutation=mutation):
                doc = copy.deepcopy(self.feature)
                if mutation == "missing_node":
                    del doc["nodes"]["test_plan_review"]
                elif mutation == "unknown_node":
                    doc["nodes"]["deploy"] = {}
                elif mutation == "missing_status":
                    del doc["nodes"]["spec"]["status"]
                elif mutation == "unknown_status":
                    doc["nodes"]["spec"]["status"] = "done"
                elif mutation == "blocked":
                    doc["nodes"]["spec"]["status"] = "blocked"
                else:
                    doc["nodes"]["spec"]["evidence"] = []
                bind(doc)
                result = self.feature_result(doc)
                self.assertEqual(result["status"], "blocked")
                self.assertNotIn("candidate", result)
                self.assertFalse(result["retry_allowed"])

    def test_review_cannot_be_signed_by_implementer_or_have_blocking_findings(self):
        for name in pipeline.REVIEW_AUTHORS:
            with self.subTest(node=name):
                doc = copy.deepcopy(self.feature)
                node = doc["nodes"][name]
                node["owner"] = doc["nodes"]["implementation"]["owner"]
                node["review"]["reviewer"] = node["owner"]
                self.assertEqual(self.feature_result(bind(doc))["status"], "blocked")
        doc = copy.deepcopy(self.feature)
        doc["nodes"]["code_review"]["review"]["findings"] = [{
            "id": "REV-001", "severity": "major", "evidence": "AC-001 behavior",
            "impact": "Fails acceptance", "minimal_fix": "Repair input check", "owner": "writer",
            "acceptance": "TC-001 passes",
        }]
        self.assertEqual(self.feature_result(bind(doc))["status"], "blocked")

    def test_stale_review_binding_upstream_and_bytes_are_rejected(self):
        for mutation in ("review", "binding", "input"):
            with self.subTest(mutation=mutation):
                doc = copy.deepcopy(self.feature)
                if mutation == "review":
                    doc["nodes"]["code_review"]["review"]["reviewed_revision"] = 0
                    bind(doc)
                elif mutation == "binding":
                    doc["rollback"] = "Changed rollback contract after approval"
                else:
                    doc["nodes"]["design"]["inputs"]["spec"]["artifact_revision"] = 0
                    bind(doc)
                self.assertEqual(self.feature_result(doc)["status"], "blocked")
        (self.root / self.feature["scope"][0]).write_text("changed after review", encoding="utf-8")
        result = self.feature_result()
        self.assertEqual(result["status"], "blocked")
        self.assertIn("stale content", result["reasons"][0])

    def test_test_report_needs_passing_results_and_complete_ac_coverage(self):
        for status in ("fail", "blocked", "not_run", "unknown"):
            with self.subTest(status=status):
                doc = copy.deepcopy(self.feature)
                doc["nodes"]["targeted_test"]["test_report"]["results"][0]["status"] = status
                self.assertEqual(self.feature_result(bind(doc))["status"], "blocked")
        doc = copy.deepcopy(self.feature)
        doc["ac"].append({"id": "AC-002", "criterion": "An additional untested behavior"})
        self.assertEqual(self.feature_result(bind(doc))["status"], "blocked")

    def test_conditional_retries_stop_after_two_and_reject_broken_history(self):
        doc = copy.deepcopy(self.feature)
        doc["nodes"]["code_review"]["status"] = "revise"
        doc["nodes"]["code_review"]["review"]["status"] = "revise"
        bind(doc)
        self.assertTrue(self.feature_result(doc)["retry_allowed"])
        doc = advance(doc)
        self.assertTrue(self.feature_result(doc)["retry_allowed"])
        invalid = copy.deepcopy(doc)
        invalid["retry_history"][0]["status"] = "blocked"
        self.assertEqual(self.feature_result(invalid)["status"], "blocked")
        invalid = copy.deepcopy(doc)
        invalid["retry_history"][0]["reason"] = ""
        self.assertEqual(self.feature_result(invalid)["status"], "blocked")
        doc = advance(doc)
        result = self.feature_result(doc)
        self.assertEqual(result["status"], "revise")
        self.assertFalse(result["retry_allowed"])
        self.assertEqual(self.feature_result(advance(doc))["status"], "blocked")
        # A repaired third snapshot may pass, but only with a history bound to it.
        doc["nodes"]["code_review"]["status"] = "pass"
        doc["nodes"]["code_review"]["review"]["status"] = "pass"
        bind(doc)
        self.assertEqual(self.feature_result(doc)["status"], "blocked")
        doc["retry_history"][-1]["to_snapshot"] = pipeline.feature_digest(doc)
        self.assertEqual(self.feature_result(doc)["status"], "candidate")

    def test_release_reuses_candidates_and_topologically_sorts(self):
        self.release["candidates"].reverse()
        self.release["freeze_digest"] = pipeline.release_digest(self.release)
        self.release["validation"]["freeze_digest"] = self.release["freeze_digest"]
        result = self.release_result()
        self.assertEqual(result["status"], "integration_ready")
        self.assertEqual(result["manifest"]["dependency_order"], ["alpha", "beta"])
        self.assertFalse(result["release_authorized"])

    def test_dependency_missing_and_cycle_are_rejected(self):
        missing = copy.deepcopy(self.release)
        missing["candidates"][1]["dependencies"] = ["absent"]
        self.assertIn("missing candidate dependency", self.release_result(missing)["reasons"][0])
        cyclic = copy.deepcopy(self.release)
        cyclic["candidates"][0]["dependencies"] = ["beta"]
        self.assertIn("cycle", self.release_result(cyclic)["reasons"][0])

    def test_same_file_and_explicit_conflicts_are_rejected(self):
        doc = copy.deepcopy(self.release)
        doc["candidates"][1]["scope"] = doc["candidates"][0]["scope"]
        self.assertIn("same-file conflict", self.release_result(doc)["reasons"][0])
        doc = copy.deepcopy(self.release)
        doc["candidates"][0]["conflicts"] = ["beta"]
        self.assertIn("declared candidate conflict", self.release_result(doc)["reasons"][0])

    def test_base_head_candidate_and_version_changes_invalidate_freeze(self):
        for mutation in ("base", "head", "candidate", "version", "scope"):
            with self.subTest(mutation=mutation):
                doc = copy.deepcopy(self.release)
                if mutation == "base":
                    doc["base_commit"] = "e" * 40
                elif mutation == "head":
                    doc["head_commit"] = "f" * 40
                elif mutation == "candidate":
                    doc["candidates"][0]["commit"] = "e" * 40
                elif mutation == "version":
                    doc["version_plan"]["to"] = "0.3.0"
                else:
                    doc["validation_scope"].append("another-contract-check")
                self.assertEqual(self.release_result(doc)["status"], "blocked")
        doc = copy.deepcopy(self.release)
        doc["version_plan"]["to"] = "0.3.0"
        doc["freeze_digest"] = pipeline.release_digest(doc)
        self.assertIn("stale integration evidence", self.release_result(doc)["reasons"][0])

    def test_candidate_status_is_not_trusted_and_actual_rejects_mock(self):
        doc = copy.deepcopy(self.release)
        source = doc["candidates"][0]["source"]
        source["nodes"]["code_review"]["review"]["reviewed_revision"] = 0
        bind(source)
        self.assertEqual(self.release_result(doc)["status"], "blocked")
        self.assertEqual(pipeline.evaluate_feature(self.feature, self.root, "a" * 40, "b" * 40)["status"], "blocked")
        self.assertEqual(pipeline.evaluate_release(self.release, self.root, "a" * 40, "d" * 40)["status"], "blocked")

    def test_integration_budget_and_partial_results_fail_closed(self):
        for field, value in (("attempts", 3), ("minutes", 11), ("minutes", -1)):
            with self.subTest(field=field, value=value):
                doc = copy.deepcopy(self.release)
                doc["usage"][field] = value
                self.assertEqual(self.release_result(doc)["status"], "blocked")
        for status in ("fail", "blocked", "not_run", "unknown"):
            doc = copy.deepcopy(self.release)
            doc["validation"]["results"]["contract-smoke"] = status
            self.assertEqual(self.release_result(doc)["status"], "blocked")
        self.release["budget"]["max_attempts"] = 1
        self.release["freeze_digest"] = pipeline.release_digest(self.release)
        self.release["validation"]["freeze_digest"] = self.release["freeze_digest"]
        self.release["validation"]["status"] = "revise"
        self.assertFalse(self.release_result()["retry_allowed"])

    def test_actual_git_and_content_checks_without_creating_a_repository(self):
        # Use this checkout's existing committed diff. Attestations below are test data,
        # not claims that the repository's changes received real business acceptance.
        head = pipeline.git_read(ROOT, "rev-parse", "HEAD").decode().strip()
        base = pipeline.git_read(ROOT, "rev-parse", "HEAD^").decode().strip()
        scope = pipeline.git_read(ROOT, "diff", "--no-ext-diff", "--no-textconv", "--name-only",
                                  "-z", base, head, "--").decode().strip("\0").split("\0")
        artifacts = [pipeline.file_ref(ROOT, path) for path in scope]
        evidence = [pipeline.file_ref(ROOT, "docs/contracts.md")]
        doc = copy.deepcopy(self.feature)
        doc.update(mode="actual", repo=ROOT.name, base_commit=base, head_commit=head, scope=scope)
        for name, parents in pipeline.GRAPH.items():
            node = doc["nodes"][name]
            readonly = name in pipeline.REVIEW_AUTHORS or name == "targeted_test"
            node.update(artifacts=artifacts, evidence=evidence, read_set=list(dict.fromkeys(scope + ["docs/contracts.md"])),
                        write_set=[] if readonly else scope,
                        inputs={parent: {"artifact_revision": 1, "artifacts": artifacts} for parent in parents})
            if "review" in node:
                node["review"]["scope"] = scope
            if "test_report" in node:
                node["test_report"].update(scope=scope, conclusion="Synthetic unit-test attestation")
                node["test_report"]["results"][0]["evidence"] = evidence
        bind(doc)
        self.assertEqual(pipeline.evaluate_feature(doc, ROOT, base, head)["status"], "candidate")
        self.assertEqual(pipeline.evaluate_feature(doc, ROOT, base, "0" * 40)["status"], "blocked")
        invalid = copy.deepcopy(doc)
        invalid["head_commit"] = "0" * 40
        self.assertEqual(pipeline.evaluate_feature(bind(invalid), ROOT, base, "0" * 40)["status"], "blocked")

    def test_cli_exit_codes_no_shell_execution_and_no_release_side_effects(self):
        marker = self.root / "should-not-exist"
        self.feature["command"] = "touch " + str(marker)
        bind(self.feature)
        before = {str(path): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        refs_before = pipeline.git_read(ROOT, "show-ref")
        self.assertEqual(self.feature_result()["status"], "candidate")
        self.assertEqual(self.release_result()["status"], "integration_ready")
        self.assertFalse(marker.exists())
        for kind in ("feature", "release"):
            run = subprocess.run([sys.executable, str(ROOT / "scripts/pipeline.py"), "demo", kind],
                                 capture_output=True, text=True, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue(json.loads(run.stdout)["fixture"])
        manifest = self.root / "input.json"
        manifest.write_text(json.dumps(self.feature), encoding="utf-8")
        run = subprocess.run([sys.executable, str(ROOT / "scripts/pipeline.py"), "feature", str(manifest),
                              "--repo", str(self.root), "--base", "a" * 40, "--head", "b" * 40],
                             capture_output=True, text=True, timeout=10)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stdout)["status"], "blocked")
        manifest.write_text('{"schema_version": 1, "schema_version": 2}', encoding="utf-8")
        duplicate = subprocess.run([sys.executable, str(ROOT / "scripts/pipeline.py"), "fingerprint", "feature", str(manifest)],
                                   capture_output=True, text=True, timeout=10)
        self.assertEqual(duplicate.returncode, 2)
        for path, content in before.items():
            self.assertEqual(Path(path).read_bytes(), content)
        self.assertFalse(marker.exists())
        self.assertEqual(pipeline.git_read(ROOT, "show-ref"), refs_before)


if __name__ == "__main__":
    unittest.main()
