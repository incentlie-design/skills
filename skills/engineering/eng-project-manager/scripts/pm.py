#!/usr/bin/env python3
"""Local PM ledger: no shell, network, native goal mutation or task dispatch."""
import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
from datetime import datetime, timezone
from collections import Counter

CONTRACT = "eng-project-manager/v1"
CATEGORIES = ("product_docs", "technical_docs", "requirements", "issues")
KINDS = ("goal", "requirement", "acceptance", "task")
STATES = ("draft", "ready", "running", "review", "done", "blocked", "cancelled")
IDENTITY = ("project_id", "goal_id", "main_task_id", "repo", "mode")
METRICS = ("tokens", "minutes", "commands", "cost_usd")
ACTIVE_ASSIGNMENTS = ("assigned", "running")
ASSIGNMENT_STATES = ("proposed", "assigned", "running", "completed", "released", "cancelled")


def require(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "timestamp requires timezone")
    return parsed


def now():
    return datetime.now(timezone.utc).isoformat()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def positive(value):
    return type(value) is int and value > 0


def sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def keyed(items):
    require(isinstance(items, list), "expected array")
    result = {}
    for item in items:
        require(isinstance(item, dict) and nonempty(item.get("id")), "item requires id")
        require(item["id"] not in result, "duplicate id: " + item["id"])
        result[item["id"]] = item
    return result


def local_path(repo, value):
    require(nonempty(value), "path required")
    relative = Path(value)
    require(not relative.is_absolute() and ".." not in relative.parts, "unsafe path")
    resolved = (repo / relative).resolve()
    require(resolved.is_relative_to(repo.resolve()), "path escapes repo (including symlink)")
    return resolved


def graph(snapshot, edge_type, reverse=False):
    result = {n["id"]: [] for n in snapshot["nodes"]}
    for edge in snapshot["edges"]:
        if edge_type is None or edge["type"] == edge_type:
            start, end = edge["from"], edge["to"]
            if reverse:
                start, end = end, start
            result[start].append(end)
    return result


def reachable(adjacency, start):
    found, pending = set(), list(adjacency[start])
    while pending:
        node = pending.pop()
        if node not in found:
            found.add(node)
            pending.extend(adjacency[node])
    return sorted(found)


def topological(adjacency):
    degrees = {node: 0 for node in adjacency}
    for children in adjacency.values():
        for child in children:
            degrees[child] += 1
    ready = sorted(n for n, degree in degrees.items() if degree == 0)
    order = []
    while ready:
        node = ready.pop(0)
        order.append(node)
        for child in adjacency[node]:
            degrees[child] -= 1
            if degrees[child] == 0:
                ready.append(child)
    require(len(order) == len(adjacency), "DAG cycle")
    return order


def completion_graph(snapshot):
    result = {n["id"]: [] for n in snapshot["nodes"]}
    for edge in snapshot["edges"]:
        a, b = edge["from"], edge["to"]
        if edge["type"] == "decomposes":
            a, b = b, a
        result[a].append(b)
    return result


def validate(snapshot):
    require(snapshot["schema_version"] == 1, "unsupported snapshot schema")
    for field in ("run_id", "change_id", "content_summary", *IDENTITY):
        require(nonempty(snapshot.get(field)), "missing identity/envelope: " + field)
    require(snapshot["mode"] in ("real", "fixture"), "invalid mode")
    repo = Path(snapshot["repo"])
    require(repo.is_absolute() and repo.is_dir(), "repo must be an existing absolute directory")
    require(positive(snapshot["artifact_revision"]), "artifact_revision must be positive integer")
    require(snapshot["base_commit"] == "uncommitted" or
            re.fullmatch(r"[0-9a-f]{40}", snapshot["base_commit"]), "invalid base_commit")
    sources = keyed(snapshot["sources"])
    require(snapshot["source_id"] in sources, "missing primary source")
    for source in sources.values():
        require(source["kind"] in ("goal_tool", "task_tool", "handoff", "file", "fixture"),
                "unknown source kind")
        for field in ("locator", "source_revision", "session_id"):
            require(nonempty(source[field]), "source missing " + field)
        timestamp(source["observed_at"])
        require(source["completeness"] in ("complete", "partial"), "invalid completeness")
    goal = snapshot["goal"]
    require(nonempty(goal["original_text"]) and isinstance(goal["constraints"], list)
            and all(nonempty(c) for c in goal["constraints"]), "original goal/constraints required")
    require(goal["source_id"] in sources and nonempty(goal["identity_note"]), "goal source required")
    nodes, artifacts = keyed(snapshot["nodes"]), keyed(snapshot["artifacts"])
    require(goal["node_id"] in nodes and nodes[goal["node_id"]]["kind"] == "goal", "missing goal root")
    require(sum(n["kind"] == "goal" for n in nodes.values()) == 1, "exactly one goal root required")
    for node in nodes.values():
        require(node["kind"] in KINDS and node["status"] in STATES, "invalid node kind/state")
        require(nonempty(node["title"]) and node["source_id"] in sources, "node title/source required")
        require(node["owner"] is None or nonempty(node["owner"]), "invalid owner")
        require(node["session_id"] is None or nonempty(node["session_id"]), "invalid session")
        require(isinstance(node["artifacts"], list) and set(node["artifacts"]) <= artifacts.keys(),
                "unknown required artifact")
        if node["status"] in ("blocked", "cancelled"):
            require(nonempty(node.get("reason")), "blocked/cancelled node requires reason")
    seen = set()
    for edge in snapshot["edges"]:
        a, b, kind = edge["from"], edge["to"], edge["type"]
        require(a in nodes and b in nodes and a != b, "dangling/self edge")
        require((a, b, kind) not in seen, "duplicate edge")
        seen.add((a, b, kind))
        pair = (nodes[a]["kind"], nodes[b]["kind"])
        require((kind == "decomposes" and pair in (
            ("goal", "requirement"), ("requirement", "acceptance"),
            ("acceptance", "task"), ("task", "task"))) or
            (kind == "precedes" and pair == ("task", "task")), "invalid edge direction/type")
    topological(graph(snapshot, None))
    topological(completion_graph(snapshot))
    for artifact in artifacts.values():
        require(artifact["category"] in CATEGORIES, "invalid artifact category")
        require(artifact["role"] in ("subject", "evidence", "reference"), "invalid artifact role")
        require(artifact["owner"] is None or nonempty(artifact["owner"]), "invalid artifact owner")
        require(positive(artifact["artifact_revision"]), "invalid artifact revision")
        require(artifact["sha256"] is None or sha(artifact["sha256"]), "invalid artifact hash")
        if artifact["path"] is not None:
            local_path(repo, artifact["path"])
        for field, kind in (("requirements", "requirement"), ("tasks", "task")):
            require(isinstance(artifact[field], list) and
                    all(n in nodes and nodes[n]["kind"] == kind for n in artifact[field]),
                    "invalid artifact " + field)
    for evidence in keyed(snapshot["evidence"]).values():
        require(evidence["source_id"] in sources, "unknown evidence source")
        require(positive(evidence["artifact_revision"]), "invalid evidence revision")
        require(evidence["result"] in ("pass", "fail", "blocked", "not_run"), "invalid result")
        require(evidence["kind"] in ("execution", "review", "fixture"), "invalid evidence kind")
        require(evidence["nodes"] and set(evidence["nodes"]) <= nodes.keys(), "invalid evidence nodes")
        timestamp(evidence["observed_at"])
        require(isinstance(evidence["bindings"], dict) and
                set(evidence["bindings"]) <= artifacts.keys() and
                all(sha(v) for v in evidence["bindings"].values()), "invalid evidence bindings")
        if evidence["record_artifact"] is not None:
            require(evidence["record_artifact"] in artifacts and
                    artifacts[evidence["record_artifact"]]["role"] == "evidence" and
                    sha(evidence["record_sha256"]), "invalid evidence record")
    alignment = snapshot.get("alignment")
    if alignment:
        require(alignment["status"] in ("aligned", "drift", "unreviewed") and
                alignment["source_id"] in sources and positive(alignment["artifact_revision"])
                and nonempty(alignment["note"]), "invalid alignment")
    validate_management(snapshot)
    return snapshot


def plan_content(snapshot):
    return {"nodes": [{k: n[k] for k in ("id", "kind", "title", "artifacts")}
                      | {"work_package": n.get("work_package")}
                      for n in snapshot["nodes"]], "edges": snapshot["edges"]}


def implementation_content(snapshot):
    return {"plan": plan_content(snapshot), "base_commit": snapshot["base_commit"],
            "subjects": [a for a in snapshot["artifacts"] if a["role"] == "subject"]}


def transition(old, new):
    require(all(old[k] == new[k] for k in IDENTITY), "identity mismatch")
    require(old["goal"] == new["goal"], "original goal is immutable; preserve baseline")
    require(new["artifact_revision"] >= old["artifact_revision"], "artifact revision regressed")
    for field in ("nodes", "artifacts", "sources", "evidence"):
        before, after = keyed(old[field]), keyed(new[field])
        require(before.keys() <= after.keys(), "history items cannot be removed: " + field)
        for key in before:
            if field in ("sources", "evidence"):
                require(before[key] == after[key], "source/evidence id is immutable: " + key)
            if field == "nodes":
                require(before[key]["kind"] == after[key]["kind"], "node kind is immutable")
    before_source = keyed(old["sources"])[old["source_id"]]
    after_source = keyed(new["sources"])[new["source_id"]]
    require(timestamp(after_source["observed_at"]) >= timestamp(before_source["observed_at"]),
            "source observation regressed")
    if implementation_content(old) != implementation_content(new):
        require(new["artifact_revision"] > old["artifact_revision"],
                "implementation/scope changed without artifact_revision bump")
    cancelled = {n["id"] for n in new["nodes"] if n["status"] == "cancelled"} - {
        n["id"] for n in old["nodes"] if n["status"] == "cancelled"}
    if plan_content(old) != plan_content(new) or cancelled:
        decision = new.get("scope_decision", {})
        require(nonempty(decision.get("approved_by")) and nonempty(decision.get("reason"))
                and decision.get("source_id") in keyed(new["sources"])
                and decision.get("artifact_revision") == new["artifact_revision"]
                and new["artifact_revision"] > old["artifact_revision"],
                "scope change requires explicit sourced decision and new revision")
    transition_management(old, new)


def number(value, metric):
    return (type(value) in (int, float) and math.isfinite(value) and value >= 0 and
            (metric not in ("tokens", "commands") or type(value) is int))


def limits_valid(limits):
    require(isinstance(limits, dict) and limits.keys() <= set(METRICS), "invalid budget metrics")
    require(all(v is None or number(v, k) for k, v in limits.items()), "invalid budget limit")


def validate_management(snapshot):
    nodes, artifacts, sources = (keyed(snapshot[k]) for k in ("nodes", "artifacts", "sources"))
    children = graph(snapshot, "decomposes")
    for node in nodes.values():
        package = node.get("work_package")
        if package is None:
            continue
        require(node["kind"] == "task", "work_package belongs to task")
        for field in ("objective", "done_when"):
            require(nonempty(package[field]), "work_package requires " + field)
        for field in ("input_artifacts", "output_artifacts"):
            require(isinstance(package[field], list) and
                    set(package[field]) <= artifacts.keys(), "invalid work_package artifacts")
        require(package["output_artifacts"] and
                set(package["output_artifacts"]) <= set(node["artifacts"]),
                "work_package outputs must be bound by task evidence")
        require(isinstance(package["stop_conditions"], list) and package["stop_conditions"]
                and all(nonempty(s) for s in package["stop_conditions"]),
                "work_package stop conditions required")
        require(isinstance(package["write_scope"], list), "write_scope must be array")
        for path in package["write_scope"]:
            local_path(Path(snapshot["repo"]), path)
    management = snapshot.get("management")
    if management is None:
        return
    require(management["schema_version"] == 1, "invalid management schema")
    assignments = keyed(management["assignments"])
    goal_budget = management.get("goal_budget")
    if goal_budget:
        limits_valid(goal_budget["limits"])
        require(goal_budget["source_id"] in sources, "goal budget source missing")
    active_implementers = set()
    for assignment in assignments.values():
        task = assignment["task_id"]
        require(task in nodes and nodes[task]["kind"] == "task", "assignment task outside goal")
        require(assignment["status"] in ASSIGNMENT_STATES and
                assignment["role"] in ("implementation", "review", "coordination"),
                "invalid assignment role/status")
        for field in ("agent_id", "session_id"):
            require(assignment[field] is None or nonempty(assignment[field]), "invalid assignee identity")
        require(assignment["source_id"] in sources, "assignment source missing")
        timestamp(assignment["assigned_at"])
        require(isinstance(assignment["expected_artifacts"], list) and
                all(a in artifacts and task in artifacts[a]["tasks"]
                    for a in assignment["expected_artifacts"]), "assignment artifact/task mismatch")
        limits_valid(assignment["budget_limits"])
        if assignment["status"] in ACTIVE_ASSIGNMENTS and assignment["role"] == "implementation":
            require(not children[task], "active implementation must target a leaf work package")
            require(task not in active_implementers, "multiple active implementation assignments")
            active_implementers.add(task)
        if assignment["status"] in ("released", "cancelled"):
            require(nonempty(assignment.get("reason")), "released/cancelled assignment needs reason")
    observations = {}
    for observation in keyed(management["usage"]).values():
        aid, metric = observation["assignment_id"], observation["metric"]
        require(aid in assignments and assignments[aid]["status"] != "proposed",
                "usage requires an actual assignment")
        require(metric in METRICS and number(observation["amount"], metric), "invalid usage amount")
        require(observation["kind"] in ("observed", "estimated") and
                observation["source_id"] in sources, "invalid usage source/kind")
        when = timestamp(observation["observed_at"])
        require(when >= timestamp(assignments[aid]["assigned_at"]), "usage predates assignment")
        observations.setdefault((aid, metric, observation["kind"]), []).append(observation)
    for key, values in observations.items():
        values.sort(key=lambda v: timestamp(v["observed_at"]))
        for previous, current in zip(values, values[1:]):
            if timestamp(previous["observed_at"]) == timestamp(current["observed_at"]):
                require(previous["amount"] == current["amount"], "conflicting usage at same time")
            if key[2] == "observed":
                require(current["amount"] >= previous["amount"], "cumulative usage regressed")
    for delivery in keyed(management["deliveries"]).values():
        aid = delivery["assignment_id"]
        require(aid in assignments and assignments[aid]["status"] != "proposed",
                "delivery requires an actual assignment")
        require(delivery["artifact_id"] in assignments[aid]["expected_artifacts"],
                "delivery is not an expected assignment artifact")
        require(delivery["source_id"] in sources and positive(delivery["artifact_revision"]) and
                sha(delivery["sha256"]), "invalid delivery provenance")
        require(timestamp(delivery["observed_at"]) >= timestamp(assignments[aid]["assigned_at"]),
                "delivery predates assignment")


def transition_management(old, new):
    before, after = old.get("management"), new.get("management")
    if before is None and after is None:
        return
    require(after is not None, "management history cannot be removed")
    before = before or {"assignments": [], "usage": [], "deliveries": []}
    for field in ("assignments", "usage", "deliveries"):
        prior, current = keyed(before[field]), keyed(after[field])
        require(prior.keys() <= current.keys(), "management records cannot be removed: " + field)
        for key in prior:
            if field != "assignments":
                require(prior[key] == current[key], "usage/delivery observations are immutable")
            else:
                for fixed in ("task_id", "agent_id", "session_id", "role", "assigned_at"):
                    require(prior[key][fixed] == current[key][fixed],
                            "assignment identity immutable; release and create a new assignment")
                if prior[key]["status"] in ("completed", "released", "cancelled"):
                    require(prior[key]["status"] == current[key]["status"],
                            "terminal assignment cannot be reopened")
    if (before["assignments"] != after["assignments"] or
            before.get("goal_budget") != after.get("goal_budget")):
        decision = after.get("decision", {})
        added_sources = keyed(new["sources"]).keys() - keyed(old["sources"]).keys()
        require(nonempty(decision.get("approved_by")) and nonempty(decision.get("reason")) and
                decision.get("source_id") in added_sources,
                "assignment/budget change requires a new sourced management decision")


def observation_freshness(observation, snapshot, at, max_age_hours, source_states):
    source = keyed(snapshot["sources"])[observation["source_id"]]
    if snapshot["mode"] == "real" and source["kind"] == "fixture":
        return "fixture"
    own = freshness({"observed_at": observation["observed_at"], "completeness": "complete"},
                    at, max_age_hours)
    return source_states[source["id"]] if own == "fresh" else own


def budget_accounts(assignment, management, snapshot, at, max_age_hours, source_states):
    accounts = {}
    source = keyed(snapshot["sources"])[assignment["source_id"]]
    limit_current = observation_freshness(
        {"source_id": source["id"], "observed_at": source["observed_at"]},
        snapshot, at, max_age_hours, source_states) == "fresh"
    for metric in METRICS:
        values = [u for u in management["usage"]
                  if u["assignment_id"] == assignment["id"] and u["metric"] == metric]
        latest = {}
        for kind in ("observed", "estimated"):
            candidates = [u for u in values if u["kind"] == kind]
            latest[kind] = max(candidates, key=lambda u: timestamp(u["observed_at"])) if candidates else None
        observed, estimated = latest["observed"], latest["estimated"]
        limit = assignment["budget_limits"].get(metric)
        used = observed["amount"] if observed else None
        state = (observation_freshness(observed, snapshot, at, max_age_hours, source_states)
                 if observed else "unreported")
        current = state == "fresh"
        remaining = round(limit - used, 8) if current and limit is not None and limit_current else None
        status = ("over_budget" if remaining is not None and remaining < 0 else
                  "exhausted" if remaining == 0 else
                  "unknown_limit" if limit is None else
                  "stale_limit" if not limit_current else
                  "estimated_only" if not observed and estimated else
                  state if not current else "within_budget")
        accounts[metric] = {
            "limit": limit, "limit_current": limit_current, "reported_used": used, "usage_freshness": state,
            "current_used": used if current else None, "remaining": remaining, "status": status,
            "usage_id": observed["id"] if observed else None,
            "source_id": observed["source_id"] if observed else None,
            "observed_at": observed["observed_at"] if observed else None,
            "estimated_used": estimated["amount"] if estimated else None,
            "estimate_source_id": estimated["source_id"] if estimated else None,
            "estimate_freshness": observation_freshness(
                estimated, snapshot, at, max_age_hours, source_states) if estimated else None}
    return accounts


def aggregate_budgets(assignments, goal_limits=None, goal_limit_fresh=True):
    """Sum unique assignment accounts, never repeated AC paths or cumulative observations."""
    rows = {a["id"]: a for a in assignments if a["status"] != "proposed"}
    result = {}
    for metric in METRICS:
        missing = [a["id"] for a in rows.values() if a["budget"][metric]["current_used"] is None]
        known = sum(a["budget"][metric]["current_used"] or 0 for a in rows.values())
        used = round(known, 8) if rows and not missing else None
        active = [a for a in rows.values() if a["status"] in ACTIVE_ASSIGNMENTS]
        allocated = (sum(a["budget"][metric]["limit"] for a in active)
                     if all(a["budget"][metric]["limit"] is not None and
                            a["budget"][metric]["limit_current"] for a in active) else None)
        reserved = (sum(max(a["budget"][metric]["remaining"], 0) for a in active)
                    if all(a["budget"][metric]["remaining"] is not None for a in active) else None)
        limit = (goal_limits or {}).get(metric)
        balance = round(limit - used, 8) if limit is not None and used is not None and goal_limit_fresh else None
        result[metric] = {
            "goal_limit": limit, "goal_limit_current": goal_limit_fresh,
            "current_used": used, "known_current_usage_subtotal": round(known, 8),
            "unknown_usage_assignments": missing, "active_allocated_limit": allocated,
            "remaining_to_goal_limit": balance, "active_remaining_allocation": reserved,
            "unallocated": round(balance - reserved, 8) if balance is not None and reserved is not None else None,
            "status": "over_budget" if balance is not None and balance < 0 else
                      "overallocated" if balance is not None and reserved is not None and reserved > balance else
                      "exhausted" if balance == 0 else "incomplete" if used is None else "recorded"}
    return result


def management_view(snapshot, report, at, max_age_hours):
    management = snapshot.get("management")
    data = management or {"assignments": [], "usage": [], "deliveries": []}
    source_states, nodes = report["source_states"], keyed(snapshot["nodes"])
    artifacts = {a["id"]: a for rows in report["index"].values() for a in rows}
    rows, alerts = [], []
    for assignment in data["assignments"]:
        row = copy.deepcopy(assignment)
        row["task_status"] = report["nodes"][row["task_id"]]["status"]
        row["assignment_freshness"] = source_states[row["source_id"]]
        row["budget"] = budget_accounts(row, data, snapshot, at, max_age_hours, source_states)
        row["assets"] = []
        for aid in row["expected_artifacts"]:
            artifact = artifacts[aid]
            receipts = [d for d in data["deliveries"]
                        if d["assignment_id"] == row["id"] and d["artifact_id"] == aid]
            delivery = max(receipts, key=lambda d: timestamp(d["observed_at"])) if receipts else None
            delivery_state = "unreported"
            if delivery:
                observed_state = observation_freshness(delivery, snapshot, at, max_age_hours, source_states)
                delivery_state = ("current" if observed_state == "fresh" and
                                  delivery["artifact_revision"] == artifact["artifact_revision"] and
                                  delivery["sha256"] == artifact["actual_sha256"] and
                                  artifact["availability"] == "present" else "stale_or_unverified")
            row["assets"].append({
                "artifact_id": aid, "path": artifact["resolved_path"], "category": artifact["category"],
                "availability": artifact["availability"], "artifact_revision": artifact["artifact_revision"],
                "delivery": copy.deepcopy(delivery), "delivery_status": delivery_state,
                "evidence_ids": artifact["evidence_ids"]})
            artifact.setdefault("assigned_to", []).append({
                "assignment_id": row["id"], "agent_id": row["agent_id"], "session_id": row["session_id"],
                "status": row["status"], "delivery_status": delivery_state})
        reasons = []
        if row["agent_id"] is None or row["session_id"] is None:
            reasons.append("assignee_identity_incomplete")
        if row["assignment_freshness"] != "fresh":
            reasons.append("assignment_source_" + row["assignment_freshness"])
        if not row["expected_artifacts"]:
            reasons.append("expected_assets_unrecorded")
        if not any(v is not None for v in row["budget_limits"].values()):
            reasons.append("budget_limits_unrecorded")
        if row["status"] in (*ACTIVE_ASSIGNMENTS, "completed"):
            reasons += ["budget_" + metric + "_" + b["status"] for metric, b in row["budget"].items()
                        if metric in row["budget_limits"] and b["status"] != "within_budget"]
        if row["status"] == "completed" and any(a["delivery_status"] != "current" for a in row["assets"]):
            reasons.append("completed_assignment_missing_current_delivery")
        if reasons:
            alerts.append({"assignment_id": row["id"], "task_id": row["task_id"],
                           "owner": nodes[row["task_id"]]["owner"], "reasons": reasons})
        rows.append(row)
    goal_budget = data.get("goal_budget", {})
    goal_source = keyed(snapshot["sources"]).get(goal_budget.get("source_id"))
    goal_limit_current = bool(goal_source and observation_freshness(
        {"source_id": goal_source["id"], "observed_at": goal_source["observed_at"]},
        snapshot, at, max_age_hours, source_states) == "fresh")
    budget = aggregate_budgets(rows, goal_budget.get("limits"),
                              goal_limit_current)
    groups = {}
    for field in ("agent_id", "session_id"):
        groups[field] = []
        for identity in sorted({r[field] for r in rows}, key=lambda v: v or ""):
            assigned = [r for r in rows if r[field] == identity]
            groups[field].append({
                field: identity, "assignment_ids": [r["id"] for r in assigned],
                "task_ids": sorted({r["task_id"] for r in assigned}),
                "current_task_ids": sorted({r["task_id"] for r in assigned if r["status"] in ACTIVE_ASSIGNMENTS}),
                "artifact_ids": sorted({a for r in assigned for a in r["expected_artifacts"]}),
                "budget": aggregate_budgets(assigned)})
    packages = []
    for nid, node in nodes.items():
        if node["kind"] != "task":
            continue
        related = [r for r in rows if r["task_id"] in [nid] + report["nodes"][nid]["descendants"]]
        package = node.get("work_package", {})
        ancestors = report["nodes"][nid]["ancestors"]
        packages.append({
            "task_id": nid, "objective": package.get("objective", node["title"]),
            "objective_basis": "work_package" if package else "legacy_title_only",
            "done_when": package.get("done_when"),
            "requirement_ids": [n for n in ancestors if nodes[n]["kind"] == "requirement"],
            "acceptance": [{"id": n, "criterion": nodes[n]["title"], "status": report["nodes"][n]["status"]}
                           for n in ancestors if nodes[n]["kind"] == "acceptance"],
            "input_artifacts": package.get("input_artifacts", []),
            "output_artifacts": package.get("output_artifacts", node["artifacts"]),
            "write_scope": package.get("write_scope"), "stop_conditions": package.get("stop_conditions"),
            "owner": node["owner"], "status": report["nodes"][nid]["status"],
            "assignment_ids": [r["id"] for r in related],
            "current_assignment_ids": [r["id"] for r in related if r["status"] in ACTIVE_ASSIGNMENTS],
            "budget": aggregate_budgets(related)})
    unmanaged = [p["task_id"] for p in packages if not p["current_assignment_ids"] and
                 nodes[p["task_id"]]["status"] not in ("done", "cancelled")]
    goal_dag = {"goal_id": snapshot["goal_id"], "original_objective": snapshot["goal"]["original_text"],
                "constraints": snapshot["goal"]["constraints"], "goal_status": report["goal_status"],
                "requirements": [{"id": n["id"], "objective": n["title"]} for n in nodes.values()
                                 if n["kind"] == "requirement"],
                "edges": snapshot["edges"], "work_packages": packages,
                "work_package_gaps": [p["task_id"] for p in packages if p["objective_basis"] == "legacy_title_only"]}
    return {"recording_status": "recorded" if management else "not_recorded",
            "assignments": rows, "by_agent": groups["agent_id"], "by_session": groups["session_id"],
            "goal_budget": budget, "unassigned_tasks": unmanaged, "alerts": alerts}, goal_dag


def management_focus(report, agent_id=None, session_id=None):
    rows = [a for a in report["management"]["assignments"]
            if (agent_id is None or a["agent_id"] == agent_id) and
               (session_id is None or a["session_id"] == session_id)]
    return {"agent_id": agent_id, "session_id": session_id, "assignments": rows,
            "task_ids": sorted({a["task_id"] for a in rows}), "budget": aggregate_budgets(rows),
            "status": "matched" if rows else "not_recorded"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_state(path):
    state = read_json(path)
    require(state["contract"] == CONTRACT and state["history"], "invalid ledger")
    previous = None
    event_ids = set()
    for revision, entry in enumerate(state["history"], 1):
        require(entry["revision"] == revision and entry["previous_hash"] == previous,
                "broken history chain")
        require(entry["hash"] == digest({k: v for k, v in entry.items() if k != "hash"}),
                "history hash mismatch")
        require(entry["event"]["id"] not in event_ids, "duplicate event id in history")
        event_ids.add(entry["event"]["id"])
        validate(entry["snapshot"])
        if revision > 1:
            transition(state["history"][revision - 2]["snapshot"], entry["snapshot"])
        previous = entry["hash"]
    return state


def append_state(state, snapshot, event_id, reason):
    history = state["history"]
    entry = {"revision": len(history) + 1,
             "previous_hash": history[-1]["hash"] if history else None,
             "event": {"id": event_id, "recorded_at": now(), "reason": reason,
                       "source_id": snapshot["source_id"]},
             "snapshot": copy.deepcopy(snapshot)}
    entry["hash"] = digest(entry)
    history.append(entry)
    return entry


def save(state_path, snapshot, event_id, reason, expected=None):
    validate(snapshot)
    require(nonempty(event_id) and nonempty(reason), "event id/reason required")
    state_path = Path(state_path)
    require(not state_path.is_symlink(), "ledger cannot be a symlink")
    lock = state_path.with_name(state_path.name + ".lock")
    # One writer; refusal on an existing lock avoids lost updates. No automatic lock deletion.
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    temp = None
    try:
        os.close(fd)
        if expected is None:
            require(not state_path.exists(), "ledger already exists")
            state = {"contract": CONTRACT, "history": []}
        else:
            state = load_state(state_path)
            for entry in state["history"]:
                if entry["event"]["id"] == event_id:
                    require(entry["snapshot"] == snapshot and entry["event"]["reason"] == reason,
                            "event id conflict")
                    return {"status": "unchanged", "ledger_revision": len(state["history"])}
            require(expected == len(state["history"]), "ledger revision conflict")
            transition(state["history"][-1]["snapshot"], snapshot)
        entry = append_state(state, snapshot, event_id, reason)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=state_path.parent,
                                         delete=False) as stream:
            temp = Path(stream.name)
            json.dump(state, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, state_path)
        return {"status": "recorded", "ledger_revision": entry["revision"], "hash": entry["hash"]}
    finally:
        if temp is not None and temp.exists():
            temp.unlink()
        lock.unlink()


def artifact_index(snapshot):
    result = {category: [] for category in CATEGORIES}
    for artifact in snapshot["artifacts"]:
        row = copy.deepcopy(artifact)
        row["evidence_ids"] = [e["id"] for e in snapshot["evidence"]
                               if artifact["id"] in e["bindings"] or
                               artifact["id"] == e["record_artifact"]]
        row["resolved_path"], row["actual_sha256"] = None, None
        if artifact["path"] is None:
            row["availability"] = "unlocated"
        else:
            try:
                path = local_path(Path(snapshot["repo"]), artifact["path"])
                row["resolved_path"] = str(path)
                if not path.is_file():
                    row["availability"] = "missing"
                elif path.stat().st_size > 16 * 1024 * 1024:
                    row["availability"] = "unverified_large"
                else:
                    row["actual_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                    row["availability"] = ("present" if artifact["sha256"] == row["actual_sha256"]
                                           else "unhashed" if artifact["sha256"] is None else "changed")
            except (ValueError, OSError) as error:
                row["availability"] = "unreadable"
                row["error"] = str(error)
        result[artifact["category"]].append(row)
    return result


def freshness(source, at, max_age_hours):
    age = (at - timestamp(source["observed_at"])).total_seconds() / 3600
    if age < 0:
        return "future"
    if age > max_age_hours:
        return "stale"
    return "fresh" if source["completeness"] == "complete" else "partial"


def assess(snapshot, at=None, max_age_hours=24):
    validate(snapshot)
    at = timestamp(at) if isinstance(at, str) else at or datetime.now(timezone.utc)
    require(max_age_hours > 0, "max age must be positive")
    sources, nodes = keyed(snapshot["sources"]), keyed(snapshot["nodes"])
    index = artifact_index(snapshot)
    artifacts = {a["id"]: a for rows in index.values() for a in rows}
    source_status = {key: freshness(s, at, max_age_hours) for key, s in sources.items()}
    decomposition = graph(snapshot, "decomposes")
    parents = graph(snapshot, "decomposes", True)
    prerequisites = graph(snapshot, "precedes", True)
    dependents = graph(snapshot, "precedes")
    evidence_states = {}
    for evidence in snapshot["evidence"]:
        problems = []
        if evidence["artifact_revision"] != snapshot["artifact_revision"]:
            problems.append("stale_revision")
        if source_status[evidence["source_id"]] != "fresh":
            problems.append("source_" + source_status[evidence["source_id"]])
        age = (at - timestamp(evidence["observed_at"])).total_seconds() / 3600
        if age < 0 or age > max_age_hours:
            problems.append("stale_or_future_observation")
        for aid, expected in evidence["bindings"].items():
            if artifacts[aid]["availability"] != "present" or artifacts[aid]["actual_sha256"] != expected:
                problems.append("stale_binding:" + aid)
        record = artifacts.get(evidence["record_artifact"])
        if evidence["result"] in ("pass", "fail"):
            if not record or record["availability"] != "present":
                problems.append("missing_record")
            elif record["actual_sha256"] != evidence["record_sha256"]:
                problems.append("stale_record")
        simulated = evidence["kind"] == "fixture" or sources[evidence["source_id"]]["kind"] == "fixture"
        if snapshot["mode"] == "real" and simulated:
            problems.append("fixture_not_real")
        evidence_states[evidence["id"]] = {"result": evidence["result"], "problems": problems,
                                           "simulated": simulated}
    observations = {}
    for nid, node in nodes.items():
        candidates = [e for e in snapshot["evidence"] if nid in e["nodes"]]
        # Latest observation wins; a tied failure cannot be masked by a pass.
        rank = {"pass": 0, "not_run": 1, "blocked": 2, "fail": 3}
        candidates.sort(key=lambda e: (timestamp(e["observed_at"]), rank[e["result"]]), reverse=True)
        reason, selected, own = [], None, node["status"]
        if candidates:
            selected = candidates[0]
            verdict = evidence_states[selected["id"]]
            reason.extend(verdict["problems"])
            required = set(node["artifacts"])
            if selected["result"] == "pass" and (not any(
                    artifacts[a]["role"] == "subject" for a in required) or
                    not required <= selected["bindings"].keys()):
                reason.append("missing_subject_bindings")
            if reason:
                own = "stale" if any("stale" in p for p in reason) else "missing_evidence"
            elif selected["result"] != "pass":
                own = selected["result"]
                reason.append("evidence_" + own)
            elif node["status"] == "done":
                own = "simulated_done" if snapshot["mode"] == "fixture" else "verified_done"
        elif node["status"] == "done" and node["kind"] in ("task", "acceptance"):
            own = "missing_evidence"
            reason.append("no_evidence")
        if node["status"] in ("cancelled", "blocked"):
            own = node["status"]
            reason.append(node["reason"])
        if node["kind"] == "task" and node["owner"] is None:
            reason.append("owner_unassigned")
        observations[nid] = {"id": nid, "kind": node["kind"], "title": node["title"],
                             "reported_status": node["status"], "evidence_status": own,
                             "status": own, "reasons": reason, "owner": node["owner"],
                             "session_id": node["session_id"],
                             "selected_evidence": selected["id"] if selected else None}
    accepted = {"verified_done", "simulated_done"}
    # Evaluation edges mean prerequisite -> consumer, child -> parent.
    for nid in topological(completion_graph(snapshot)):
        item = observations[nid]
        blockers = [n for n in prerequisites[nid] + decomposition[nid]
                    if observations[n]["status"] not in accepted]
        item["blocked_by"] = sorted(set(blockers))
        if blockers and item["status"] != "cancelled":
            item["status"] = "blocked"
        if (item["kind"] in ("goal", "requirement") and decomposition[nid] and not blockers
                and item["evidence_status"] not in
                ("blocked", "cancelled", "fail", "not_run", "stale", "missing_evidence")):
            item["status"] = "simulated_done" if snapshot["mode"] == "fixture" else "verified_done"
        item["upstream"] = reachable(prerequisites, nid)
        item["downstream"] = reachable(dependents, nid)
        item["ancestors"] = reachable(parents, nid)
        item["descendants"] = reachable(decomposition, nid)
        item["affected_acceptance"] = sorted({a for target in [nid] + item["downstream"]
                                               for a in reachable(parents, target)
                                               if nodes[a]["kind"] == "acceptance"})
    gaps = []
    root = snapshot["goal"]["node_id"]
    covered = set(reachable(decomposition, root)) | {root}
    for nid, node in nodes.items():
        if nid not in covered:
            gaps.append({"node": nid, "reason": "unmapped_to_original_goal"})
        if node["kind"] in ("goal", "requirement", "acceptance") and not decomposition[nid]:
            gaps.append({"node": nid, "reason": "missing_decomposition"})
        if node["status"] == "cancelled":
            gaps.append({"node": nid, "reason": "cancelled_scope_needs_goal_review"})
    primary_freshness = source_status[snapshot["source_id"]]
    alignment = snapshot.get("alignment", {})
    alignment_current = (alignment.get("status") == "aligned" and
                         alignment.get("artifact_revision") == snapshot["artifact_revision"] and
                         source_status.get(alignment.get("source_id")) == "fresh")
    acceptances = [n for n in nodes if nodes[n]["kind"] == "acceptance"]
    complete = (bool(acceptances) and not gaps and alignment_current and
                primary_freshness == "fresh" and
                observations[root]["status"] in accepted and
                all(observations[n]["status"] in accepted for n in acceptances))
    goal_status = ("simulated_complete" if snapshot["mode"] == "fixture" else "verified_complete") if complete else "incomplete"
    next_actions = [{"node": nid, "owner": n["owner"], "session_id": n["session_id"],
                     "action": "assign_owner" if n["owner"] is None else
                               "refresh_evidence" if n["evidence_status"] in ("stale", "missing_evidence")
                               else "resolve_or_report",
                     "reasons": n["reasons"], "status": n["status"]}
                    for nid, n in observations.items() if n["kind"] == "task" and
                    n["status"] not in accepted and n["status"] != "cancelled" and not n["blocked_by"]]
    if not next_actions and not complete:
        next_actions = [{"node": root, "owner": nodes[root]["owner"],
                         "session_id": nodes[root]["session_id"],
                         "action": "reconcile_goal_alignment_sources_and_acceptance"}]
    report = {"identity": {k: snapshot[k] for k in IDENTITY},
            "artifact_revision": snapshot["artifact_revision"], "as_of": at.isoformat(),
            "source_id": snapshot["source_id"], "source_freshness": primary_freshness,
            "source_states": source_status, "goal_status": goal_status,
            "alignment": alignment or {"status": "unreviewed"}, "alignment_current": alignment_current,
            "gaps": gaps, "task_counts": dict(Counter(n["status"] for n in observations.values()
                                                     if n["kind"] == "task")),
            "progress_basis": "AC evidence + dependency closure + source freshness + goal alignment; no task percentage",
            "nodes": observations, "evidence": evidence_states, "index": index,
            "next_actions": next_actions}
    report["management"], report["goal_dag"] = management_view(snapshot, report, at, max_age_hours)
    return report


def mermaid(snapshot, report):
    lines = ["flowchart TD"]
    ids = {n["id"]: "n" + str(i) for i, n in enumerate(snapshot["nodes"])}
    for node in snapshot["nodes"]:
        label = node["id"] + " " + node["title"] + " [" + report["nodes"][node["id"]]["status"] + "]"
        if node.get("work_package"):
            label += " / 目标: " + node["work_package"]["objective"]
        assigned = [a for a in report["management"]["assignments"]
                    if a["task_id"] == node["id"] and a["status"] in ACTIVE_ASSIGNMENTS]
        if assigned:
            label += " / " + ", ".join((a["agent_id"] or "?") + "@" + (a["session_id"] or "?")
                                      for a in assigned)
        label = label.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", " ")
        lines.append(f'  {ids[node["id"]]}["{label}"]')
    for edge in snapshot["edges"]:
        connector = "-->|decomposes|" if edge["type"] == "decomposes" else "-.->|precedes|"
        lines.append(f'  {ids[edge["from"]]} {connector} {ids[edge["to"]]}')
    return "\n".join(lines)


def markdown_index(report):
    labels = dict(zip(CATEGORIES, ("产品文档", "技术文档", "需求列表", "问题列表")))
    def cell(value):
        return str(value).replace("|", "&#124;").replace("\n", " ")
    lines = [f'Goal: {report["identity"]["goal_id"]}; as of {report["as_of"]}',
             f'Source: {report["source_id"]} ({report["source_freshness"]})']
    for category, rows in report["index"].items():
        lines += ["", "## " + labels[category], "",
                  "| ID | 路径 | 文件状态 | REQ / TASK | owner | revision | evidence |",
                  "| --- | --- | --- | --- | --- | --- | --- |"]
        for row in rows:
            values = (row["id"], row["resolved_path"] or "unlocated", row["availability"],
                      ", ".join(row["requirements"] + row["tasks"]), row["owner"] or "unassigned",
                      row["artifact_revision"], ", ".join(row["evidence_ids"]) or "none")
            lines.append("| " + " | ".join(cell(v) for v in values) + " |")
        if not rows:
            lines.append("| — | 未登记 | missing | — | unassigned | — | none |")
    return "\n".join(lines)


def markdown_brief(report):
    def cell(value):
        return ("未记录" if value is None else str(value)).replace("|", "&#124;").replace("\n", " ")
    def row(values):
        return "| " + " | ".join(cell(v) for v in values) + " |"
    goal, management = report["goal_dag"], report["management"]
    lines = [f'Goal {goal["goal_id"]}: {cell(goal["original_objective"])}',
             f'状态: {report["goal_status"]}; 来源: {report["source_freshness"]}; 时间: {report["as_of"]}',
             f'分配记录: {management["recording_status"]}; 所有预算为来源报告，不是自动计费。',
             "", "## DAG 工作目标", "",
             "| TASK | 具体目标 | 完成条件 | REQ / AC | 当前分配 |",
             "| --- | --- | --- | --- | --- |"]
    for package in goal["work_packages"]:
        lines.append(row((package["task_id"], package["objective"], package["done_when"],
                          ", ".join(package["requirement_ids"] + [a["id"] for a in package["acceptance"]]),
                          ", ".join(package["current_assignment_ids"]) or "未分配")))
    lines += ["", "## agent / session 与资产", "",
              "| 分配 / TASK | agent | session | 分配状态 | 预期资产 / 文件 / 交付记录 |",
              "| --- | --- | --- | --- | --- |"]
    for assignment in management["assignments"]:
        assets = "; ".join(a["artifact_id"] + ": " + a["availability"] + "/" + a["delivery_status"]
                           for a in assignment["assets"])
        lines.append(row((assignment["id"] + " / " + assignment["task_id"], assignment["agent_id"],
                          assignment["session_id"], assignment["status"], assets or "未记录")))
    lines += ["", "## 预算", "",
              "| 分配 | 单位 | 上限 | 来源报告已用 | 当前剩余 | 状态 |",
              "| --- | --- | --- | --- | --- | --- |"]
    for assignment in management["assignments"]:
        shown = False
        for metric, budget in assignment["budget"].items():
            if metric in assignment["budget_limits"] or budget["usage_id"] or budget["estimated_used"] is not None:
                lines.append(row((assignment["id"], metric, budget["limit"], budget["reported_used"],
                                  budget["remaining"], budget["status"])))
                shown = True
        if not shown:
            lines.append(row((assignment["id"], "—", None, None, None, "not_recorded")))
    for metric, budget in management["goal_budget"].items():
        if budget["goal_limit"] is not None:
            lines.append(row(("GOAL（不与分配预算重复相加）", metric, budget["goal_limit"],
                              budget["current_used"], budget["remaining_to_goal_limit"], budget["status"])))
    lines += ["", "未分配任务: " + (", ".join(management["unassigned_tasks"]) or "无"),
              "工作目标/完成条件未完整记录: " + (", ".join(goal["work_package_gaps"]) or "无")]
    for alert in management["alerts"]:
        lines.append("- " + cell(alert["assignment_id"]) + ": " + cell(", ".join(alert["reasons"])))
    lines += ["", markdown_index(report)]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("validate")
    check.add_argument("--snapshot", required=True, type=Path)
    for name in ("init", "refresh"):
        cmd = commands.add_parser(name)
        cmd.add_argument("--snapshot", required=True, type=Path)
        cmd.add_argument("--state", required=True, type=Path)
        cmd.add_argument("--event-id", required=True)
        cmd.add_argument("--reason", required=True)
        if name == "refresh":
            cmd.add_argument("--expected-revision", required=True, type=int)
    for name in ("query", "dag", "index", "brief"):
        cmd = commands.add_parser(name)
        cmd.add_argument("--state", required=True, type=Path)
        cmd.add_argument("--at", help="ISO timestamp; explicit historical replay, never live freshness")
        cmd.add_argument("--max-age-hours", type=float, default=24)
        if name == "query":
            cmd.add_argument("--node")
            cmd.add_argument("--agent", help="filter assignment records by exact agent ID")
            cmd.add_argument("--session", help="filter assignment records by exact session ID")
    args = parser.parse_args()
    try:
        if args.command == "validate":
            validate(read_json(args.snapshot))
            result = {"status": "valid", "behavior_verified": False}
        elif args.command in ("init", "refresh"):
            result = save(args.state, read_json(args.snapshot), args.event_id, args.reason,
                          getattr(args, "expected_revision", None))
        else:
            state = load_state(args.state)
            snapshot = state["history"][-1]["snapshot"]
            result = assess(snapshot, args.at, args.max_age_hours)
            result["ledger_revision"] = len(state["history"])
            result["historical_replay"] = args.at is not None
            if args.command == "dag":
                print(mermaid(snapshot, result))
                return 0
            if args.command == "index":
                print(markdown_index(result))
                return 0
            if args.command == "brief":
                print(markdown_brief(result))
                return 0
            if args.node:
                require(args.node in result["nodes"], "unknown node")
                result["focus"] = result["nodes"][args.node]
                result["focus"]["work_package"] = next(
                    (p for p in result["goal_dag"]["work_packages"] if p["task_id"] == args.node), None)
            if args.agent or args.session:
                result["assignment_focus"] = management_focus(result, args.agent, args.session)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as error:
        print(json.dumps({"status": "needs_input", "error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
