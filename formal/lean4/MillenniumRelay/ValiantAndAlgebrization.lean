import MillenniumRelay.ProofComplexityPHP

/-!
# Baton #019 Formalization Target: F_2 Frobenius Invariance, Valiant Iterated Cut Budget & Schuler Monotonicity

This module extends the zero-dependency Lean 4.12 core library (`MillenniumRelay`) with
machine-checked constructive proofs of four foundational results from Batons #012, #014, and #015:

1. Characteristic-2 / `F_2` Frobenius & Boolean Ring Identities (`f2_idempotent`,
   `f2_frobenius_add_sq`, `f2_xor_cancel_right`, `f2_frobenius_xorFin_sq`):
   Over `Bool` representing `F_2` (`xor` = addition, `&&` = multiplication), every element is
   multiplicatively idempotent (`a && a = a`), squaring distributes additively
   (`(a + b)^2 = a^2 + b^2`), addition is self-cancelling (`(a + b) + b = a`), and arbitrary-width
   parity linear extensions `xorFin k f` satisfy the characteristic-2 Frobenius identity powering
   Baton #012's Frobenius Linear-Extension Degree Invariance Theorem for Polynomial Calculus over `F_2`.
2. Valiant Iterated Edge-Removal Budget (`valiant_iterated_cut_budget`,
   `valiant_iterated_cut_budget_div`, `valiant_iterated_msb_existence`):
   Composing Baton #015's single-step MSB-bucket halving bound (`valiant_msb_halving_step`) across
   `t` rounds with per-round cut `cut i ≤ E / r` yields the exact total-cut budget
   `r * sumFinNat t cut ≤ t * E` and `sumFinNat t cut ≤ (t * E) / r`.
3. Valiant Exact Depth-Halving Power Identity (`valiant_depth_halving_power`,
   `valiant_depth_halving_div`):
   For `t ≤ r`, `2 ^ t * 2 ^ (r - t) = 2 ^ r` and `2 ^ r / 2 ^ t = 2 ^ (r - t)`, formalizing
   the exact depth reduction factor `d / 2^t` over `Nat`.
4. Schuler Width-Splitting Tree Bound Monotonicity (`schuler_split_monotonicity`,
   `schuler_right_branch_var_drop`, `schuler_branch_step_bound`, `schuler_leaf_pow_mono`):
   Formalizes the clause-count monotonicity `M1 ≤ M2 → M1 * 2 ^ (n - k) ≤ M2 * 2 ^ (n - k)`,
   strict right-branch variable drop `1 ≤ k → n ≥ 1 → n - k < n`, and width-threshold monotonicity
   underlying Baton #014's Ordered Schuler SAT upper bound.

Pure Lean 4.12 core (`Init` + internal `MillenniumRelay.ProofComplexityPHP` only): zero external
libraries, zero unfinished obligations, zero custom postulates, and zero classical choice.
-/

namespace MillenniumRelay

/-! ## Section 1: Characteristic-2 Boolean / `F_2` Frobenius Algebra (Baton #012) -/

/-- Multiplicative idempotence over `F_2` (`Bool`): `a^2 = a`. -/
theorem f2_idempotent : ∀ a : Bool, (a && a) = a
  | false => rfl
  | true  => rfl

/-- Characteristic-2 Frobenius endomorphism over `F_2` (`Bool`): `(a + b)^2 = a^2 + b^2`. -/
theorem f2_frobenius_add_sq :
    ∀ a b : Bool, ((xor a b) && (xor a b)) = xor (a && a) (b && b)
  | false, false => rfl
  | false, true  => rfl
  | true,  false => rfl
  | true,  true  => rfl

/-- Additive self-cancellation over `F_2` (`Bool`): `(a + b) + b = a`. -/
theorem f2_xor_cancel_right : ∀ a b : Bool, xor (xor a b) b = a
  | false, false => rfl
  | false, true  => rfl
  | true,  false => rfl
  | true,  true  => rfl

/-- Characteristic-2 doubling law over `F_2` (`Bool`): `a + a = 0`. -/
theorem f2_xor_self : ∀ a : Bool, xor a a = false
  | false => rfl
  | true  => rfl

/-- Left distributivity of multiplication over addition in `F_2` (`Bool`). -/
theorem f2_and_xor_distrib_left :
    ∀ a b c : Bool, (a && xor b c) = xor (a && b) (a && c)
  | false, false, false => rfl
  | false, false, true  => rfl
  | false, true,  false => rfl
  | false, true,  true  => rfl
  | true,  false, false => rfl
  | true,  false, true  => rfl
  | true,  true,  false => rfl
  | true,  true,  true  => rfl

/-- Finite `F_2`-linear parity sum over `Fin k`: `⨁_{i=0}^{k-1} f i`. -/
def xorFin : (k : Nat) → (Fin k → Bool) → Bool
  | 0, _ => false
  | k + 1, f =>
    xor (xorFin k (fun i => f ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)) (f ⟨k, Nat.lt_succ_self k⟩)

/-- `k`-ary characteristic-2 Frobenius identity over `F_2`:
    `(⨁_{i=0}^{k-1} f i)^2 = ⨁_{i=0}^{k-1} (f i)^2`. -/
theorem f2_frobenius_xorFin_sq :
    ∀ (k : Nat) (f : Fin k → Bool),
      (xorFin k f && xorFin k f) = xorFin k (fun i => f i && f i)
  | 0, _ => rfl
  | k + 1, f => by
    simp only [xorFin]
    rw [f2_frobenius_add_sq]
    rw [f2_frobenius_xorFin_sq k (fun i => f ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)]

/-- Arbitrary-width parity linear extensions `y = ⨁_{i=0}^{k-1} f i` satisfy the Boolean
    idempotence equation `y^2 = y`, the algebraic core of Baton #012's Frobenius
    Linear-Extension Degree Invariance Theorem for Polynomial Calculus over `F_2`. -/
theorem f2_xorFin_idempotent (k : Nat) (f : Fin k → Bool) :
    (xorFin k f && xorFin k f) = xorFin k f :=
  f2_idempotent (xorFin k f)

/-! ## Section 2: Valiant Multi-Step Iterated Cut Budget (Batons #014 & #015) -/

/-- Pointwise congruence for `sumFinNat`. -/
theorem sumFinNat_congr :
    ∀ (k : Nat) (f g : Fin k → Nat),
      (∀ i : Fin k, f i = g i) → sumFinNat k f = sumFinNat k g
  | 0, _, _, _ => rfl
  | k + 1, f, g, h => by
    simp only [sumFinNat]
    have ih := sumFinNat_congr k
      (fun i => f ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)
      (fun i => g ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)
      (fun i => h ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)
    have hlast := h ⟨k, Nat.lt_succ_self k⟩
    omega

/-- Valiant's multi-step edge-removal budget:
    if `t` rounds of MSB bucket-selection each remove `cut i ≤ E / r`, then the total
    removed edges `sumFinNat t cut` satisfy `r * sumFinNat t cut ≤ t * E`. -/
theorem valiant_iterated_cut_budget :
    ∀ (t r E : Nat) (cut : Fin t → Nat),
      (∀ i : Fin t, cut i ≤ E / r) →
      r * sumFinNat t cut ≤ t * E
  | 0, r, E, _, _ => by
    simp only [sumFinNat, Nat.mul_zero, Nat.zero_mul]
    exact Nat.le_refl 0
  | t + 1, r, E, cut, hcut => by
    simp only [sumFinNat]
    have ih := valiant_iterated_cut_budget t r E
      (fun i => cut ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)
      (fun i => hcut ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)
    have hlast : cut ⟨t, Nat.lt_succ_self t⟩ ≤ E / r := hcut ⟨t, Nat.lt_succ_self t⟩
    have hmul : r * cut ⟨t, Nat.lt_succ_self t⟩ ≤ r * (E / r) :=
      Nat.mul_le_mul_left r hlast
    have hdiv : r * (E / r) ≤ E := Nat.mul_div_le E r
    rw [Nat.mul_add, Nat.succ_mul]
    omega

/-- Division form of Valiant's multi-step edge-removal budget:
    for `r ≥ 1`, if each of `t` rounds removes `cut i ≤ E / r`, then
    `sumFinNat t cut ≤ (t * E) / r`. -/
theorem valiant_iterated_cut_budget_div
    (t r E : Nat) (hr : r ≥ 1) (cut : Fin t → Nat)
    (hcut : ∀ i : Fin t, cut i ≤ E / r) :
    sumFinNat t cut ≤ (t * E) / r := by
  have hbud : r * sumFinNat t cut ≤ t * E :=
    valiant_iterated_cut_budget t r E cut hcut
  match Nat.decLe (sumFinNat t cut) ((t * E) / r) with
  | isTrue hle => exact hle
  | isFalse hgt =>
    have hge : (t * E) / r + 1 ≤ sumFinNat t cut := by omega
    have hmul : r * ((t * E) / r + 1) ≤ r * sumFinNat t cut :=
      Nat.mul_le_mul_left r hge
    have hsucc : r * ((t * E) / r + 1) = r * ((t * E) / r) + r :=
      Nat.mul_succ r ((t * E) / r)
    have hdiv : r * ((t * E) / r) + (t * E) % r = t * E :=
      Nat.div_add_mod (t * E) r
    have hmod : (t * E) % r < r := Nat.mod_lt (t * E) hr
    omega

/-- Constructive end-to-end composition of Baton #015's `valiant_msb_halving_step` with
    `valiant_iterated_cut_budget`: given `t` rounds of `r`-bucket partitions (`r ≥ 1`)
    each summing to `E`, there exists a sequence of chosen bucket cuts `cut : Fin t → Nat`
    whose total satisfies `r * sumFinNat t cut ≤ t * E` (constructed with zero choice). -/
theorem valiant_iterated_msb_existence :
    ∀ (t r E : Nat) (_hr : r ≥ 1) (b : Fin t → Fin r → Nat),
      (∀ i : Fin t, sumFinNat r (b i) = E) →
      ∃ cut : Fin t → Nat,
        (∀ i : Fin t, ∃ j : Fin r, cut i = b i j) ∧
        (∀ i : Fin t, cut i ≤ E / r) ∧
        r * sumFinNat t cut ≤ t * E
  | 0, _, _, _, _, _ =>
    ⟨fun i => Fin.elim0 i,
     fun i => Fin.elim0 i,
     fun i => Fin.elim0 i,
     by simp only [sumFinNat, Nat.mul_zero, Nat.zero_mul]; exact Nat.le_refl 0⟩
  | t + 1, r, E, hr, b, hsum => by
    have ih := valiant_iterated_msb_existence t r E hr
      (fun i => b ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)
      (fun i => hsum ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)
    cases ih with
    | intro cutPrev hPrev =>
      cases hPrev with
      | intro hPrevMem hPrevRest =>
        cases hPrevRest with
        | intro hPrevLe _ =>
          have hStep := valiant_msb_halving_step r E hr
            (b ⟨t, Nat.lt_succ_self t⟩) (hsum ⟨t, Nat.lt_succ_self t⟩)
          cases hStep with
          | intro jLast hjLast =>
            let cut : Fin (t + 1) → Nat := fun i =>
              match Nat.decLt i.val t with
              | isTrue hlt => cutPrev ⟨i.val, hlt⟩
              | isFalse _ => b ⟨t, Nat.lt_succ_self t⟩ jLast
            have hMem : ∀ i : Fin (t + 1), ∃ j : Fin r, cut i = b i j := by
              intro i
              dsimp only [cut]
              cases hlt : Nat.decLt i.val t with
              | isTrue hltProof =>
                cases hPrevMem ⟨i.val, hltProof⟩ with
                | intro j hj =>
                  exact ⟨j, hj⟩
              | isFalse _ =>
                dsimp only
                have hival : i.val = t := by
                  have hilt : i.val < t + 1 := i.isLt
                  omega
                have hieq : i = ⟨t, Nat.lt_succ_self t⟩ := Fin.ext hival
                rw [hieq]
                exact ⟨jLast, rfl⟩
            have hLe : ∀ i : Fin (t + 1), cut i ≤ E / r := by
              intro i
              dsimp only [cut]
              cases hlt : Nat.decLt i.val t with
              | isTrue hltProof => exact hPrevLe ⟨i.val, hltProof⟩
              | isFalse _ => exact hjLast
            exact ⟨cut, hMem, hLe, valiant_iterated_cut_budget (t + 1) r E cut hLe⟩

/-! ## Section 3: Valiant Exact Depth-Halving Power Identity (Baton #014) -/

/-- Exact power-of-two depth-halving factorization over `Nat`:
    for `t ≤ r`, `2^t * 2^(r - t) = 2^r` (so `t` halvings reduce depth `2^r` by factor `2^t`
    to `2^(r - t)`). -/
theorem valiant_depth_halving_power (r t : Nat) (h : t ≤ r) :
    2 ^ t * 2 ^ (r - t) = 2 ^ r := by
  rw [← Nat.pow_add, Nat.add_sub_of_le h]

/-- Positivity of powers of two over `Nat`. -/
theorem pow_two_pos : ∀ k : Nat, 0 < 2 ^ k
  | 0 => Nat.lt_succ_self 0
  | k + 1 => by
    have ih := pow_two_pos k
    rw [Nat.pow_succ]
    omega

/-- Exact division form of Valiant's depth halving over `Nat`:
    for `t ≤ r`, `2^r / 2^t = 2^(r - t)`. -/
theorem valiant_depth_halving_div (r t : Nat) (h : t ≤ r) :
    2 ^ r / 2 ^ t = 2 ^ (r - t) := by
  have hpos : 0 < 2 ^ t := pow_two_pos t
  have hpow : 2 ^ t * 2 ^ (r - t) = 2 ^ r := valiant_depth_halving_power r t h
  have hdiv : 2 ^ t * (2 ^ r / 2 ^ t) + 2 ^ r % 2 ^ t = 2 ^ r := Nat.div_add_mod (2 ^ r) (2 ^ t)
  have hmod : 2 ^ r % 2 ^ t < 2 ^ t := Nat.mod_lt (2 ^ r) hpos
  match Nat.decLt (2 ^ r / 2 ^ t) (2 ^ (r - t)) with
  | isTrue hlt =>
    have hle1 : 2 ^ r / 2 ^ t + 1 ≤ 2 ^ (r - t) := by omega
    have hmul : 2 ^ t * (2 ^ r / 2 ^ t + 1) ≤ 2 ^ t * 2 ^ (r - t) :=
      Nat.mul_le_mul_left (2 ^ t) hle1
    have hsucc : 2 ^ t * (2 ^ r / 2 ^ t + 1) = 2 ^ t * (2 ^ r / 2 ^ t) + 2 ^ t :=
      Nat.mul_succ (2 ^ t) (2 ^ r / 2 ^ t)
    omega
  | isFalse hge =>
    match Nat.decLt (2 ^ (r - t)) (2 ^ r / 2 ^ t) with
    | isTrue hgt =>
      have hle2 : 2 ^ (r - t) + 1 ≤ 2 ^ r / 2 ^ t := by omega
      have hmul : 2 ^ t * (2 ^ (r - t) + 1) ≤ 2 ^ t * (2 ^ r / 2 ^ t) :=
        Nat.mul_le_mul_left (2 ^ t) hle2
      have hsucc : 2 ^ t * (2 ^ (r - t) + 1) = 2 ^ t * 2 ^ (r - t) + 2 ^ t :=
        Nat.mul_succ (2 ^ t) (2 ^ (r - t))
      omega
    | isFalse hle => omega

/-! ## Section 4: Schuler Width-Splitting Tree Bound Monotonicity (Baton #014) -/

/-- Clause-count monotonicity of Baton #014's Ordered Schuler width-splitting bound:
    increasing the clause budget `M1 ≤ M2` preserves `M1 * 2^(n - k) ≤ M2 * 2^(n - k)`. -/
theorem schuler_split_monotonicity
    (n k M1 M2 : Nat) (hM : M1 ≤ M2) :
    M1 * 2 ^ (n - k) ≤ M2 * 2 ^ (n - k) :=
  Nat.mul_le_mul_right (2 ^ (n - k)) hM

/-- Strict variable-count drop on every Schuler right branch (falsifying a length-`k` prefix):
    whenever `n ≥ 1` and `1 ≤ k`, the remaining active variable count satisfies `n - k < n`. -/
theorem schuler_right_branch_var_drop
    (n k : Nat) (hn : n ≥ 1) (hk : 1 ≤ k) :
    n - k < n := by
  omega

/-- Combined Schuler right-branch monotonicity and strict variable-drop step bound. -/
theorem schuler_branch_step_bound
    (n k M1 M2 : Nat) (hn : n ≥ 1) (hk : 1 ≤ k) (hM : M1 ≤ M2) :
    M1 * 2 ^ (n - k) ≤ M2 * 2 ^ (n - k) ∧ n - k < n :=
  ⟨schuler_split_monotonicity n k M1 M2 hM, schuler_right_branch_var_drop n k hn hk⟩

/-- Monotonicity of powers of two over `Nat`. -/
theorem pow_two_mono : ∀ (a b : Nat), a ≤ b → 2 ^ a ≤ 2 ^ b
  | a, 0, h => by
    have ha : a = 0 := by omega
    rw [ha]
    exact Nat.le_refl 1
  | a, b + 1, h => by
    match Nat.decLe a b with
    | isTrue hle =>
      have ih := pow_two_mono a b hle
      rw [Nat.pow_succ]
      omega
    | isFalse hgt =>
      have hab : a = b + 1 := by omega
      rw [hab]
      exact Nat.le_refl (2 ^ (b + 1))

/-- Width-threshold monotonicity of Schuler's right-branch leaf space:
    a larger prefix width `k1 ≤ k2` eliminates at least as many variables, yielding
    `2^(n - k2) ≤ 2^(n - k1)`. -/
theorem schuler_leaf_pow_mono (n k1 k2 : Nat) (hk : k1 ≤ k2) :
    2 ^ (n - k2) ≤ 2 ^ (n - k1) := by
  apply pow_two_mono
  omega

end MillenniumRelay
