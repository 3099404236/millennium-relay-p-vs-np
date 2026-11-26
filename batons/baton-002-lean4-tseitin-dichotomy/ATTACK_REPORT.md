# Baton #002: Zero-`sorry` Lean 4 Core Formalization of the Tseitin–ETH Scaling Obstruction

- **Target Millennium Problem**: P versus NP (Clay Mathematics Institute — **Unsolved**)
- **Baton ID**: `baton-002`
- **Node ID**: `baton-002-lean4-tseitin-dichotomy`
- **Status**: `VERIFIED_STATIC_READY_FOR_LEAN_CI` (Eliminated both `sorry` placeholders in `formal/lean4/MillenniumRelay/TseitinDichotomy.lean` using Lean 4.12.0 core primitives with zero Mathlib imports and zero custom axioms; added `lean-toolchain` and `lakefile.toml`; statically audited and exhaustively verified via `verification/verify_baton_002_lean_proof.py`. **Transparency notice**: Lean/Lake binaries are not installed on this local host, so kernel-level `lake build` execution is deferred to Lean CI / `elan`.)
- **P vs NP Resolved?**: **NO** (`p_vs_np_resolved: false`)

---

## 1. Objective & Statement Immutability Compliance

Baton #001 established the **Tseitin–ETH Scaling Dichotomy** (pruning black-box Tseitin reductions from polynomial-size Boolean circuits to sub-exponential $3\text{-SAT}$ algorithms) and froze two immutable target statements in `formal/lean4/MillenniumRelay/TseitinDichotomy.lean`.

Per `PROTOCOL.md` Rule 2 (**Immutable Target Statements**), Baton #002 preserves every type definition (`GateOp`, `Gate`, `Circuit`), helper function (`tseitinVarCount`, `tseitinClauseUpperBound`), and both theorem signatures **byte-for-byte without modification**:

1. **Statement 1 (`tseitin_clause_bound_linear`)**:
   ```lean
   theorem tseitin_clause_bound_linear (c : Circuit) :
       tseitinClauseUpperBound c = 4 * (tseitinVarCount c - c.nInputs) + 1
   ```
2. **Statement 2 (`tseitin_poly_scaling_obstruction`)**:
   ```lean
   theorem tseitin_poly_scaling_obstruction
       (n k g : Nat) (hn : n ≥ 1) (hk : k ≥ 1) (hg : g ≥ 1)
       (hbeat : (n + n ^ k) ≤ n * g) :
       n ^ (k - 1) ≤ g
   ```

---

## 2. Rigorous Mathematical Derivation & Lean 4.12 Core Proof Trace

Both proofs rely **exclusively** on Lean 4.12.0 core (`Init`) — zero Mathlib imports, zero custom axioms, zero `sorry`/`admit`/`unsafe` escapes.

### 2.1 Theorem 1: `tseitin_clause_bound_linear`

**Mathematical proof**:
By definition, for any circuit $c$ with $n = c.\mathrm{nInputs}$ inputs and $s = c.\mathrm{gates.length}$ fan-in-2 gates:
- $\mathrm{tseitinVarCount}(c) = n + s$,
- $\mathrm{tseitinClauseUpperBound}(c) = 4s + 1$.

In truncated natural-number arithmetic ($\mathbb{N}$), $(n + s) - n = s$ holds unconditionally for all $n, s \in \mathbb{N}$ (`Nat.add_sub_cancel_left`). Substituting into the right-hand side gives:
$$4 \cdot ((n + s) - n) + 1 = 4s + 1 = \mathrm{tseitinClauseUpperBound}(c).$$

**Lean 4.12 core discharge**:
```lean
  simp only [tseitinClauseUpperBound, tseitinVarCount, Nat.add_sub_cancel_left]
```
- Uses `Nat.add_sub_cancel_left (n m : Nat) : n + m - n = m` from `Init.Data.Nat.Basic`.
- Closes by reflexivity (`rfl`) after unfolding the two local definitions and cancelling `c.nInputs`.

### 2.2 Theorem 2: `tseitin_poly_scaling_obstruction`

**Complexity-theoretic meaning**:
Suppose a black-box Tseitin reduction converts an $n$-input, $s(n) = n^k$-gate Boolean circuit into a $3\text{-CNF}$ on $m = n + n^k$ variables, and a $3\text{-SAT}$ algorithm runs in time $\exp(m / g(m))$. To beat $2^n$ brute force (up to the constant $\ln 2$ factor normalized into $g$), the scaled exponent satisfies $(n + n^k) / g \le n$, i.e. $n + n^k \le n \cdot g$ over $\mathbb{N}$. Theorem 2 proves this forces $g \ge n^{k-1} = \Theta(m^{1 - 1/k})$, hence $m / g(m) \le O(m^{1/k})$ for every fixed polynomial degree $k \ge 1$.

**Algebraic proof & line-by-line Lean 4.12 kernel correspondence**:
Perform case analysis on $k \in \mathbb{N}$ (`cases k with`):

1. **Case $k = 0$ (`| zero =>`)**:
   Contradicts hypothesis $h_k : 0 \ge 1$ (i.e., $1 \le 0$). Discharged immediately by core `omega` (`Init.Omega`).
2. **Case $k = m + 1$ (`| succ m =>`)**:
   The target $n^{(m+1) - 1} \le g$ reduces definitionally in the Lean 4 kernel to $n^m \le g$ (since `Nat.sub (Nat.succ m) 1 ≡ m`).
   - **Step `h1`**: Since $n \ge 0$ in $\mathbb{N}$,
     $$n^{m+1} \le n + n^{m+1}$$
     by `Nat.le_add_left (n ^ (m + 1)) n` (`Init.Data.Nat.Basic`: `n ≤ m + n`).
   - **Step `h2`**: By transitivity (`Nat.le_trans h1 hbeat`) with $h_{\text{beat}} : n + n^{m+1} \le n \cdot g$,
     $$n^{m+1} \le n \cdot g.$$
   - **Step `h3`**: By `Nat.pow_succ : n ^ (m + 1) = n ^ m * n` and `Nat.mul_comm : n * n ^ m = n ^ m * n`,
     $$n \cdot n^m = n^m \cdot n = n^{m+1} \le n \cdot g.$$
   - **Step `h4` (Conclusion)**: Since $h_n : n \ge 1$ is definitionally $0 < n$ (`Nat.le (Nat.succ 0) n`), left-cancellation of a positive factor via `Nat.le_of_mul_le_mul_left h3 hn` (`{a b c : Nat} (h : c * a ≤ c * b) (hc : 0 < c) : a ≤ b`) yields:
     $$n^m \le g. \qquad \square$$

**Sharpness & Redundancy Remarks**:
- **Sharpness**: Because $n + n^{m+1} = n \cdot (n^m + 1)$, the hypothesis $n + n^k \le n \cdot g$ actually implies the slightly stronger bound $n^{k-1} + 1 \le g$, attained with exact equality at $g = n^{k-1} + 1$. Thus the formalized bound $n^{k-1} \le g$ is tight up to an additive $+1$.
- **Hypothesis `hg : g ≥ 1`**: Technically redundant (since $n \cdot 1 = n \le n + n^k \le n \cdot g$ already forces $g \ge 1$ when $n \ge 1$), but retained verbatim in the signature to uphold statement immutability.

---

## 3. Lean 4 Packaging & Verification Summary

- **`formal/lean4/lean-toolchain`**: Pinned to `leanprover/lean4:v4.12.0`.
- **`formal/lean4/lakefile.toml`**: Declares `[[lean_lib]] name = "MillenniumRelay"` with `roots = ["MillenniumRelay.TseitinDichotomy"]` and `defaultTargets = ["MillenniumRelay"]`, requiring zero external packages (`lake build` completes offline once Lean v4.12.0 is installed).
- **`verification/verify_baton_002_lean_proof.py`**:
  1. Verifies zero occurrences of `sorry`, `admit`, `axiom`, `unsafe`, `partial`, `implemented_by`, or `import Mathlib` in both raw and comment-stripped Lean source.
  2. Verifies exact immutability of both Baton #001 theorem signatures and all core definitions.
  3. Parses `formal/lean4/lakefile.toml` with Python 3.12 stdlib `tomllib` and validates module root resolution.
  4. Exhaustively verifies Theorem 1 across $10{,}201$ `(nInputs, gateCount)` pairs ($0 \le n, s \le 100$).
  5. Exhaustively verifies Theorem 2 and every intermediate Lean proof step (`h1`–`h4`) across $320{,}000$ triples ($n \in [1, 20], k \in [1, 8], g \in [1, 2000]$), confirming 0 counterexamples and exact boundary tightness at $g = n^{k-1} + 1$.
  6. Automatically invokes `lake build` when `lake` is available on `PATH`, and honestly reports `[INFO]` on hosts without Lean installed.

---

## 4. Mandatory 4-Barrier Audit

Because Baton #002 formalizes a **negative obstruction** (pruning black-box Tseitin reductions to $3\text{-SAT}$) rather than proposing a positive proof of $\text{P} \neq \text{NP}$ or $\text{P} = \text{NP}$, it does not claim to break any separation barrier; instead, it locks in a verified quantitative wall that downstream attacks must circumvent:

| Barrier | Reference | Relevance to Baton #002 | Status |
| :--- | :--- | :--- | :--- |
| **1. Relativization** | Baker–Gill–Solovay (1975) | Not applicable as an attack route — Theorem 2 is an unconditional arithmetic obstruction on Tseitin variable blowup $m = n + s$, independent of oracles. | **N/A (Meta-obstruction)**; downstream `baton-003` uses non-relativizing Williams PCP/easy-witness bridge |
| **2. Natural Proofs** | Razborov–Rudich (1997) | Formalization proves a scaling impossibility for black-box reductions; does not construct a natural combinatorial property of Boolean functions. | **N/A (Meta-obstruction)**; preserved for `baton-003`/`baton-004` |
| **3. Algebrization** | Aaronson–Wigderson (2009) | Purely elementary $\mathbb{N}$-inequality on circuit-to-CNF encoding overhead; does not rely on low-degree oracle extensions. | **N/A (Meta-obstruction)**; active filter for `baton-005` (GCT) |
| **4. Locality Barrier** | CHOPRS (STOC 2020) | Confirms black-box Tseitin cannot supply $N^{1+\epsilon}$ lower bounds to magnification without collapsing $3\text{-SAT}$ to $2^{m^\epsilon}$; leaves the CHOPRS locality barrier intact on Route 1B. | **Unchanged (Active Blocker on Route 1B)**; handed off to `baton-004` |

---

## 5. Handoff to Downstream Batons

1. **Lean CI Activation (Repo Maintainer / Relay Gate Follow-up)**:
   Once `baton-002`'s `node_patch.json` is merged into `roadmap.json`, add a Lean CI job to `.github/workflows/relay-gate.yml` running `elan` + `lake build` in `formal/lean4/` so the proof becomes kernel-checked on every commit.
2. **Optional Formalization Child Node (Real-Analytic Dichotomy)**:
   If a future formalizer wants the full real-analytic statement $T(m) = \exp(m / g(m)) \le 2^n \implies g(m) = \Omega(m^{1-1/k})$ (including $\ln 2$ and asymptotic `Filter.Tendsto`), create a *new* Mathlib-backed child module (e.g., `MillenniumRelay/TseitinDichotomyAsymptotic.lean`) without touching the zero-dependency core module `TseitinDichotomy.lean`.
3. **Active Attack Frontiers**:
   - **`baton-003-direct-tc0-sat`**: Avoid Tseitin variable blowup entirely via structure-preserving $\text{TC}^0\text{-SAT}$ algorithms operating directly on $n$ input variables.
   - **`baton-004-nonlocal-magnification`**: Investigate non-local hardness magnification / Hirahara non-black-box meta-complexity reductions bypassing CHOPRS (2020).
   - **`baton-005-gct-obstructions`**: Build reproducible Kronecker/plethysm multiplicity-obstruction tests for GCT.
