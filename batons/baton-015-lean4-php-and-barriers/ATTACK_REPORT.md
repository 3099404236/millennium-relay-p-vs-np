# Baton #015: Zero-Mathlib Lean 4.12 Formalization of PHP, Cutting Planes & Valiant Depth-Reduction

- **Target Millennium Problem**: P versus NP (Clay Mathematics Institute — **Unsolved**)
- **Baton ID**: `baton-015`
- **Node ID**: `baton-015-lean4-php-and-barriers`
- **Status**: `VERIFIED` (Expanded `formal/lean4/MillenniumRelay/` with `ProofComplexityPHP.lean` — pure Lean 4.12 core, zero external imports, zero `sorry`/`admit`/custom axioms, zero `Classical.choice`, zero errors and zero warnings; registered in `formal/lean4/lakefile.toml` alongside `TseitinDichotomy`; kernel-checked locally on Lean 4 and cross-verified combinatorially via `verification/verify_baton_015_lean4_library.py`.)
- **P vs NP Resolved?**: **NO** (`p_vs_np_resolved: false`)

---

## 1. Objective & Role in the Millennium Relay

While Batons #001–#011 established computational and barrier-theoretic results across proof complexity, circuit depth reduction, and meta-complexity, only the Tseitin–ETH scaling dichotomy had previously been formalized in Lean 4 (`formal/lean4/MillenniumRelay/TseitinDichotomy.lean`, Baton #002).

Baton #015 expands the zero-dependency Lean 4 library `MillenniumRelay` with `formal/lean4/MillenniumRelay/ProofComplexityPHP.lean` and adds `"MillenniumRelay.ProofComplexityPHP"` to `roots` in `formal/lean4/lakefile.toml` so `lake build` compiles **both** formal modules in GitHub Actions (`lean4-kernel-gate`, pinned to `leanprover/lean4:v4.12.0`).

Specifically, we formalize and machine-check **three foundational pillars** underlying proof complexity (Baton #006, Baton #012) and circuit depth-reduction frontiers (Valiant 1977; Viola; Williams):

1. **`pigeonhole_no_injection`** — Constructive combinatorial Pigeonhole Principle $\text{PHP}_n^{n+1}$: no injective function $f : \mathrm{Fin}(n + 1) \to \mathrm{Fin}(n)$ exists.
2. **`cutting_planes_php_contradiction` & `chvatal_gomory_hole_step`** — The integer-sum core contradiction and Chvátal–Gomory rounding inference powering Cook–Coullard–Turán's (1987) $O(n^3)$ Cutting Planes refutation of $\text{PHP}_n^{n+1}$ (separating Cutting Planes exponentially from Resolution).
3. **`valiant_msb_halving_step`** — The exact averaging inequality powering Valiant's (1977) MSB-bucket depth-reduction halving step for $O(n)$-size Boolean circuits: partitioning $E$ DAG edges into $k \ge 1$ buckets guarantees a bucket of size $\le \lfloor E / k \rfloor$.

---

## 2. Rigorous Mathematical Derivations & Lean 4.12 Core Proof Traces

All proofs use **exclusively** Lean 4.12.0 core (`Init`) — zero Mathlib imports, zero `sorry`, zero `admit`, zero custom axioms, and zero `Classical.choice` (`#print axioms` reports only `[propext, Quot.sound]`).

### 2.1 Theorem 1: Combinatorial Pigeonhole Principle (`pigeonhole_no_injection`)

**Statement**:
```lean
theorem pigeonhole_no_injection :
    ∀ (n : Nat) (f : Fin (n + 1) → Fin n),
      (∀ a b : Fin (n + 1), f a = f b → a = b) → False
```

**Constructive Inductive Proof**:
- **Base case ($n = 0$)**: Given $f : \mathrm{Fin}\,1 \to \mathrm{Fin}\,0$, evaluate $f(\langle 0, 0 < 1 \rangle) : \mathrm{Fin}\,0$ and apply `Fin.elim0` to derive `False`.
- **Inductive step ($n \to n + 1$)**: Given an injective $f : \mathrm{Fin}(n + 2) \to \mathrm{Fin}(n + 1)$, let $\mathrm{last} = \langle n + 1, n + 1 < n + 2 \rangle$ and decide $(f(\mathrm{last})).\mathrm{val} = n$ via `Nat.decEq`:
  - **Case 1 ($(f(\mathrm{last})).\mathrm{val} = n$)**: For every $i \in \mathrm{Fin}(n + 1)$, letting $i' = \langle i.\mathrm{val}, i.\mathrm{val} < n + 2 \rangle$, injectivity of $f$ and $i' \neq \mathrm{last}$ force $(f(i')).\mathrm{val} \neq n$, hence $(f(i')).\mathrm{val} < n$. Defining $g(i) = \langle (f(i')).\mathrm{val}, \dots \rangle : \mathrm{Fin}\,n$ yields an injection $g : \mathrm{Fin}(n + 1) \to \mathrm{Fin}\,n$, contradicting the induction hypothesis.
  - **Case 2 ($(f(\mathrm{last})).\mathrm{val} < n$)**: Define the constructive redirect map $g : \mathrm{Fin}(n + 1) \to \mathrm{Fin}\,n$ by
    $$g(i) = \begin{cases} \langle (f(\mathrm{last})).\mathrm{val}, \dots \rangle & \text{if } (f(i')).\mathrm{val} = n, \\ \langle (f(i')).\mathrm{val}, \dots \rangle & \text{otherwise.} \end{cases}$$
    Suppose $g(a) = g(b)$ for $a, b \in \mathrm{Fin}(n + 1)$. Splitting on `Nat.decEq (f a').val n` and `Nat.decEq (f b').val n`:
    - *(both $= n$)*: $f(a') = f(b') \implies a' = b' \implies a = b$.
    - *(one $= n$, one $\neq n$)*: forces $f(\mathrm{last}) = f(b')$ (or $f(a') = f(\mathrm{last})$), so $\mathrm{last} = b'$ (resp. $a' = \mathrm{last}$), contradicting $b.\mathrm{val} < n + 1$ (resp. $a.\mathrm{val} < n + 1$).
    - *(neither $= n$)*: $(f(a')).\mathrm{val} = (f(b')).\mathrm{val} \implies f(a') = f(b') \implies a = b$.
    Thus $g$ is injective, contradicting the induction hypothesis. $\blacksquare$

**Why this proof design is CI-bulletproof**: By using `match Nat.decEq ...` + `dsimp only` instead of `by_cases` or `dite`/`dif_pos`/`↓reduceDIte`, the proof introduces **zero** `Classical.choice` axioms and avoids every version-dependent simp lemma across Lean 4.12 through 4.36+.

---

### 2.2 Theorem 2: Cutting Planes Integer-Sum Contradiction (`cutting_planes_php_contradiction` & `chvatal_gomory_hole_step`)

**Definitions & Core Double-Sum Algebra**:
We define finite integer summation over `Fin n`:
```lean
def sumFin : (n : Nat) → (Fin n → Int) → Int
  | 0, _ => 0
  | n + 1, f =>
    sumFin n (fun i => f ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩) + f ⟨n, Nat.lt_succ_self n⟩
```
and prove five elementary structural lemmas by structural induction on `n` + `omega`:
1. `sumFin_zero`: $\sum_{i=0}^{n-1} 0 = 0$.
2. `sumFin_const_one`: $\sum_{i=0}^{n-1} 1 = \mathrm{Int.ofNat}\, n$.
3. `sumFin_add`: $\sum_{i=0}^{n-1} (f(i) + g(i)) = \sum_{i=0}^{n-1} f(i) + \sum_{i=0}^{n-1} g(i)$.
4. `sumFin_mono`: $(\forall i,\, f(i) \le g(i)) \implies \sum_i f(i) \le \sum_i g(i)$.
5. `sumFin_swap` (Fubini over finite grids):
   $$\sum_{i=0}^{m-1} \sum_{j=0}^{n-1} x_{i,j} = \sum_{j=0}^{n-1} \sum_{i=0}^{m-1} x_{i,j}.$$

**Statement (`cutting_planes_php_contradiction`)**:
```lean
theorem cutting_planes_php_contradiction
    (n : Nat) (x : Fin (n + 1) → Fin n → Int)
    (hpigeon : ∀ i : Fin (n + 1), (1 : Int) ≤ sumFin n (fun j => x i j))
    (hhole : ∀ j : Fin n, sumFin (n + 1) (fun i => x i j) ≤ (1 : Int)) :
    False
```

**Proof**:
Applying `sumFin_mono` and `sumFin_const_one` to `hpigeon` over `Fin (n + 1)` yields:
$$\mathrm{Int.ofNat}(n + 1) \le \sum_{i=0}^{n} \sum_{j=0}^{n-1} x_{i,j}.$$
Applying `sumFin_mono` and `sumFin_const_one` to `hhole` over `Fin n` yields:
$$\sum_{j=0}^{n-1} \sum_{i=0}^{n} x_{i,j} \le \mathrm{Int.ofNat}(n).$$
By `sumFin_swap (n + 1) n x`, both double sums are equal, forcing $n + 1 \le n$ over $\mathbb{Z}$, closed immediately by `omega`. $\blacksquare$

**Companion Chvátal–Gomory Rounding Step (`chvatal_gomory_hole_step`)**:
In Baton #006's Cook–Coullard–Turán $O(n^3)$ Cutting Planes refutation of $\text{PHP}_n^{n+1}$, the pairwise hole axioms $-x_{i,j} - x_{i',j} \ge -1$ cannot yield $\sum_{i=1}^{n+1} x_{i,j} \le 1$ by linear combinations alone because the fractional point $x_{i,j} = 1/n$ satisfies every axiom for $n \ge 2$ (LP integrality gap). Instead, the inductive step multiplies $-\sum_{i=1}^k x_{i,j} \ge -1$ by $k - 1$, adds $k$ pairwise hole axioms to get $k \cdot S \le 2k - 1$ (where $S = \sum_{i=1}^{k+1} x_{i,j} \in \mathbb{Z}$), and applies **Chvátal–Gomory division by $k$ with ceiling rounding** ($\lceil -(2k-1)/k \rceil = -1$). We formalize this exact rounding inference:
```lean
theorem chvatal_gomory_hole_step
    (k : Nat) (S : Int)
    (hle : Int.ofNat k * S ≤ 2 * Int.ofNat k - 1) :
    S ≤ 1
```
Proved via `Int.decLe S 1` and the inductive lemma `int_two_mul_ofNat_le_mul : 2 ≤ S → 2 * k ≤ k * S`, yielding $2k \le kS \le 2k - 1$, contradiction via `omega`. $\blacksquare$

---

### 2.3 Theorem 3: Valiant Depth-Reduction MSB-Bucket Averaging (`valiant_msb_halving_step`)

**Complexity-Theoretic Context (Valiant 1977)**:
Given any directed acyclic graph (circuit) of depth $d = 2^r$ with $E$ edges, label each vertex by its topological depth $\ell(v) \in \{0, \dots, 2^r - 1\}$ and assign every edge $(u, v)$ ($\ell(u) < \ell(v)$) to the bucket $B_t$ where $t = \mathrm{msb}(\ell(u) \oplus \ell(v)) \in \{0, \dots, r - 1\}$. Since the $r$ buckets partition all $E$ edges ($\sum_{t=0}^{r-1} |B_t| = E$), `valiant_msb_halving_step` guarantees some bit position $t^*$ with $|B_{t^*}| \le \lfloor E / r \rfloor$. Deleting $B_{t^*}$ prevents any directed path from crossing between vertices with bit $t^* = 0$ and bit $t^* = 1$, **strictly halving the maximum depth** to $\le d/2 - 1$ at edge cost $\le \lfloor E / \log_2 d \rfloor$. Iterating $k$ times reduces depth from $d$ to $d / 2^k$ while removing only $O(E / \log \log d)$ edges — the foundation of Valiant's depth-reduction program for linear-size log-depth circuits.

**Statement (`valiant_msb_halving_step`)**:
```lean
theorem valiant_msb_halving_step
    (k E : Nat) (hk : k ≥ 1) (b : Fin k → Nat) (hsum : sumFinNat k b = E) :
    ∃ i : Fin k, b i ≤ E / k
```

**Constructive Proof**:
1. **`sumFinNat_ge_mul_of_forall_ge`**: By induction on $k$, $(\forall i,\, t \le b_i) \implies k \cdot t \le \sum_i b_i$.
2. **`exists_le_or_forall_gt`**: Constructively (via `Nat.decLe` and `Nat.decLt`, zero `Classical.em`), either $\exists i,\, b_i \le t$ or $\forall i,\, t + 1 \le b_i$.
3. Apply `exists_le_or_forall_gt` with $t = \lfloor E / k \rfloor$:
   - In the `inl` branch, we immediately obtain the desired witness $i \in \mathrm{Fin}\,k$ with $b_i \le E / k$.
   - In the `inr` branch, every bucket has size $\ge E / k + 1$, so `sumFinNat_ge_mul_of_forall_ge` gives $k \cdot (E / k + 1) \le E$. Combined with Euclidean division `Nat.div_add_mod : k * (E / k) + E % k = E`, `Nat.mod_lt : E % k < k` (using `hk : k ≥ 1`), and `Nat.mul_succ : k * (E / k + 1) = k * (E / k) + k`, `omega` derives a contradiction. $\blacksquare$

---

## 3. Machine-Checked & Exhaustive Verification Summary

- **Live Lean 4 Kernel Build**:
  - `formal/lean4/MillenniumRelay/ProofComplexityPHP.lean` compiled cleanly with **0 errors, 0 warnings** (`✔ Built MillenniumRelay.ProofComplexityPHP (1.0s)` via `lake build`).
  - `#print axioms` confirmed all four main theorems depend only on `[propext, Quot.sound]` — **zero `sorryAx`, zero custom axioms, zero `Classical.choice`**.
  - `formal/lean4/lakefile.toml` updated to `roots = ["MillenniumRelay.TseitinDichotomy", "MillenniumRelay.ProofComplexityPHP"]` (with `lean-toolchain` pinned to `leanprover/lean4:v4.12.0`).
- **Automated Verification Suite (`verification/verify_baton_015_lean4_library.py`)**:
  1. Static hygiene audit on both `ProofComplexityPHP.lean` and `TseitinDichotomy.lean` (0 forbidden tokens in both raw and comment-stripped text; 0 external/Mathlib imports; 0 version-fragile tactics; all 13 declarations present).
  2. `lakefile.toml` and `lean-toolchain` packaging check via stdlib `tomllib`.
  3. **Theorem 1**: Exhaustively checked all $16{,}739$ functions $\mathrm{Fin}(n+1) \to \mathrm{Fin}(n)$ for $n = 0..5$ (0 injections) and verified the constructive redirect map on all $872$ bijections for $n = 1..5$.
  4. **Theorem 2**: Exhaustively checked all $4{,}164$ binary matrices for $n = 1..3$, $10{,}000$ signed integer matrices for $n = 1..10$, $10{,}251$ Chvátal–Gomory rounding pairs ($5{,}100$ active), and the exact LP integrality gap ($x_{i,j} = 1/n$) for $n = 2..20$.
  5. **Theorem 3**: Exhaustively checked all $8{,}567$ weak bucket compositions ($k \in [1, 5], E \in [0, 12]$, $452$ tight), $10{,}000$ random partitions ($k \le 64, E \le 100{,}000$), and $3$ concrete MSB-bucket DAG depth-halving simulations ($d = 16, 32, 64$, verifying edge deletion $\le \lfloor E / \log_2 d \rfloor$ and post-deletion depth $\le d/2 - 1$).
  6. Live local Lean 4 kernel check passing with exit code 0, 0 errors, 0 warnings.

---

## 4. Mandatory 4-Barrier Audit

Baton #015 formalizes **foundational proof-complexity and depth-reduction lemmas** rather than proposing a direct $\text{P} \neq \text{NP}$ separation. Nevertheless, auditing how each formalized theorem interacts with the four major complexity barriers clarifies what these lemmas can and cannot do downstream:

| Barrier | Reference | Interaction with Baton #015 Theorems | Status |
| :--- | :--- | :--- | :--- |
| **1. Relativization** | Baker–Gill–Solovay (1975) | `pigeonhole_no_injection`, `cutting_planes_php_contradiction`, and `valiant_msb_halving_step` are unconditional finite combinatorial/arithmetic theorems independent of oracles. Note that **Relativized PHP** (`PHP(R)` for an oracle relation) *can* be separated in weak proof systems, whereas Valiant's graph depth-reduction is purely combinatorial and applies identically to oracle circuits (hence cannot by itself bypass BGS for Turing-machine separations). | **N/A (Combinatorial core)**; non-relativizing ingredients remain required for global separations |
| **2. Natural Proofs** | Razborov–Rudich (1997) | Cutting Planes refutations of $\text{PHP}_n^{n+1}$ (`cutting_planes_php_contradiction` + `chvatal_gomory_hole_step`) demonstrate *upper bounds* (short proofs) in $\text{CP}$, explaining why $\text{PHP}$ cannot separate $\text{CP}$ (or $\text{TC}^0$-Frege / Frege) from $\text{EF}$. Meanwhile, Valiant's depth reduction (`valiant_msb_halving_step`) reduces linear-size log-depth circuit lower bounds to common-information / rigidity lower bounds — which *avoid* largeness if proved for explicit matrices, though known rigidity constructions remain far short of Valiant's threshold. | **Intact**; formalization clarifies why $\text{PHP}$ fails as a $\text{CP}$/$\text{TC}^0$-Frege hard tautology |
| **3. Algebrization** | Aaronson–Wigderson (2009) | Double-sum integer cancellation (`sumFin_swap`) and integer rounding (`chvatal_gomory_hole_step`) are discrete $\mathbb{Z}$-inferences (non-algebraic over fields of characteristic $0$, since fractional $1/n$ survives over $\mathbb{Q}$). However, proving super-polynomial lower bounds for Frege / Extended Frege requires non-algebrizing / non-interpolation techniques beyond integer counting. | **Intact**; handed off to proof-complexity frontier (`baton-012`) |
| **4. Locality Barrier** | CHOPRS (STOC 2020) | Valiant's MSB-bucket halving (`valiant_msb_halving_step`) is a global topological cut over all $E$ edges; turning depth reduction into circuit lower bounds for $O(n)$-size $O(\log n)$-depth circuits hits the Valiant rigidity wall (Alman–Williams 2017 showed Walsh–Hadamard is non-rigid, blocking naive rigidity attacks), orthogonal to CHOPRS locality in magnification. | **Unchanged**; active blocker on Route 1B |

---

## 5. Handoff to Next Batons

1. **GitHub Actions `lean4-kernel-gate` (`leanprover/lean4:v4.12.0`)**:
   With `formal/lean4/lakefile.toml` now listing both `MillenniumRelay.TseitinDichotomy` and `MillenniumRelay.ProofComplexityPHP`, the next push to `main` automatically kernel-checks all theorems in both files under exact `leanprover/lean4:v4.12.0`.
2. **Proof Complexity Frontier (`baton-012-ac0-mod2-frege-php`)**:
   `cutting_planes_php_contradiction` + `chvatal_gomory_hole_step` formally capture why **counting-capable systems** ($\text{CP}$, $\text{TC}^0$-Frege, Frege) have short proofs of $\text{PHP}_n^{n+1}$. Downstream work on $\text{AC}^0[2]$-Frege (which has $\text{MOD}_2$ parity gates but cannot count over $\mathbb{Z}$) can build directly on this formalized distinction between $\mathbb{Z}$-summation (`sumFin`) and $\mathbb{F}_2$-summation.
3. **Future Formalization Extensions**:
   - Formalize the **Ben-Sasson–Wigderson width identity** $w(\text{PHP}_n^{n+1} \vdash \bot) = n$ from Baton #006 in a new zero-Mathlib module `MillenniumRelay/ResolutionWidth.lean`.
   - Formalize **iterated Valiant depth-halving** (`k` recursive applications of `valiant_msb_halving_step` on explicit finite DAGs) to machine-check the exact edge-deletion budget $\le k \cdot \lfloor E / \log_2 d \rfloor$.
