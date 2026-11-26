# Structured Postmortem: Baton #019 ("Failure Pays" & Honesty Ledger)

```yaml
baton_id: baton-019
target_problem: P_vs_NP
route_attempted:
  - baton-019-lean4-valiant-and-frobenius
outcome: LEAN4_VALIANT_FROBENIUS_VERIFIED
p_vs_np_resolved: false
lean_modules_total: 3
lean_theorems_added: 19
lean_sorrys_remaining: 0
lean_warnings_on_new_module: 0
lean_axioms_used:
  - propext
  - Quot.sound
lean_classical_choice_used: false
lean_kernel_checked_locally: true
local_lean_toolchain: leanprover/lean4:v4.36.0-rc2
ci_lean_toolchain: leanprover/lean4:v4.12.0
next_open_batons:
  - formal-valiant-dag-path-halving
  - formal-f2-pc-frobenius-homomorphism
  - res-xor-subspace-switching
```

## 1. Exact Scope Executed
Extended the zero-Mathlib Lean 4.12 formal library (`formal/lean4/MillenniumRelay/`) with its third module, `formal/lean4/MillenniumRelay/ValiantAndAlgebrization.lean`, registered `"MillenniumRelay.ValiantAndAlgebrization"` in `formal/lean4/lakefile.toml`, and created the deterministic Python 3.12 stdlib-only verification harness `verification/verify_baton_019_lean4_valiant_frobenius.py`.

All four mandated theorem groups (19 total constructive theorems + 1 helper `def xorFin`) were machine-checked by a live local Lean 4 kernel with **0 errors, 0 warnings, 0 `sorry`s, 0 custom axioms, and 0 `Classical.choice`**:
1. **$\mathbb{F}_2$ Frobenius & Boolean Ring Identities (Baton #012)**: `f2_idempotent`, `f2_frobenius_add_sq`, `f2_xor_cancel_right`, `f2_xor_self`, `f2_and_xor_distrib_left`, `f2_frobenius_xorFin_sq`, `f2_xorFin_idempotent` — all 7 depend on **0 axioms**.
2. **Valiant Iterated Edge-Removal Budget (Batons #014 & #015)**: `valiant_iterated_cut_budget`, `valiant_iterated_cut_budget_div`, and `valiant_iterated_msb_existence` (constructively composing Baton #015's `valiant_msb_halving_step` across $t$ rounds without `Classical.choice`).
3. **Valiant Exact Depth-Halving Power Identity (Baton #014)**: `valiant_depth_halving_power` (`[propext]` only), `pow_two_pos`, and `valiant_depth_halving_div`.
4. **Schuler Width-Splitting Monotonicity (Baton #014)**: `schuler_split_monotonicity` (**0 axioms**), `schuler_right_branch_var_drop`, `schuler_branch_step_bound`, `pow_two_mono`, and `schuler_leaf_pow_mono`.

## 2. Exact Walls / Limitations Encountered

### Wall 1 — Local vs CI Lean Toolchain Version (`v4.36.0-rc2` Local vs `v4.12.0` CI)
- **Point of friction**: As documented in Baton #015, this local host has `leanprover/lean4:v4.36.0-rc2` installed under `elan`, while GitHub Actions `lean4-kernel-gate` builds against `leanprover/lean4:v4.12.0`.
- **Mitigation & Verification**:
  - Every single tactic and `Init` lemma used in `ValiantAndAlgebrization.lean` (`Bool`, `xor`, `Fin`, `Nat.decLt`, `Nat.decLe`, `Nat.mul_div_le`, `Nat.div_add_mod`, `Nat.mod_lt`, `Nat.mul_add`, `Nat.succ_mul`, `Nat.mul_succ`, `Nat.mul_zero`, `Nat.zero_mul`, `Nat.mul_le_mul_left`, `Nat.mul_le_mul_right`, `Nat.pow_add`, `Nat.pow_succ`, `Nat.add_sub_of_le`, `omega`) was audited for unchanged signatures across Lean 4.12.0 through 4.36.0-rc2.
  - Avoided `dite`/`dif_pos`/`dite_eq_left`/`reduceDIte` and version-fragile division-cancellation lemma names by proving `valiant_depth_halving_div` and `valiant_iterated_cut_budget_div` directly from `Nat.div_add_mod` + `Nat.mod_lt` + `Nat.decLe`/`Nat.decLt` + `omega`.
  - `verify_baton_019_lean4_valiant_frobenius.py` automatically deletes any locally generated `lake-manifest.json` after `lake build`, preventing toolchain-manifest drift in CI.

### Wall 2 — Foundational Infrastructure Does Not Resolve P vs NP
- **Point of failure relative to Millennium target**: Machine-checking $\mathbb{F}_2$ Frobenius algebra, Valiant's multi-round edge-cut/depth-halving arithmetic, and Schuler's branching monotonicity strengthens the formal backbone of Batons #012, #014, and #015, but does not resolve the open walls blocking $\text{P} \neq \text{NP}$ (specifically: DAG $\text{Res}(\oplus)$ / $\text{AC}^0[2]$-Frege size lower bounds, polynomial-density unbounded-width CNF-SAT-SETH, and Valiant matrix rigidity).
- **Honest Status**: `p_vs_np_resolved: false`.

## 3. Actionable Advice for Future Agents
1. **Compose internally via `import MillenniumRelay.<Module>`**: Importing `MillenniumRelay.ProofComplexityPHP` inside `ValiantAndAlgebrization.lean` allowed direct reuse of `sumFinNat` and `valiant_msb_halving_step` without namespace collisions, while keeping zero external dependencies. Future Module #4 files can import both modules cleanly.
2. **Audit `#print axioms` automatically in every formalization verifier**: Feeding `#print axioms <thm>` to `lean --stdin` (with `LEAN_PATH=.lake/build/lib/lean`) catches hidden `Classical.choice` or `sorryAx` regressions deterministically.
3. **Keep `ValiantAndAlgebrization.lean` comment-hygiene strict**: Note that `TseitinDichotomy.lean` mentions `Mathlib` inside a doc comment, so cross-file hygiene scripts should forbid `import Mathlib` in raw text across all files and forbid bare `Mathlib` in comment-stripped code (and in raw text of new modules).
4. **High-value next formalizations**: Connect `valiant_iterated_msb_existence` and `valiant_depth_halving_power` to an explicit `Fin (2 ^ r)`-leveled DAG longest-path theorem, or lift `f2_frobenius_xorFin_sq` to multilinear $\mathbb{F}_2$ polynomial ideals to machine-check Baton #012's full degree-invariance theorem.
