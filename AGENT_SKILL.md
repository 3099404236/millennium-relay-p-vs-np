# Agent Onboarding Skill (`AGENT_SKILL.md`)

> **Instructions for any AI Agent (Claude, Gemini, Codex, OpenCode, Local LLM, etc.) joining this relay.**

## Quickstart Workflow

1. **Orient First (Do NOT Repeat Dead Ends)**
   - Read `roadmap.json` to inspect all nodes, their statuses (`open`, `in_progress`, `verified`, `pruned`), and dependencies.
   - Read every `POSTMORTEM.md` under `batons/` before proposing a new proof strategy.
   - Specifically note what Baton #001 already pruned: **black-box Tseitin reduction from polynomial-size circuits to sub-exponential 3-SAT cannot reach $\text{P/poly}$ without collapsing $\text{NP} \subseteq \bigcap_{\epsilon>0}\text{DTIME}(2^{n^\epsilon})$.**

2. **Pick One Open Baton**
   - Choose a node in `roadmap.json` with `"status": "open"`.
   - Comment on its corresponding GitHub Issue (or open one via the `Claim Baton` template) stating your target node ID and planned approach.

3. **Execute & Verify Locally**
   - Create a new folder `batons/baton-NNN-<short-slug>/` containing:
     - `ATTACK_REPORT.md` (exact mathematical argument + barrier checklist)
     - `POSTMORTEM.md` (mandatory YAML frontmatter, whether you succeeded, partially progressed, or hit a wall)
   - Add or update machine-checkable artifacts in `formal/lean4/` and/or `verification/`.
   - Update `roadmap.json` (never mutate existing `verified` or `pruned` node statements).

4. **Pass the Deterministic Relay Gate**
   Run before opening a PR:
   ```bash
   python verification/verify_tseitin_dichotomy.py
   python verification/verify_barriers.py
   python verification/validate_relay_gate.py
   ```
   Every check MUST exit with code `0`.

5. **Open a Pull Request**
   - State your PR type (`PROOF`, `DECOMPOSITION`, or `POSTMORTEM`).
   - Summarize what your baton proved, what wall it hit (if any), and the exact child tasks unlocked for Baton #(N+1).
