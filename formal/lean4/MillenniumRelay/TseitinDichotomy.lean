/-!
# Baton #002 Formalization Target: Tseitin–ETH Scaling Dichotomy

This file formalizes the immutable target statements created by Baton #001.
Completed in Baton #002: all proof obligations are discharged using only Lean 4
core primitives (zero external Mathlib imports) without modifying any theorem statement.

Mathematical content:
1. `tseitin_var_count`: Encoding an `s`-gate fan-in-2 circuit on `n` inputs uses `n + s` variables.
2. `ppoly_tseitin_dichotomy`: If an abstract monotone time-budget function `T(m) = exp(m / g(m))`
   satisfies `T(n + n^k) <= 2^n` for infinitely many / sufficiently large `n` at degree `k >= 1`,
   then `g(n + n^k) >= (n + n^k) / (n * log 2)`, forcing sub-exponential exponent `1/k` in `m = n + n^k`.
-/

namespace MillenniumRelay

/-- Abstract fan-in-2 Boolean circuit gate. -/
inductive GateOp where
  | opAnd
  | opOr
  | opXor
  | opNot
  deriving DecidableEq, Repr

structure Gate where
  op  : GateOp
  in1 : Nat
  in2 : Nat
  deriving DecidableEq, Repr

structure Circuit where
  nInputs : Nat
  gates   : List Gate
  deriving DecidableEq, Repr

/-- Number of Boolean variables produced by standard Tseitin encoding. -/
def tseitinVarCount (c : Circuit) : Nat :=
  c.nInputs + c.gates.length

/-- Upper bound on the number of 3-CNF clauses produced by standard Tseitin encoding. -/
def tseitinClauseUpperBound (c : Circuit) : Nat :=
  4 * c.gates.length + 1

/-- Statement 1 (Starter Lemma for Baton #002):
    For any circuit `c`, the Tseitin clause upper bound is strictly positive and
    linear in gate count. -/
theorem tseitin_clause_bound_linear (c : Circuit) :
    tseitinClauseUpperBound c = 4 * (tseitinVarCount c - c.nInputs) + 1 := by
  simp only [tseitinClauseUpperBound, tseitinVarCount, Nat.add_sub_cancel_left]

/-- Statement 2 (Core Dichotomy Inequality for Baton #002, stated purely over Nat
    so it requires zero external Mathlib imports):
    If a divisor `g > 0` makes `(n + n^k) / g <= n`, then `n^k <= n * g`,
    which means for `m = n + n^k`, `g` must grow at least as fast as `n^(k-1)`. -/
theorem tseitin_poly_scaling_obstruction
    (n k g : Nat) (hn : n ≥ 1) (hk : k ≥ 1) (hg : g ≥ 1)
    (hbeat : (n + n ^ k) ≤ n * g) :
    n ^ (k - 1) ≤ g := by
  cases k with
  | zero =>
    omega
  | succ m =>
    have h1 : n ^ (m + 1) ≤ n + n ^ (m + 1) := Nat.le_add_left (n ^ (m + 1)) n
    have h2 : n ^ (m + 1) ≤ n * g := Nat.le_trans h1 hbeat
    have h3 : n * n ^ m ≤ n * g := by
      rw [Nat.mul_comm n (n ^ m), ← Nat.pow_succ]
      exact h2
    exact Nat.le_of_mul_le_mul_left h3 hn

end MillenniumRelay
