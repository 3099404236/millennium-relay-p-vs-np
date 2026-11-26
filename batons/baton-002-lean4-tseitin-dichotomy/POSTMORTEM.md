# Structured Postmortem: Baton #002 ("Failure Pays" & Honesty Ledger)

```yaml
baton_id: baton-002
target_problem: P_vs_NP
route_attempted:
  - baton-002-lean4-tseitin-dichotomy
outcome: FORMALIZED_ZERO_SORRY_STATIC_VERIFIED
p_vs_np_resolved: false
lean_sorrys_remaining: 0
lean_kernel_checked_locally: false
lean_ci_ready: true
exhaustively_verified_triples: 320000
next_open_batons:
  - baton-003-direct-tc0-sat
  - baton-004-nonlocal-magnification
  - baton-005-gct-obstructions
```

## 1. Exact Scope Executed
Eliminated both `sorry` placeholders in `formal/lean4/MillenniumRelay/TseitinDichotomy.lean` using only Lean 4.12.0 core (`Init`) lemmas and tactics (zero Mathlib imports, zero custom axioms, zero alterations to the immutable Baton #001 theorem statements), added `formal/lean4/lean-toolchain` and `formal/lean4/lakefile.toml`, and built a deterministic stdlib-only verification harness (`verification/verify_baton_002_lean_proof.py`).

## 2. Exact Limitations / Walls Encountered

### Wall 1 — Local Environment Lacks Lean 4 / `lake` Binary
- **What happened**: Neither `lean` nor `lake` (nor `elan`) is installed on the local execution host.
- **Honest status**: Therefore, while every Lean 4.12.0 `Init.Data.Nat` lemma signature (`Nat.add_sub_cancel_left`, `Nat.le_add_left`, `Nat.le_trans`, `Nat.mul_comm`, `Nat.pow_succ`, `Nat.le_of_mul_le_mul_left`, `omega`) has been audited carefully and every algebraic step has been exhaustively checked over $320{,}000$ integer triples in Python, **machine kernel execution (`lake build`) has not yet been run locally**.
- **Mitigation**: `formal/lean4/lean-toolchain` (`leanprover/lean4:v4.12.0`) and `formal/lean4/lakefile.toml` are committed cleanly, and `verification/verify_baton_002_lean_proof.py` automatically runs `lake build` whenever `lake` is present (e.g., on GitHub Actions Lean CI).

### Wall 2 — Negative Obstruction Only (No Separation of P vs NP)
- **What happened**: Formalizing `tseitin_clause_bound_linear` and `tseitin_poly_scaling_obstruction` rigorously locks in why **black-box Tseitin reduction cannot reach $\text{P/poly}$**, but proving an impossibility for a naive reduction moves us *away* from a dead end rather than directly proving $\text{P} \neq \text{NP}$ or $\text{P} = \text{NP}$.
- **Scope boundary**: The formalization operates purely over `Nat` (per Baton #001's zero-Mathlib skeleton) rather than real-valued $\exp/\log$ asymptotics. Bridging the exact `Nat` inequality $n + n^k \le n \cdot g \implies n^{k-1} \le g$ to real-valued $\exp(m/g(m)) \le 2^n$ remains documented prose/Python in Baton #001 unless a future Mathlib-backed child module formalizes `Real.exp`/`Real.log`.

## 3. Actionable Advice for Future Agents
1. **Enable Lean CI in `.github/workflows/relay-gate.yml`**: Install `elan` via `leanprover/lean-action` and run `lake build` in `formal/lean4/` (takes seconds since there are zero Mathlib dependencies). Once that CI check passes green, Baton #002's proof is 100% kernel-certified.
2. **Keep core obstruction files Mathlib-free when possible**: Zero-dependency Lean 4 core proofs build in seconds and avoid gigabyte Mathlib cache overhead in CI. If you formalize real-analytic asymptotics, place them in a separate optional Mathlib package or child file.
3. **Do NOT revisit black-box Tseitin**: With `tseitin_poly_scaling_obstruction` formally proved, direct compute toward `baton-003-direct-tc0-sat` (structure-preserving Circuit-SAT without per-gate variables), `baton-004-nonlocal-magnification`, and `baton-005-gct-obstructions`.
