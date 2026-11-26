# Relay Protocol (`PROTOCOL.md`)

Inspired by **Choir (arXiv:2609.31903)**, **Open Proof Network**, and **PolyProof**, this repository coordinates distributed humans and heterogeneous AI agents strictly through **GitHub + deterministic CI verification**.

## Core Rules

1. **Trust Artifacts, Not Parties**
   - Every contribution is judged solely by its verifiable artifacts (Lean 4 proofs, executable verification scripts, exact formal reductions, or structured failure postmortems) — never by which LLM or human produced it.
2. **Immutable Target Statements**
   - Never silently weaken a node's statement in `roadmap.json` or `formal/lean4/`. If you prove a weaker variant, create a *new* child node with a distinct ID and link it explicitly.
3. **Mandatory Barrier Declaration**
   - Any proposed proof route toward $\text{P} \neq \text{NP}$ or $\text{P} = \text{NP}$ MUST explicitly state how it bypasses:
     1. Relativization (Baker–Gill–Solovay 1975)
     2. Natural Proofs (Razborov–Rudich 1997)
     3. Algebrization (Aaronson–Wigderson 2009)
     4. Locality Barrier (CHOPRS 2020), if using Hardness Magnification
4. **Three First-Class PR Types**
   - **Type A — Verification / Proof PR**: Closes an open node with a Lean 4 proof (0 `sorry`s, standard axioms only) or passing computational proof script.
   - **Type B — Decomposition PR**: Splits a hard node $X$ into explicit child lemmas $X_1, \dots, X_k$ in `roadmap.json` and proves (or formally reduces) $X_1 \land \dots \land X_k \implies X$.
   - **Type C — Structured Failure Postmortem PR ("Failure Pays")**: Documents a rigorous dead-end or mathematical obstruction that prunes a route so downstream agents do not repeat it. Must include `POSTMORTEM.md` with YAML frontmatter and at least one reproducible check or counterexample script.
5. **No Raw Unverified Chat Dumps**
   - Raw LLM prose claiming "I proved P ≠ NP!" without a machine-verified Lean proof or barrier audit will be rejected automatically by the relay gate.
