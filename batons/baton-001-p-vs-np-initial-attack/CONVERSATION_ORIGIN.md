# Origin Record: How This Crowdsourced Relay Started

- **Date**: 2026-11-26
- **Originating Concept**: Crowdsourced Distributed AI Agent Relay for Millennium Prize Problems

## 1. The Founding Idea (User Prompt Summary)

> Pick an unsolved Millennium Prize Problem, attempt to solve it, and upload the work to GitHub regardless of success or failure — turning the session into a **crowdsourced relay** where thousands of ordinary people running dozens of AI agents each can hand off progress and collectively rival big tech labs that spin up 10,000 centralized agents.

## 2. Literature & Ecosystem Validation (Exa Search, Nov 2026)

Before building this repository, we ran a live literature and ecosystem check via Exa Search to verify both (a) which Millennium Prize Problems remain unsolved in late 2026, and (b) whether the crowdsourced AI-agent relay model actually works.

### Key Precedents Found
1. **Choir (Yidi Qi & Melanie Weber, Sep 2026, arXiv:2609.31903)** — *An Open Protocol for Distributed Multi-Agent Autoformalization*: Proves that independent contributors running their own LLM subscriptions can coordinate entirely through GitHub (Issues for task claims, PRs for proofs or sub-lemma decompositions, GitHub Actions as a deterministic Lean/Isabelle/Rocq verification gate).
2. **Open Proof Network (`github.com/thisisanameforsure/open_proof_network`)**: Applies the git-as-queue, kernel-as-gate architecture specifically to *genuinely open* mathematical conjectures, introducing the **"Failure pays"** principle (structured postmortems of failed attempts are first-class ledger artifacts).
3. **PolyProof (`github.com/polyproof/polyproof`)**: Agent-native Lean 4 collaboration platform where AI agents read shared research threads, build on partial progress, and publish compiler-verified PRs.
4. **Terence Tao — *New Mathematical Workflows* (June 2026) & *Equational Theories Project* (arXiv:2512.07087)**: Demonstrates that crowdsourced GitHub + formal verification resolved 22,028,942 equational implications, while warning against **"proof indigestion"** when unverified AI prose floods forums without modularization or machine-checked gates.

### Why We Did NOT Just Dump a Raw Chat Log
A raw chat transcript cannot be verified by CI, cannot be claimed modularly by downstream agents, and causes proof indigestion. Instead, Baton #001 transforms the originating conversation into:
- A structured mathematical attack & barrier analysis (`ATTACK_REPORT.md`)
- A machine-readable failure postmortem (`POSTMORTEM.md`)
- Executable Python verification scripts (`verification/`)
- A Lean 4 formalization skeleton (`formal/lean4/`)
- A GitHub Actions deterministic gate (`.github/workflows/relay-gate.yml`)
- A DAG roadmap (`roadmap.json`) ready for Baton #002+ to claim via GitHub Issues & PRs.
