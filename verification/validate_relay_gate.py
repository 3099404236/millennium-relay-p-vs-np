#!/usr/bin/env python3
"""
Deterministic Relay Gate (`validate_relay_gate.py`).

Enforces repository-level integrity on every PR (inspired by Choir & Open Proof Network):
1. `roadmap.json` parses cleanly, has unique node IDs, and forms an acyclic DAG.
2. Every referenced artifact path exists on disk.
3. Every `pruned`, `verified`, or `blocked_by_barrier` node has an owner_baton and
   its verification_cmd (if any) passes cleanly.
4. Every baton directory under `batons/` contains `ATTACK_REPORT.md` and `POSTMORTEM.md`
   with required YAML metadata fields (`baton_id`, `outcome`, `p_vs_np_resolved`).
5. No unverified claim of `p_vs_np_resolved: true` unless `root-p-vs-np` is marked `verified`
   with zero `sorry`s in Lean 4 formalizations.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
from typing import Dict, List, Set

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


def check_dag_acyclic(nodes: List[dict]) -> None:
    id_map: Dict[str, dict] = {}
    for node in nodes:
        nid = node["id"]
        if nid in id_map:
            raise AssertionError(f"Duplicate node ID in roadmap.json: {nid}")
        id_map[nid] = node

    # Check all dependencies exist
    for node in nodes:
        for dep in node.get("dependencies", []):
            if dep not in id_map:
                raise AssertionError(f"Node '{node['id']}' depends on unknown node '{dep}'")

    # DFS cycle detection
    state: Dict[str, int] = {}  # 0=unvisited, 1=visiting, 2=done

    def dfs(nid: str) -> None:
        st = state.get(nid, 0)
        if st == 1:
            raise AssertionError(f"Cycle detected in roadmap.json involving '{nid}'")
        if st == 2:
            return
        state[nid] = 1
        for dep in id_map[nid].get("dependencies", []):
            dfs(dep)
        state[nid] = 2

    for nid in id_map:
        dfs(nid)

    print(f"[GATE PASS] roadmap.json DAG validated ({len(nodes)} nodes, 0 cycles).")


def check_artifacts_and_commands(nodes: List[dict]) -> None:
    allowed_statuses = {"open", "in_progress", "verified", "pruned", "blocked_by_barrier"}
    for node in nodes:
        status = node.get("status")
        if status not in allowed_statuses:
            raise AssertionError(f"Invalid status '{status}' on node '{node['id']}'")

        for rel_path in node.get("artifacts", []):
            full = REPO_ROOT / rel_path
            if not full.exists():
                raise AssertionError(f"Missing artifact '{rel_path}' referenced by '{node['id']}'")

        if status in {"verified", "pruned", "blocked_by_barrier"}:
            if not node.get("owner_baton"):
                raise AssertionError(f"Completed/pruned node '{node['id']}' missing owner_baton")
            cmd = node.get("verification_cmd")
            if cmd:
                # Only allow safe python verification scripts inside verification/
                if not re.fullmatch(r"python verification/[a-zA-Z0-9_]+\.py", cmd):
                    raise AssertionError(f"Disallowed verification_cmd format: {cmd}")
                res = subprocess.run(
                    [sys.executable, cmd.split()[1]],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                )
                if res.returncode != 0:
                    raise AssertionError(
                        f"Verification command failed for '{node['id']}':\n{res.stdout}\n{res.stderr}"
                    )
    print("[GATE PASS] All referenced artifacts exist and node verification commands passed.")


def check_batons_and_honesty(nodes: List[dict]) -> None:
    batons_dir = REPO_ROOT / "batons"
    if not batons_dir.exists():
        raise AssertionError("Missing batons/ directory")

    baton_folders = [p for p in batons_dir.iterdir() if p.is_dir()]
    if not baton_folders:
        raise AssertionError("No baton folders found under batons/")

    root_node = next((n for n in nodes if n["id"] == "root-p-vs-np"), None)
    if root_node is None:
        raise AssertionError("Missing 'root-p-vs-np' node in roadmap.json")

    required_fields = ["baton_id:", "target_problem:", "outcome:", "p_vs_np_resolved:"]
    for folder in baton_folders:
        attack = folder / "ATTACK_REPORT.md"
        postmortem = folder / "POSTMORTEM.md"
        if not attack.exists():
            raise AssertionError(f"Baton '{folder.name}' missing ATTACK_REPORT.md")
        if not postmortem.exists():
            raise AssertionError(f"Baton '{folder.name}' missing POSTMORTEM.md")

        pm_text = postmortem.read_text(encoding="utf-8")
        for field in required_fields:
            if field not in pm_text:
                raise AssertionError(f"Baton '{folder.name}' POSTMORTEM.md missing required field '{field}'")

        # Guard against unverified claims of solving P vs NP
        if re.search(r"p_vs_np_resolved:\s*true", pm_text, re.IGNORECASE):
            if root_node["status"] != "verified":
                raise AssertionError(
                    f"Baton '{folder.name}' claims p_vs_np_resolved: true, but root-p-vs-np is not verified!"
                )
            lean_files = list((REPO_ROOT / "formal" / "lean4").rglob("*.lean"))
            if not lean_files:
                raise AssertionError("Claiming P vs NP resolution requires formal Lean 4 proof files.")
            for lf in lean_files:
                if re.search(r"\bsorry\b", lf.read_text(encoding="utf-8")):
                    raise AssertionError(f"Cannot claim resolution while '{lf.name}' contains `sorry`.")

    print(f"[GATE PASS] Validated {len(baton_folders)} baton folder(s) and honesty guardrails.")


def main() -> None:
    roadmap_path = REPO_ROOT / "roadmap.json"
    data = json.loads(roadmap_path.read_text(encoding="utf-8"))
    nodes = data.get("nodes", [])
    check_dag_acyclic(nodes)
    check_artifacts_and_commands(nodes)
    check_batons_and_honesty(nodes)
    print("RELAY GATE: ALL CHECKS GREEN.")


if __name__ == "__main__":
    main()
