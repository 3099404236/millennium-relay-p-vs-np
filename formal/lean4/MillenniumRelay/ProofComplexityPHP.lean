/-!
# Baton #015 Formalization Target: Pigeonhole Principle, Cutting Planes & Valiant Depth-Reduction

This file expands the zero-dependency Lean 4.12 core formal library (`MillenniumRelay`) with
machine-checked proofs of three foundational theorems from the P vs NP relay:

1. `pigeonhole_no_injection`:
   No injective function `f : Fin (n + 1) → Fin n` exists (combinatorial PHP_{n}^{n+1}).
2. `cutting_planes_php_contradiction` (plus `chvatal_gomory_hole_step`):
   The Cutting Planes integer-sum core contradiction for PHP_{n}^{n+1}: if an integer matrix
   `x : Fin (n + 1) → Fin n → Int` has every pigeon row sum `≥ 1` and every hole column sum `≤ 1`,
   then `False`, together with the Chvátal–Gomory rounding step `k * S ≤ 2 * k - 1 → S ≤ 1`.
3. `valiant_msb_halving_step`:
   The core averaging inequality of Valiant's depth-reduction MSB-bucket halving step:
   if `E` edges of a DAG are partitioned into `k ≥ 1` buckets summing to `E`, some bucket
   has size `≤ E / k`.

Pure Lean 4.12 core (`Init` only): zero external imports, zero unfinished obligations,
zero custom postulates, and zero classical choice.
-/

namespace MillenniumRelay

/-! ## Section 1: Combinatorial Pigeonhole Principle (`pigeonhole_no_injection`) -/

/-- No injective function maps `Fin (n + 1)` into `Fin n`.
    Constructive inductive proof using only Lean 4 core primitives (zero classical choice). -/
theorem pigeonhole_no_injection :
    ∀ (n : Nat) (f : Fin (n + 1) → Fin n),
      (∀ a b : Fin (n + 1), f a = f b → a = b) → False
  | 0, f, _ =>
    Fin.elim0 (f ⟨0, Nat.zero_lt_succ 0⟩)
  | n + 1, f, hf => by
    let last : Fin (n + 2) := ⟨n + 1, Nat.lt_succ_self (n + 1)⟩
    match Nat.decEq (f last).val n with
    | isTrue hlast =>
      -- Case 1: The last pigeon maps to hole `n`.
      -- Restricting `f` to `0 .. n` avoids hole `n`, yielding an injection `Fin (n + 1) → Fin n`.
      let g : Fin (n + 1) → Fin n := fun i =>
        let i' : Fin (n + 2) := ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩
        ⟨(f i').val, by
          have hlt : (f i').val < n + 1 := (f i').isLt
          have hne : (f i').val ≠ n := by
            intro heq
            have hfeq : f i' = f last := Fin.ext (by omega)
            have hieq : i' = last := hf i' last hfeq
            have hval : i.val = n + 1 := congrArg (fun x : Fin (n + 2) => x.val) hieq
            have hi : i.val < n + 1 := i.isLt
            omega
          omega⟩
      refine pigeonhole_no_injection n g ?_
      intro a b hab
      have hval : (g a).val = (g b).val := congrArg (fun x : Fin n => x.val) hab
      dsimp only [g] at hval
      have hfeq : f ⟨a.val, Nat.lt_succ_of_lt a.isLt⟩ =
                  f ⟨b.val, Nat.lt_succ_of_lt b.isLt⟩ := Fin.ext hval
      have heq := hf ⟨a.val, Nat.lt_succ_of_lt a.isLt⟩ ⟨b.val, Nat.lt_succ_of_lt b.isLt⟩ hfeq
      exact Fin.ext (congrArg (fun x : Fin (n + 2) => x.val) heq)
    | isFalse hlast =>
      -- Case 2: The last pigeon maps to a hole `< n`.
      -- Redirect whichever pigeon (if any) hits hole `n` into hole `(f last).val`.
      have hlast_lt : (f last).val < n := by
        have hlt : (f last).val < n + 1 := (f last).isLt
        omega
      let g : Fin (n + 1) → Fin n := fun i =>
        let i' : Fin (n + 2) := ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩
        match Nat.decEq (f i').val n with
        | isTrue _ => ⟨(f last).val, hlast_lt⟩
        | isFalse hne => ⟨(f i').val, by have hlt : (f i').val < n + 1 := (f i').isLt; omega⟩
      refine pigeonhole_no_injection n g ?_
      intro a b hab
      let a' : Fin (n + 2) := ⟨a.val, Nat.lt_succ_of_lt a.isLt⟩
      let b' : Fin (n + 2) := ⟨b.val, Nat.lt_succ_of_lt b.isLt⟩
      have hval : (g a).val = (g b).val := congrArg (fun x : Fin n => x.val) hab
      dsimp only [g] at hval
      cases ha : Nat.decEq (f a').val n with
      | isTrue hfa =>
        cases hb : Nat.decEq (f b').val n with
        | isTrue hfb =>
          have hfeq : f a' = f b' := Fin.ext (by omega)
          have heq : a' = b' := hf a' b' hfeq
          exact Fin.ext (congrArg (fun x : Fin (n + 2) => x.val) heq)
        | isFalse _hfb =>
          simp only [a', b'] at ha hb
          rw [ha, hb] at hval
          dsimp only at hval
          have hfeq : f last = f b' := Fin.ext hval
          have heq : last = b' := hf last b' hfeq
          have hcontra : n + 1 = b.val := congrArg (fun x : Fin (n + 2) => x.val) heq
          have hblt : b.val < n + 1 := b.isLt
          omega
      | isFalse _hfa =>
        cases hb : Nat.decEq (f b').val n with
        | isTrue _hfb =>
          simp only [a', b'] at ha hb
          rw [ha, hb] at hval
          dsimp only at hval
          have hfeq : f a' = f last := Fin.ext hval
          have heq : a' = last := hf a' last hfeq
          have hcontra : a.val = n + 1 := congrArg (fun x : Fin (n + 2) => x.val) heq
          have halt : a.val < n + 1 := a.isLt
          omega
        | isFalse _hfb =>
          simp only [a', b'] at ha hb
          rw [ha, hb] at hval
          dsimp only at hval
          have hfeq : f a' = f b' := Fin.ext hval
          have heq : a' = b' := hf a' b' hfeq
          exact Fin.ext (congrArg (fun x : Fin (n + 2) => x.val) heq)

/-! ## Section 2: Cutting Planes Integer-Sum PHP Contradiction -/

/-- Finite integer sum over `Fin n`: `∑_{i=0}^{n-1} f i`. -/
def sumFin : (n : Nat) → (Fin n → Int) → Int
  | 0, _ => 0
  | n + 1, f =>
    sumFin n (fun i => f ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩) + f ⟨n, Nat.lt_succ_self n⟩

/-- Summing zeros over `Fin n` equals `0`. -/
theorem sumFin_zero : ∀ (n : Nat), sumFin n (fun _ => (0 : Int)) = 0
  | 0 => rfl
  | n + 1 => by
    simp only [sumFin]
    rw [sumFin_zero n]
    omega

/-- Summing `1` over `Fin n` equals `Int.ofNat n`. -/
theorem sumFin_const_one : ∀ (n : Nat), sumFin n (fun _ => (1 : Int)) = Int.ofNat n
  | 0 => rfl
  | n + 1 => by
    simp only [sumFin]
    rw [sumFin_const_one n]
    rfl

/-- Additivity of `sumFin`. -/
theorem sumFin_add : ∀ (n : Nat) (f g : Fin n → Int),
    sumFin n (fun i => f i + g i) = sumFin n f + sumFin n g
  | 0, _, _ => rfl
  | n + 1, f, g => by
    simp only [sumFin]
    rw [sumFin_add n]
    omega

/-- Pointwise monotonicity of `sumFin`. -/
theorem sumFin_mono : ∀ (n : Nat) (f g : Fin n → Int),
    (∀ i : Fin n, f i ≤ g i) → sumFin n f ≤ sumFin n g
  | 0, _, _, _ => Int.le_refl 0
  | n + 1, f, g, h => by
    simp only [sumFin]
    have ih := sumFin_mono n
      (fun i => f ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)
      (fun i => g ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)
      (fun i => h ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)
    have hlast := h ⟨n, Nat.lt_succ_self n⟩
    omega

/-- Exchanging the order of summation in a finite `m × n` integer double sum. -/
theorem sumFin_swap : ∀ (m n : Nat) (x : Fin m → Fin n → Int),
    sumFin m (fun i => sumFin n (fun j => x i j)) =
    sumFin n (fun j => sumFin m (fun i => x i j))
  | 0, n, _ => by
    simp only [sumFin]
    exact (sumFin_zero n).symm
  | m + 1, n, x => by
    simp only [sumFin]
    rw [sumFin_swap m n (fun i j => x ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩ j)]
    rw [← sumFin_add n]

/-- Cutting Planes integer-sum core contradiction for `PHP_n^{n+1}`:
    no integer matrix `x : Fin (n + 1) → Fin n → Int` can have every pigeon row sum `≥ 1`
    and every hole column sum `≤ 1` (yielding `n + 1 ≤ total ≤ n`, hence `False`). -/
theorem cutting_planes_php_contradiction
    (n : Nat) (x : Fin (n + 1) → Fin n → Int)
    (hpigeon : ∀ i : Fin (n + 1), (1 : Int) ≤ sumFin n (fun j => x i j))
    (hhole : ∀ j : Fin n, sumFin (n + 1) (fun i => x i j) ≤ (1 : Int)) :
    False := by
  have hlow := sumFin_mono (n + 1) (fun _ => (1 : Int))
    (fun i => sumFin n (fun j => x i j)) hpigeon
  rw [sumFin_const_one (n + 1)] at hlow
  have hhigh := sumFin_mono n
    (fun j => sumFin (n + 1) (fun i => x i j)) (fun _ => (1 : Int)) hhole
  rw [sumFin_const_one n] at hhigh
  have hswap := sumFin_swap (n + 1) n x
  have hsucc : Int.ofNat (n + 1) = Int.ofNat n + 1 := rfl
  omega

/-- Auxiliary monotonicity bound over `Int` for `chvatal_gomory_hole_step`. -/
theorem int_two_mul_ofNat_le_mul :
    ∀ (k : Nat) (S : Int), (2 : Int) ≤ S → 2 * Int.ofNat k ≤ Int.ofNat k * S
  | 0, _, _ => by
    have h0 : Int.ofNat 0 = 0 := rfl
    rw [h0, Int.zero_mul]
    omega
  | k + 1, S, hS => by
    have ih := int_two_mul_ofNat_le_mul k S hS
    have hsucc : Int.ofNat (k + 1) = Int.ofNat k + 1 := rfl
    rw [hsucc, Int.add_mul, Int.one_mul]
    omega

/-- Chvátal–Gomory division/rounding step from Cook–Coullard–Turán's `O(n^3)` Cutting Planes
    refutation of `PHP_n^{n+1}`: if `k * S ≤ 2 * k - 1` for an integer `S`,
    then integer rounding forces `S ≤ 1`. -/
theorem chvatal_gomory_hole_step
    (k : Nat) (S : Int)
    (hle : Int.ofNat k * S ≤ 2 * Int.ofNat k - 1) :
    S ≤ 1 := by
  match Int.decLe S 1 with
  | isTrue h => exact h
  | isFalse hnot =>
    have hS : (2 : Int) ≤ S := by omega
    have hmul := int_two_mul_ofNat_le_mul k S hS
    omega

/-! ## Section 3: Valiant Depth-Reduction MSB-Bucket Averaging (`valiant_msb_halving_step`) -/

/-- Finite natural-number sum over `Fin k`: `∑_{i=0}^{k-1} b i`. -/
def sumFinNat : (k : Nat) → (Fin k → Nat) → Nat
  | 0, _ => 0
  | k + 1, b =>
    sumFinNat k (fun i => b ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩) + b ⟨k, Nat.lt_succ_self k⟩

/-- If every bucket has size at least `t`, the sum of `k` buckets is at least `k * t`. -/
theorem sumFinNat_ge_mul_of_forall_ge :
    ∀ (k t : Nat) (b : Fin k → Nat),
      (∀ i : Fin k, t ≤ b i) → k * t ≤ sumFinNat k b
  | 0, _, _, _ => by
    simp only [sumFinNat, Nat.zero_mul]
    exact Nat.le_refl 0
  | k + 1, t, b, h => by
    simp only [sumFinNat]
    have ih := sumFinNat_ge_mul_of_forall_ge k t
      (fun i => b ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)
      (fun i => h ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩)
    have hlast := h ⟨k, Nat.lt_succ_self k⟩
    rw [Nat.succ_mul]
    omega

/-- Constructive dichotomy over `Fin k`: either some bucket is `≤ t`, or all buckets are `≥ t + 1`. -/
theorem exists_le_or_forall_gt :
    ∀ (k t : Nat) (b : Fin k → Nat),
      (∃ i : Fin k, b i ≤ t) ∨ (∀ i : Fin k, t + 1 ≤ b i)
  | 0, _, _ => Or.inr (fun i => Fin.elim0 i)
  | k + 1, t, b => by
    cases exists_le_or_forall_gt k t (fun i => b ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩) with
    | inl hex =>
      cases hex with
      | intro i hi =>
        exact Or.inl ⟨⟨i.val, Nat.lt_succ_of_lt i.isLt⟩, hi⟩
    | inr hall =>
      match Nat.decLe (b ⟨k, Nat.lt_succ_self k⟩) t with
      | isTrue hle =>
        exact Or.inl ⟨⟨k, Nat.lt_succ_self k⟩, hle⟩
      | isFalse hgt =>
        refine Or.inr (fun j => ?_)
        match Nat.decLt j.val k with
        | isTrue hlt =>
          exact hall ⟨j.val, hlt⟩
        | isFalse hge =>
          have hjval : j.val = k := by
            have hjlt : j.val < k + 1 := j.isLt
            omega
          have hjeq : j = ⟨k, Nat.lt_succ_self k⟩ := Fin.ext hjval
          rw [hjeq]
          omega

/-- Core arithmetic averaging inequality of Valiant's depth-reduction MSB-bucket halving step:
    if `E` edges of a DAG are partitioned into `k ≥ 1` buckets whose sizes sum to `E`,
    then there exists a bucket of size `≤ E / k`. -/
theorem valiant_msb_halving_step
    (k E : Nat) (hk : k ≥ 1) (b : Fin k → Nat) (hsum : sumFinNat k b = E) :
    ∃ i : Fin k, b i ≤ E / k := by
  cases exists_le_or_forall_gt k (E / k) b with
  | inl hex => exact hex
  | inr hall =>
    have hge : k * (E / k + 1) ≤ sumFinNat k b :=
      sumFinNat_ge_mul_of_forall_ge k (E / k + 1) b hall
    have hdiv : k * (E / k) + E % k = E := Nat.div_add_mod E k
    have hmod : E % k < k := Nat.mod_lt E hk
    have hmul : k * (E / k + 1) = k * (E / k) + k := Nat.mul_succ k (E / k)
    omega

end MillenniumRelay
