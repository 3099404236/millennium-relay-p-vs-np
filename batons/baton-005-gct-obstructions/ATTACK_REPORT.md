# Baton #005: Geometric Complexity Theory (GCT) Obstructions & Valiant's Algebraic P vs NP (`VP` vs `VNP`)

- **Target Millennium Problem**: P versus NP (via Valiant's algebraic analog $\text{VP}$ vs $\text{VNP}$, Permanent vs Determinant)
- **Baton ID**: `baton-005`
- **Node ID**: `baton-005-gct-obstructions`
- **Status**: `BLOCKED_BY_BARRIER` (Did **not** resolve $\text{P}$ vs $\text{NP}$ or $\text{VP}$ vs $\text{VNP}$; verified exact Grenet determinantal constructions $\operatorname{dc}(\operatorname{perm}_2)=2$, $\operatorname{dc}(\operatorname{perm}_3)\le 7$ symbolically in $\mathbb{Z}[X]$ and numerically across 50 random integer matrices, and $\operatorname{dc}(\operatorname{perm}_4)\le 15$; proved & computationally verified the Pieri Padding Interlacing Lemma and small-degree occurrence positivity mirroring Bürgisser–Ikenmeyer–Panova (JAMS 2019); mapped the surviving `#P`-hard multiplicity-obstruction frontier and Algebraic Natural Proofs barrier)
- **Date**: 2026-11-26
- **Verification Command**: `python verification/verify_baton_005_gct_perm_det.py`

---

## 1. Valiant's Algebraic $\text{P}$ vs $\text{NP}$ (`VP` vs `VNP`) & Determinantal Complexity

### 1.1 Algebraic Complexity Classes and Relevance to $\text{P}$ vs $\text{NP}$
Valiant (1979) formulated an algebraic analog of $\text{P}$ vs $\text{NP}$ over a field $\mathbb{F}$ (for GCT, $\mathbb{F} = \mathbb{C}$):
- **$\text{VP}$**: families of multivariate polynomials $\{f_n\}$ of polynomial degree computed by polynomial-size arithmetic circuits.
- **$\text{VBP}$** (often denoted $\text{VP}_{ws}$): families computed by polynomial-size algebraic branching programs (ABPs), equivalently affine-linear projections of polynomial-size determinants.
- **$\text{VNP}$**: families expressible as exponential Boolean-hypercube sums $f_n(\mathbf{x}) = \sum_{\mathbf{e}\in\{0,1\}^{p(n)}} g_n(\mathbf{x},\mathbf{e})$ with $\{g_n\} \in \text{VP}$.

By **Valiant's Completeness Theorems (1979)**:
- The permanent $\operatorname{perm}_n(X) = \sum_{\sigma \in S_n} \prod_{i=1}^n x_{i,\sigma(i)}$ is **$\text{VNP}$-complete** over any field of characteristic $\neq 2$.
- The determinant $\det_m(Y) = \sum_{\sigma \in S_m} \operatorname{sgn}(\sigma) \prod_{i=1}^m y_{i,\sigma(i)}$ is **$\text{VBP}$-complete** (and $\text{VP}$-hard under quasi-polynomial projections).

**Bridge to Boolean $\text{P}$ vs $\text{NP}$ (Bürgisser 2000)**: Assuming the Generalized Riemann Hypothesis (GRH), $\text{VP}_{\mathbb{C}} = \text{VNP}_{\mathbb{C}} \implies \text{NP} \subseteq \text{P/poly}$ (via Nullstellensatz/prime-modulus transfer and Toda's theorem). Contrapositively, separating $\text{VP}_{\mathbb{C}} \neq \text{VNP}_{\mathbb{C}}$ is a mathematically necessary prerequisite (under GRH) to proving $\text{NP} \not\subseteq \text{P/poly}$.

### 1.2 Determinantal Complexity, Valiant's Universality, and Grenet's Exact Upper Bound
The **determinantal complexity** $\operatorname{dc}(f)$ of a polynomial $f(X)$ is the smallest $m$ such that $f(X) = \det_m(A(X))$ for an $m \times m$ matrix $A(X)$ whose entries are affine-linear forms in $X$. Its Zariski-closure analog is the **border determinantal complexity** $\overline{\operatorname{dc}}(f)$, the smallest $m$ such that $f$ lies in the Zariski closure of affine projections of $\det_m$.

- **Valiant's Universality Theorem (1979)**: Every polynomial $f$ computed by an arithmetic formula or algebraic branching program of size $s$ satisfies $\operatorname{dc}(f) \le s + 2$ (and every $f \in \text{VP}$ satisfies $\operatorname{dc}(f) = n^{O(\log n)}$). Valiant's Conjecture states $\operatorname{dc}(\operatorname{perm}_n) = n^{\omega(1)}$; the Mulmuley–Sohoni GCT strengthening asserts $\overline{\operatorname{dc}}(\operatorname{perm}_n) = n^{\omega(1)}$.
- **Best General Lower Bound**: Mignon–Ressayre (2004) over $\mathbb{C}$ (extended to $\operatorname{char}\neq 2$ by Cai–Chen–Li 2010) proved $\operatorname{dc}(\operatorname{perm}_n) \ge n^2 / 2$ via Hessian rank.
- **Exact Small-$n$ Values & Grenet's Upper Bound (2011)**:
  - For $n = 2$: $\operatorname{dc}(\operatorname{perm}_2) = 2$, witnessed explicitly by
    $$M_2(X) = \begin{pmatrix} x_{00} & -x_{01} \\ x_{10} & x_{11} \end{pmatrix}, \qquad \det(M_2(X)) = x_{00}x_{11} + x_{01}x_{10} = \operatorname{perm}_2(X).$$
  - **Theorem (Grenet 2011)**: For every $n \ge 2$, $\operatorname{dc}(\operatorname{perm}_n) \le 2^n - 1$.
    *Proof sketch (cycle-cover bijection)*: Form the Boolean-lattice DAG on $2^n$ subsets $S \subseteq \{0,\dots,n-1\}$ with directed edges $S \to S \cup \{j\}$ ($j \notin S$) weighted by $x_{|S|, j}$. Paths from $\emptyset$ to $\{0,\dots,n-1\}$ are in bijection with $S_n$ and have product weights $\prod_{i=0}^{n-1} x_{i,\sigma(i)}$. Identify $\emptyset$ and $\{0,\dots,n-1\}$ into a single vertex $v_0$, producing a directed graph $G'_n$ on $N = 2^n - 1$ vertices, and add weight-$1$ self-loops on all $2^n - 2$ proper nonempty subsets. Every cycle cover of $G'_n$ consists of a unique $n$-cycle through $v_0$ (of sign $(-1)^{n-1}$) plus $2^n - 1 - n$ self-loops of weight $1$. Scaling row $0$ by $(-1)^{n-1}$ yields a $(2^n - 1)\times(2^n - 1)$ affine-linear matrix $M_n(X)$ with $\det(M_n(X)) = \operatorname{perm}_n(X)$ identically in $\mathbb{Z}[X]$.
  - For $n = 3$, $(-1)^{3-1} = +1$ and $2^3 - 1 = 7$, yielding Grenet's explicit $7 \times 7$ matrix (indexed by $0:\emptyset/\![3]$, $1:\{0\}$, $2:\{1\}$, $3:\{2\}$, $4:\{0,1\}$, $5:\{0,2\}$, $6:\{1,2\}$):
    $$M_3(X) = \begin{pmatrix}
    0 & x_{00} & x_{01} & x_{02} & 0 & 0 & 0 \\
    0 & 1 & 0 & 0 & x_{11} & x_{12} & 0 \\
    0 & 0 & 1 & 0 & x_{10} & 0 & x_{12} \\
    0 & 0 & 0 & 1 & 0 & x_{10} & x_{11} \\
    x_{22} & 0 & 0 & 0 & 1 & 0 & 0 \\
    x_{21} & 0 & 0 & 0 & 0 & 1 & 0 \\
    x_{20} & 0 & 0 & 0 & 0 & 0 & 1
    \end{pmatrix}.$$
    Combined with the singular-locus codimension lower bound of Alper–Bogart–Velasco (2017), $\operatorname{dc}(\operatorname{perm}_3) = 7$ is exact!

**Verification (`verification/verify_baton_005_gct_perm_det.py`)**:
- Symbolically expanded $\det(M_3(X))$ over $\mathbb{Z}[x_{00},\dots,x_{22}]$ and verified exact polynomial identity $\det(M_3(X)) \equiv \operatorname{perm}_3(X)$ (6 monomials, coefficient $+1$ each).
- Verified `det_bareiss(M_3(X)) == perm_ryser(X)` across 50 random integer $3 \times 3$ matrices, `dc(perm_2) = 2` across 50 random $2 \times 2$ matrices, and Grenet's $15 \times 15$ matrix `M_4(X)` across 20 random $4 \times 4$ matrices (`dc(perm_4) <= 15`).

---

## 2. The Geometric Complexity Theory (GCT) Orbit-Closure Framework

Mulmuley and Sohoni (2001, 2008) recast $\overline{\operatorname{dc}}(\operatorname{perm}_n) > m$ into representation theory of $\operatorname{GL}_{m^2}(\mathbb{C})$ acting on $V = \operatorname{Sym}^m(\mathbb{C}^{m^2})$:

1. **Orbit Closures**: Pad $\operatorname{perm}_n$ to homogeneous degree $m$ using a fresh linear form $\ell$:
   $$Z_{m,n} := \overline{\operatorname{GL}_{m^2}(\mathbb{C}) \cdot (\ell^{m-n}\operatorname{perm}_n)}, \qquad \Omega_m := \overline{\operatorname{GL}_{m^2}(\mathbb{C}) \cdot \det_m} \subset \operatorname{Sym}^m(\mathbb{C}^{m^2}).$$
2. **Coordinate-Ring Contravariance**: If $\overline{\operatorname{dc}}(\operatorname{perm}_n) \le m$, then $Z_{m,n} \subseteq \Omega_m$, inducing a $\operatorname{GL}_{m^2}$-equivariant surjection on every homogeneous degree-$d$ component of the coordinate rings:
   $$\mathbb{C}[\Omega_m]_d \twoheadrightarrow \mathbb{C}[Z_{m,n}]_d.$$
3. **Multiplicity Inequality (Schur's Lemma)**: Decomposing into irreducible Weyl modules $S_\lambda(\mathbb{C}^{m^2})$ ($\lambda \vdash md$, $\ell(\lambda) \le m^2$), $Z_{m,n} \subseteq \Omega_m$ forces:
   $$\forall d \ge 1,\;\forall \lambda \vdash md: \qquad \operatorname{mult}_\lambda(\mathbb{C}[Z_{m,n}]_d) \le \operatorname{mult}_\lambda(\mathbb{C}[\Omega_m]_d).$$
4. **Ambient Plethysm & Determinant Orbit Upper Bounds**:
   - The ambient degree-$d$ coordinate ring is the plethysm $\operatorname{Sym}^d(\operatorname{Sym}^m(\mathbb{C}^{m^2})) = \bigoplus_{\lambda \vdash md} S_\lambda^{\oplus a_\lambda(d,m)}$, where $a_\lambda(d,m) = \langle s_\lambda, h_d[h_m] \rangle$.
   - The stabilizer of $\det_m$ in $\operatorname{SL}_{m^2}$ is $(\operatorname{SL}_m \times \operatorname{SL}_m) \rtimes \mathbb{Z}_2$ (transpose). By Frobenius reciprocity, the open-orbit coordinate ring satisfies:
     $$\operatorname{mult}_\lambda(\mathbb{C}[\operatorname{GL}_{m^2}\cdot \det_m]_d) = \operatorname{sk}(\lambda; d^m) \le k(\lambda, d^m, d^m),$$
     where $d^m = (d,\dots,d)$ is the $m \times d$ rectangle, $k(\lambda, d^m, d^m)$ is the rectangular Kronecker coefficient, and $\operatorname{sk}(\lambda; d^m) = \operatorname{mult}_\lambda(\operatorname{Sym}^2([d^m]))$ is the symmetric rectangular Kronecker coefficient.
   - Hence $\operatorname{mult}_\lambda(\mathbb{C}[\Omega_m]_d) \le \min\big(a_\lambda(d,m),\; \operatorname{sk}(\lambda; d^m)\big)$.

---

## 3. Why Occurrence Obstructions Fail (Padding Interlacing + BIP, JAMS 2019)

An **occurrence obstruction** is a partition $\lambda \vdash md$ such that $\operatorname{mult}_\lambda(\mathbb{C}[Z_{m,n}]_d) > 0$ while $\operatorname{mult}_\lambda(\mathbb{C}[\Omega_m]_d) = 0$. Mulmuley–Sohoni originally conjectured that occurrence obstructions suffice to prove super-polynomial lower bounds on $\overline{\operatorname{dc}}(\operatorname{perm}_n)$.

### 3.1 The Padding Interlacing Lemma (Elementary Pieri Proof)
Why are candidate partitions for $Z_{m,n}$ forced into a narrow corner of Young diagrams?

**Lemma (Padding Interlacing)**: *Every irreducible $S_\lambda$ occurring in $\mathbb{C}[Z_{m,n}]_d$ satisfies:*
1. $\ell(\lambda) \le n^2 + 1$ (since $\ell^{m-n}\operatorname{perm}_n$ uses at most $n^2+1$ variables);
2. $\lambda_1 \ge d(m - n)$, equivalently $|\bar{\lambda}| := \sum_{i \ge 2} \lambda_i \le nd$.

*Proof*: For every $g \in \operatorname{GL}_{m^2}$,
$$(g \cdot (\ell^{m-n}\operatorname{perm}_n))^{\otimes d} = \underbrace{(g\cdot \ell)^{\otimes d(m-n)}}_{\in\, \operatorname{Sym}^{d(m-n)}(V) \,=\, S_{(d(m-n))}(V)} \otimes \underbrace{(g\cdot \operatorname{perm}_n)^{\otimes d}}_{\in\, \operatorname{Sym}^d(\operatorname{Sym}^n(V))}$$
maps equivariantly into $\operatorname{Sym}^d(\operatorname{Sym}^m(V))$. Thus every $S_\lambda$ in $\mathbb{C}[Z_{m,n}]_d$ occurs in $S_{(d(m-n))} \otimes S_\mu$ for some $\mu \vdash nd$ with $a_\mu(d,n) > 0$. By the **Pieri Rule**, $\lambda / \mu$ is a horizontal strip, giving interlacing $\lambda_1 \ge \mu_1 \ge \lambda_2 \ge \mu_2 \ge \dots$. Summing $\lambda_{i+1} \le \mu_i$ over $i \ge 1$ yields $|\bar{\lambda}| = \sum_{i \ge 2}\lambda_i \le |\mu| = nd$, hence $\lambda_1 = md - |\bar{\lambda}| \ge d(m-n)$. $\square$

### 3.2 The Bürgisser–Ikenmeyer–Panova No-Go Theorem (JAMS 2019)
Building on Ikenmeyer–Panova (FOCS 2016 / Adv. Math. 2017) on rectangular Kronecker positivity for partitions with long first rows, **Bürgisser, Ikenmeyer, and Panova (JAMS, Vol. 32, No. 1, 2019, pp. 163–193)** proved:

> **Theorem (BIP 2019 — No Occurrence Obstructions)**: Let $m, n, d \ge 1$ with $m \ge n^{25}$ and $\lambda \vdash md$. If $S_\lambda$ occurs in $\mathbb{C}[Z_{m,n}]_d$, then $S_\lambda$ **also occurs** in $\mathbb{C}[\Omega_m]_d$ (i.e., $\operatorname{mult}_\lambda(\mathbb{C}[\Omega_m]_d) > 0$).

**Why it kills occurrence obstructions**:
1. The padding factor $\ell^{m-n}$ forces every $\lambda$ occurring in $\mathbb{C}[Z_{m,n}]_d$ to have a massive first row ($\lambda_1 \ge d(m-n)$) and bounded number of rows ($\ell(\lambda) \le n^2 + 1$).
2. Conversely, $\Omega_m$ is rich enough (via Valiant universality / degenerations of $\det_m$ into padded sums of powers / low-variable polynomials and Kronecker semigroup positivity) that $\mathbb{C}[\Omega_m]_d$ absorbs **every** irreducible representation satisfying those padding constraints whenever $m \ge n^{25}$.
3. Consequently, **no occurrence obstruction can ever prove a lower bound stronger than $\overline{\operatorname{dc}}(\operatorname{perm}_n) = \Omega(n^{25})$**, completely blocking the super-polynomial bound required for $\overline{\text{VBP}} \neq \text{VNP}$!

### 3.3 Exact Computational Verification on Small Padded $(n, m, d)$ Instances
Using our exact Murnaghan–Nakayama character engine, wreath-product plethysm engine ($a_\lambda(d,m) = \frac{1}{|S_m \wr S_d|}\sum_{g \in S_m \wr S_d} \chi^\lambda(g)$), and Pieri horizontal-strip generator in `verification/verify_baton_005_gct_perm_det.py`, we verified full character-table orthogonality for $S_4, S_6, S_8, S_9, S_{10}$, checked all plethysms against $\operatorname{GL}_4$ Weyl dimension identities, and computed exact Kronecker and symmetric Kronecker multiplicities across all padding-admissible candidate partitions:

| Padded Instance $(n,m,d)$ | $N=md$ | Min $\lambda_1 = d(m-n)$ | Candidate $\lambda$ | $a_\lambda(d,m)$ | $k(\lambda, d^m, d^m)$ | $\operatorname{sk}(\lambda; d^m)$ | Orbit Occ. Obstruction? |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| $(2, 3, 2)$ | 6 | 2 | $(6)$, $(4,2)$ | $1, 1$ | $1, 1$ | $1, 1$ | **None (0/2)** |
| $(2, 4, 2)$ | 8 | 4 | $(8)$, $(6,2)$, $(4,4)$ | $1, 1, 1$ | $1, 1, 1$ | $1, 1, 1$ | **None (0/3)** |
| $(2, 5, 2)$ | 10 | 6 | $(10)$, $(8,2)$, $(6,4)$ | $1, 1, 1$ | $1, 1, 1$ | $1, 1, 1$ | **None (0/3)** |
| $(2, 3, 3)$ | 9 | 3 | $(9)$, $(7,2)$, $(6,3)$, $(5,2,2)$, $(4,4,1)$ | $1,1,1,1,1$ | $1,1,1,2,1$ | $1,1,1,2,1$ | **None (0/5)** |

Notice two sharp mathematical phenomena revealed even at $N = 9$:
- **100% occurrence positivity** across every padding-admissible candidate ($\operatorname{sk}(\lambda; d^m) \ge 1$ everywhere), illustrating the small-scale precursor of BIP (2019).
- **Non-trivial multiplicity & orbit-vs-closure gap**: At $(2,3,3)$, $\lambda = (5,2,2)$ has $\operatorname{sk}((5,2,2); (3,3,3)) = 2 > 1 = a_{(5,2,2)}(3,3)$, showing that the open-orbit multiplicity strictly exceeds the ambient plethysm multiplicity (whereas for the non-plethysm partition $(3,3,3)$, $k=1$ splits into $\operatorname{sk}=0, \operatorname{ak}=1$, confirming the transpose-symmetry filter is non-trivial).

---

## 4. The Surviving Frontier: Multiplicity Obstructions & Their Complexity Wall

With occurrence obstructions provably dead for $m \ge n^{25}$, GCT survives only via **multiplicity obstructions**: finding $\lambda \vdash md$ with
$$0 < \operatorname{mult}_\lambda(\mathbb{C}[\Omega_m]_d) < \operatorname{mult}_\lambda(\mathbb{C}[Z_{m,n}]_d).$$
However, multiplicity obstructions hit two severe structural barriers:
1. **Computational `#P`-Hardness & Missing Combinatorial Rules**:
   - Computing Kronecker coefficients $k(\lambda,\mu,\nu)$ is **`#P`-hard** (Bürgisser–Ikenmeyer 2008), and even deciding positivity $k(\lambda,\mu,\nu) > 0$ is **`NP`-hard** (Ikenmeyer–Mulmuley–Walter 2017).
   - Computing plethysm coefficients $a_\lambda(d,m)$ is **`#P`-hard** (Fischer–Ikenmeyer 2020), and finding a positive combinatorial rule for $k(\lambda,\mu,\nu)$ or $a_\lambda(d,m)$ remains one of the deepest open problems in algebraic combinatorics (Stanley's Problem 9).
   - Worse still, $\operatorname{mult}_\lambda(\mathbb{C}[\Omega_m]_d)$ is strictly smaller than $\operatorname{sk}(\lambda; d^m)$ in general (due to boundary/non-normality phenomena in the orbit closure $\Omega_m$), meaning one cannot even rely on open-orbit Kronecker upper bounds alone unless $\operatorname{sk}(\lambda; d^m) < \operatorname{mult}_\lambda(\mathbb{C}[Z_{m,n}]_d)$.
2. **Algebraic Natural Proofs Barrier (Forbes–Shpilka–Volk 2018; Grochow–Kumar–Saks–Saraf 2017; Efremenko–Garg–Oliveira–Wigderson 2018)**:
   - Any GCT multiplicity obstruction produces a highest-weight polynomial $P \in \mathbb{C}[\operatorname{Sym}^m(\mathbb{C}^{m^2})]_d$ vanishing on $\Omega_m$ (all small determinants) and non-vanishing on $Z_{m,n}$ (the padded permanent).
   - If $\operatorname{VP}$ contains pseudorandom polynomial families (polynomials with small arithmetic circuits indistinguishable by small-circuit distinguishers), then no **low-degree, efficiently computable** polynomial $P$ (i.e., $P$ itself in $\text{VP}$) can vanish on all of $\Omega_m$! Thus any successful GCT multiplicity obstruction must either have **super-polynomial degree $d$** or yield **defining equations of $\Omega_m$ that are themselves computationally hard** (not in $\text{VP}$).

---

## 5. Mandatory 4-Barrier Audit

| Barrier | Reference | What It Blocks | Status for GCT (`baton-005`) |
| :--- | :--- | :--- | :--- |
| **1. Relativization** | Baker–Gill–Solovay (1975) | Pure black-box simulation/diagonalization invariant under oracles | **Bypassed**: GCT works over $\mathbb{C}$ using algebraic geometry and $\operatorname{GL}_{m^2}$-representation theory of specific polynomials ($\det_m, \operatorname{perm}_n$), not relativizing Turing machines. |
| **2. Natural Proofs (Boolean & Algebraic)** | Razborov–Rudich (1997); Forbes–Shpilka–Volk (2018); GKSS (2017) | Large + constructive circuit/polynomial distinguishers (assuming PRFs / algebraic PRGs) | **Partially Bypassed (Boolean) / ACTIVE BLOCKER (Algebraic)**: Bypasses Boolean Razborov–Rudich via algebraic geometry, **but** any low-degree / $\text{VP}$-computable GCT obstruction polynomial vanishing on $\Omega_m$ hits the **Algebraic Natural Proofs Barrier** (FSV 2018 / GKSS 2017). |
| **3. Algebrization** | Aaronson–Wigderson (2009) | Arithmetization / low-degree oracle extensions alone | **Bypassed in principle (Algebraic setting)**: GCT targets $\text{VP} \neq \text{VNP}$ via non-abelian representation multiplicities of $\operatorname{GL}_{m^2}$-orbit closures, not low-degree oracle interpolation. (Transferring $\text{VP}\neq\text{VNP}$ to Boolean $\text{P}\neq\text{NP}$ still requires GRH or separate non-algebrizing transfer.) |
| **4. Locality Barrier** | CHOPRS (STOC 2020) | Small-depth local oracle reductions in Hardness Magnification | **Not Applicable**: GCT does not use Hardness Magnification reductions. Instead, GCT faces its own domain-specific wall: **BIP (JAMS 2019) No-Occurrence-Obstructions Theorem** + **`#P`-hardness of Kronecker/plethysm multiplicities**. |

---

## 6. Verdict & Exact Handoff to Next Batons

- **Did Baton #005 resolve $\text{P}$ vs $\text{NP}$ or $\text{VP}$ vs $\text{VNP}$?** **NO.**
- **What Baton #005 rigorously verified and mapped**:
  1. Verified exact integer `det_bareiss` and `perm_ryser`, optimal $\operatorname{dc}(\operatorname{perm}_2)=2$, Grenet's explicit $7 \times 7$ matrix $M_3(X)$ ($\det(M_3(X)) \equiv \operatorname{perm}_3(X)$ symbolically in $\mathbb{Z}[X]$ and on 50 random integer matrices), and Grenet's $15 \times 15$ matrix for $\operatorname{perm}_4$.
  2. Proved the Pieri Padding Interlacing Lemma ($\lambda_1 \ge d(m-n)$) and verified 100% small-degree occurrence positivity ($\operatorname{sk}(\lambda; d^m) > 0$) across $(n,m,d) \in \{(2,3,2),(2,4,2),(2,5,2),(2,3,3)\}$ using an exact Murnaghan–Nakayama + wreath-product plethysm engine.
  3. Marked `baton-005-gct-obstructions` as `blocked_by_barrier` due to the **BIP (2019) No-Occurrence-Obstructions wall**, **`#P`-hardness of multiplicity obstructions**, and the **Algebraic Natural Proofs Barrier**.

### Recommended Handoff for Future GCT Batons
1. **Do NOT search for occurrence obstructions** separating $\overline{\operatorname{GL}_{m^2}\cdot (\ell^{m-n}\operatorname{perm}_n)}$ from $\overline{\operatorname{GL}_{m^2}\cdot \det_m}$ — BIP (2019) proves none exist for $m \ge n^{25}$.
2. **Testbed Multiplicity Obstructions on Simpler Algebraic Varieties First**: Before attacking $\det_m$ vs $\operatorname{perm}_n$, build exact multiplicity-obstruction verifiers on **Chow varieties vs secant varieties / Waring border rank** or **matrix multiplication tensors** (where Dörfler–Ikenmeyer–Panova 2019 and Ikenmeyer–Panova demonstrated genuine multiplicity obstructions strictly beating occurrence obstructions).
3. **Avoid Padding Where Possible**: Investigate **unpadded / non-padded geometric models** (e.g., border ABP / iterated matrix multiplication $\operatorname{IMM}_{w,d}$ vs $\operatorname{perm}_n$, where the degree matches without $\ell^{m-n}$ padding, avoiding the Pieri first-row collapse!).
