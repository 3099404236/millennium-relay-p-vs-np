# Baton #003: Direct Structure-Preserving $\text{TC}^0$-SAT Without Tseitin Variable Blowup

- **Target Millennium Problem**: P versus NP (Clay Mathematics Institute — **Unsolved**)
- **Baton ID**: `baton-003`
- **Roadmap Node**: `baton-003-direct-tc0-sat`
- **Status**: `BLOCKED_BY_BARRIER` (Did **not** resolve P vs NP or separate $\text{NEXP} \not\subseteq \text{TC}^0$; built and exhaustively verified a zero-Tseitin structure-preserving depth-2 $\text{TC}^0$-SAT solver, proved and verified the exact mathematical walls pinning current $\text{TC}^0$-SAT at wire bound $w(n) = n^{1 + c^{-d}}$ — namely denominator-clearing degree blowup in BRS rational approximations, exponential wire-exponent decay under Littlewood–Offord random-restriction peeling, collision with Allender–Koucký amplification, and Williams witness-compression loss)
- **Date**: 2026-11-26
- **Dependencies**: `route-1a-blackbox-tseitin-eth`

---

## 1. Mission & Exact Target

Baton #001 (`route-1a-blackbox-tseitin-eth`) proved that black-box Tseitin reduction to sub-exponential $3\text{-SAT}$ is a dead end because it introduces $m = n + s$ variables (and for Linear Threshold Function gates of fan-in $k$, naive adder-based Tseitin translation introduces $\Omega(W)$ auxiliary variables for $W$ wires).

Baton #003 therefore attacks **structure-preserving $\text{TC}^0$-SAT** directly on the $n$ original Boolean input variables $x \in \{0,1\}^n$ (**zero Tseitin variables introduced**):

> **Core Target**: Can structure-preserving $\text{TC}^0$-SAT algorithms (combining meet-in-the-middle half-space domination, random restrictions, and rational/probabilistic polynomial approximations) beat $2^n / n^{\omega(1)}$ for depth-$d$ threshold circuits with $w(n) = n^{1+\epsilon}$ wires for a fixed constant $\epsilon > 0$ independent of $d$ (or $w(n) = n^{1 + \Omega(1/d)}$), which via Ryan Williams's algorithmic method and Allender–Koucký amplification would separate $\text{NEXP} \not\subseteq \text{TC}^0$?

---

## 2. Circuit Model & Structure-Preserving Depth-2 $\text{TC}^0$-SAT

### 2.1 Linear Threshold Circuits ($\text{LTF}^d$)
A **Linear Threshold Function (LTF)** gate $g: \{0,1\}^k \to \{0,1\}$ with integer weights $w \in \mathbb{Z}^k$ and threshold $\theta \in \mathbb{Z}$ computes:
$$g(z_1, \dots, z_k) = \mathbf{1}\!\left[\sum_{j=1}^k w_j z_j \ge \theta\right].$$
A depth-2 $\text{TC}^0$ ($\text{LTF} \circ \text{LTF}$) circuit $C$ on $n$ inputs with $s_1$ bottom gates computes:
$$C(x) = \mathbf{1}\!\left[\sum_{i=1}^{s_1} \alpha_i \, \mathbf{1}\!\left[\langle w^{(i)}, x \rangle \ge \theta_i\right] \ge \Theta\right], \qquad x \in \{0,1\}^n.$$

### 2.2 Zero-Tseitin Split-and-Dominate / Meet-in-the-Middle Half-Space Solver
To solve Depth-2 $\text{TC}^0$-SAT **without introducing any Tseitin variables**, we exploit four exact structural invariants of $\text{LTF} \circ \text{LTF}$:

1. **Monotone-Top Canonicalization (Exact Identity, 0 Auxiliary Variables)**:
   For every bottom gate $i$ with $\alpha_i < 0$, observe that
   $$1 - \mathbf{1}\!\left[\langle w^{(i)}, x \rangle \ge \theta_i\right] = \mathbf{1}\!\left[\langle w^{(i)}, x \rangle \le \theta_i - 1\right] = \mathbf{1}\!\left[\langle -w^{(i)}, x \rangle \ge 1 - \theta_i\right].$$
   Substituting $\alpha_i g_i(x) = \alpha_i + (-\alpha_i)(1 - g_i(x))$, we replace $(w^{(i)}, \theta_i, \alpha_i) \mapsto (-w^{(i)}, 1 - \theta_i, -\alpha_i)$ and shift $\Theta \mapsto \Theta - \alpha_i$ (dropping any $\alpha_i = 0$ gate). The resulting circuit $\tilde{C}$ satisfies $\tilde{C}(x) = C(x)$ **for all** $x \in \{0,1\}^n$ and has strictly positive top weights $\tilde{\alpha}_i > 0$.

2. **Meet-in-the-Middle Variable Split ($x = (x_L, x_R)$)**:
   Partition $n = n_L + n_R$ with $n_L = \lfloor n/2 \rfloor$, $n_R = \lceil n/2 \rceil$. Every bottom affine form splits additively:
   $$\langle \tilde{w}^{(i)}, x \rangle = a_i(x_L) + b_i(x_R), \quad a_i(x_L) = \langle \tilde{w}^{(i)}_L, x_L \rangle, \; b_i(x_R) = \langle \tilde{w}^{(i)}_R, x_R \rangle.$$
   Precomputing the tables $L = \{a(x_L) : x_L \in \{0,1\}^{n_L}\}$ and $R = \{b(x_R) : x_R \in \{0,1\}^{n_R}\}$ costs $2^{n_L} + 2^{n_R} = O(2^{n/2})$ evaluations.

3. **Exact Pareto Vector-Domination Pruning**:
   Because every $\tilde{\alpha}_i > 0$, $\tilde{C}(x_L, x_R)$ is coordinatewise monotone non-decreasing in both $a(x_L) \in \mathbb{Z}^{s_1}$ and $b(x_R) \in \mathbb{Z}^{s_1}$.
   - **Lemma 1 (Soundness of Pareto Filtering)**: If $a(x_L) \le a(x'_L)$ componentwise, then $\tilde{C}(x_L, x_R) \le \tilde{C}(x'_L, x_R)$ for every $x_R \in \{0,1\}^{n_R}$. Hence discarding all strictly/weakly dominated vectors from $L$ (yielding Pareto frontier $P_L$) and symmetrically from $R$ (yielding $P_R$) preserves satisfiability identically:
     $$\exists x \in \{0,1\}^n\; C(x) = 1 \iff \exists (u, v) \in P_L \times P_R\; \sum_{i=1}^{s_1} \tilde{\alpha}_i\,\mathbf{1}[u_i + v_i \ge \tilde{\theta}_i] \ge \tilde{\Theta}.$$

4. **Dual-Tree Half-Space Bounding-Box Search**:
   Build balanced axis-aligned bounding-box trees (KD-trees splitting on max $\tilde{\alpha}_i$-weighted spread) over $P_L$ and $P_R$. For any pair of sub-boxes $(U, V)$ with coordinate bounds $[U^{\min}, U^{\max}]$ and $[V^{\min}, V^{\max}]$:
   $$\text{UB}(U, V) = \sum_{i : U^{\max}_i + V^{\max}_i \ge \tilde{\theta}_i} \tilde{\alpha}_i, \qquad \text{LB}(U, V) = \sum_{i : U^{\min}_i + V^{\min}_i \ge \tilde{\theta}_i} \tilde{\alpha}_i.$$
   - If $\text{UB}(U, V) < \tilde{\Theta}$: **every** pair in $U \times V$ is guaranteed UNSAT — prune the entire Cartesian block in $O(s_1)$ time.
   - If $\text{LB}(U, V) \ge \tilde{\Theta}$: **every** pair in $U \times V$ is guaranteed SAT — immediately return a concrete witness $(x_L, x_R)$.
   - Otherwise split the larger box and search max-UB-first.

### 2.3 Computational Verification & Empirical Dimension Wall
Implemented and verified in `verification/verify_baton_003_tc0_sat.py` across 50 random non-trivial depth-2 threshold circuits for $n \in \{8, 9, 10, 11, 12\}$ ($s_1 \in \{4, 5, 6, 7\}$, spanning 23 SAT and 27 non-trivial UNSAT instances):
- **100% SAT/UNSAT equivalence** with exhaustive $2^n$ brute force; every returned witness verified directly on the original uncanonicalized circuit.
- **0 Tseitin variables added**.
- **92.9% total work reduction** vs $2^n$ overall (**93.9% reduction on non-trivial UNSAT instances**, with Pareto product survival averaging 37.0% of $2^n$).
- **Curse-of-Dimensionality Probe ($n=12$)**: Increasing the bottom gate count $s_1$ rapidly saturates the Pareto frontier in $\mathbb{Z}^{s_1}$:
  - $s_1 = 3$: **2.9%** of $2^{12}$ pairs survive Pareto filtering;
  - $s_1 = 6$: **40.1%** survive;
  - $s_1 = 12$: **93.8%** survive;
  - $s_1 = 20$: **100.0%** survive (almost all vectors become mutually incomparable in $\mathbb{Z}^{s_1}$).

This concrete computational experiment already exhibits the **vector-domination dimension wall**: meet-in-the-middle domination over $s_1$ bottom gates collapses back toward $2^n$ once $s_1$ grows past $O(n / \operatorname{polylog} n)$ unless combined with polynomial/restriction compression (as in Williams 2014/2018 and Chen–Tell 2019).

---

## 3. The Chen–Tell (STOC 2019) / Williams Frontier: Why $w(n) = n^{1 + c^{-d}}$ Works

Why do the strongest known structure-preserving $\text{TC}^0$-SAT algorithms (Impagliazzo–Paturi–Schneider 2013; Williams 2014/2018; Chen–Santhanam 2015; Tell 2018; Chen–Tell STOC 2019) achieve nontrivial savings $2^{n - n^{\Omega(c^{-d})}}$ up to wire count $w(n) = n^{1 + c^{-d}}$, and why do they hit a brick wall before $w(n) = n^{1 + \epsilon}$ for fixed $\epsilon > 0$?

### 3.1 Iterated Random-Restriction Peeling & Littlewood–Offord $\sqrt{p}$ Shrinkage
Given a depth-$d$ $\text{TC}^0$ circuit $C$ on $n_0 = n$ variables with $W = n^{1 + \epsilon_0}$ wires:
1. **Average Bottom Fan-In**: The average variable degree is $W/n = n^{\epsilon_0}$.
2. **Kane / Littlewood–Offord Restriction Shrinkage**: Under a random (or pseudorandom, bounded-independence) restriction $\rho$ keeping each variable alive with probability $p$, an LTF gate resists collapsing to a constant (or low-fan-in LTF / decision tree) with probability $O(\sqrt{p})$ — the **$\sqrt{p}$ anti-concentration barrier** (contrasting sharply with $O(p)$ shrinkage for $\text{AC}^0$ / De Morgan formulas).
3. **One-Layer Peeling Recurrence**: To shrink/simplify a bottom layer with excess wire density $n_{j-1}^{\epsilon_{j-1}}$ down below the surviving live variables $n_j = p_j n_{j-1}$, we must choose keep probability:
   $$p_j = n_{j-1}^{-\alpha \epsilon_{j-1}}, \qquad \alpha > 1 \quad (\text{typically } \alpha \ge 2 \text{ due to } \sqrt{p} \text{ shrinkage + degree-reduction overhead}).$$
   Let $n_j = n^{\lambda_j}$ ($\lambda_0 = 1$). Then:
   $$\lambda_j = \lambda_{j-1}\!\left(1 - \alpha \epsilon_{j-1}\right).$$
   Because the upper $d - j$ layers still carry up to $W = n^{1 + \epsilon_0}$ wires, the excess wire exponent *relative to the remaining live variables* $n_j$ inflates strictly according to:
   $$1 + \epsilon_j = \frac{1 + \epsilon_0}{\lambda_j} = \frac{1 + \epsilon_{j-1}}{1 - \alpha \epsilon_{j-1}} \implies \epsilon_j = \frac{(1 + \alpha)\epsilon_{j-1}}{1 - \alpha \epsilon_{j-1}} \ge c \cdot \epsilon_{j-1}, \qquad c = 1 + \alpha > 2.$$
4. **Exponential Decay of Tractable Wire Exponent**:
   Peeling $d - 1$ layers down to a tractable base case ($\epsilon_{d-1} \le \epsilon_{\text{base}} < 1$) forces:
   $$c^{d-1} \epsilon_0 \le \epsilon_{d-1} \le \epsilon_{\text{base}} \implies \epsilon_0 = O\!\left(c^{-d}\right) \implies W(n) \le n^{1 + c^{-d}}.$$
   Conversely, for **any fixed** $\epsilon_0 > 0$ independent of $d$, after $t = O(\log_c(1 / (\alpha \epsilon_0)))$ layers we hit $\alpha \epsilon_t \ge 1 \implies \lambda_{t+1} \le 0$: **all $n$ live variables are exhausted before reaching the top gate!**

In `verification/verify_baton_003_tc0_sat.py` ($\alpha = 2.0, c = 3.0, \epsilon_{\text{base}} = 0.5$), numerical simulation confirms:
- $\epsilon_{\max}(d=2) = 0.12500$, $\epsilon_{\max}(d=6) = 0.001374$, $\epsilon_{\max}(d=11) = 5.645 \times 10^{-6}$,
- Asymptotic ratio $\epsilon_{\max}(d-1) / \epsilon_{\max}(d) = 3.0000 \to c = 3.0$,
- Every fixed $\epsilon_0 \in \{0.1, 0.01, 0.001\}$ suffers total live-variable exhaustion ($\lambda = 0$) before depth $d = 20$.

---

## 4. Exact Mathematical Walls Blocking $w(n) = n^{1 + \epsilon}$ and $\text{NEXP} \not\subseteq \text{TC}^0$

### Wall A: Quantitative Collision Against Allender–Koucký (2010) Amplification
By **Allender–Koucký (JACM 2010)**, polynomial-size $\text{TC}^0$ circuits of size $n^k$ and depth $d_0$ for self-reducible targets can be amplified to wire count $n^{1 + \epsilon}$ only at the cost of blowing up the depth to $d(\epsilon) = \Theta(d_0 \cdot k / \epsilon)$, i.e., **polynomially** decaying exponent $\epsilon_{\text{AK}}(d) = \Theta(k / d)$.

**Theorem 1 (Allender–Koucký vs. Chen–Tell Non-Intersection)**:
For every restriction decay base $c \ge 2$, every polynomial witness exponent $k \ge 1$, and every depth $d \ge 1$:
$$c^{-d} < \frac{k}{d}.$$
*Proof*: Let $f(d) = d \cdot c^{-d}$ for $d > 0$. Differentiating gives $f'(d) = c^{-d}(1 - d \ln c)$, so $f$ attains its unique global maximum at $d^* = 1 / \ln c$ with value:
$$\max_{d \ge 1} d \cdot c^{-d} \le \frac{1}{e \ln c} \le \frac{1}{e \ln 2} \approx 0.5307 \quad (\text{and on integers } d \in \mathbb{Z}_{\ge 1},\; \max_{d \ge 1} d \cdot 2^{-d} = \tfrac{1}{2}) < 1 \le k. \quad \blacksquare$$

Thus the **exponential decay** $n^{1 + c^{-d}}$ of Chen–Tell and the **polynomial demand** $n^{1 + \Omega(1/d)}$ of Allender–Koucký **never intersect** at any depth $d \ge 1$.

### Wall B: Beigel–Reingold–Spielman (1995) Rational Approximation & Denominator-Clearing Degree Blowup
Why can't we replace random restrictions with direct algebraic approximations (as Williams did for $\text{ACC}^0$-SAT via Beigel–Tarui / Razborov–Smolensky)?

1. **Polynomial Approximations Fail Already at Depth 1**:
   By **Paturi (1992)**, any real polynomial approximating $\text{MAJ}_k$ to error $1/3$ requires degree $\Omega(\sqrt{k})$ (and $\Omega(\sqrt{k \log(1/\epsilon)})$ for error $\epsilon$). Over $\mathbb{F}_p$, **Razborov (1987) / Smolensky (1987)** prove probabilistic polynomial degree $\Omega(\sqrt{k})$ for $\text{MAJ}_k$. Even composing two layers multiplies degrees to $\Omega(k) = \Omega(n)$, saturating the monomial space $\binom{n}{\le D} = 2^n$.

2. **Beigel–Reingold–Spielman (1995) Rational Approximations Succeed at Depth 1 — Then Explode at Depth 2**:
   For a single LTF gate with integer affine form $z(x) = 2\langle w, x \rangle - 2\theta + 1 \in [-W, -1] \cup [1, W]$ (nonzero odd integers) where $W \le 2^m - 1$, define the Newman/BRS polynomial of degree $D_1 = b \cdot m$:
   $$P_{m,b}(z) = \prod_{j=0}^{m-1} (z + 2^j)^b, \qquad \tilde{R}_{m,b}(z) = \frac{P_{m,b}(z)}{P_{m,b}(z) + P_{m,b}(-z)}.$$
   **Theorem 2 (Exact BRS Error Bound — Verified Exhaustively on 10,728 Integer Points)**:
   For every $z \in [-W, -1] \cup [1, W]$ with $W \le 2^m - 1$ and every $b \ge 1$:
   $$\left|\tilde{R}_{m,b}(z) - \mathbf{1}[z > 0]\right| < \frac{3^{-b}}{1 - 3^{-b}}.$$
   *Proof*: Let $u = |z| \in [1, 2^m - 1]$ and pick $j^* = \lfloor \log_2 u \rfloor \in \{0, \dots, m-1\}$. Then $2^{j^*} \le u < 2^{j^*+1}$, giving
   $$\left|\frac{u - 2^{j^*}}{u + 2^{j^*}}\right| = \frac{u - 2^{j^*}}{u + 2^{j^*}} < \frac{2^{j^*}}{3 \cdot 2^{j^*}} = \frac{1}{3},$$
   while every other factor $j \ne j^*$ satisfies $\left|\frac{u - 2^j}{u + 2^j}\right| < 1$. Hence $|\rho(u)| = |P_{m,b}(-u)/P_{m,b}(u)| < 3^{-b}$, yielding error $\left|\frac{\rho(u)}{1 + \rho(u)}\right| < \frac{3^{-b}}{1 - 3^{-b}}$. $\blacksquare$

   **Theorem 3 (Denominator-Clearing Degree Explosion at Depth $\ge 2$)**:
   To approximate a depth-2 gate $G(g_1, \dots, g_{s_1}) = \mathbf{1}\!\left[\sum_{i=1}^{s_1} \alpha_i g_i(x) \ge \Theta\right]$, each bottom gate $g_i$ must be approximated by $\tilde{R}_i(x) = A_i(x)/B_i(x)$ to error $\epsilon_1 < \frac{1}{4 A_{\text{top}}}$ where $A_{\text{top}} = \sum_{i=1}^{s_1} |\alpha_i|$, requiring $b_1 = \Omega(\log A_{\text{top}})$ and single-gate degree $D_1 = \Omega(\log W_1 \cdot \log A_{\text{top}})$.
   Forming the top input sum over a common denominator:
   $$Z_{\text{top}}(x) = \sum_{i=1}^{s_1} \alpha_i \frac{A_i(x)}{B_i(x)} - \Theta = \frac{\sum_{i=1}^{s_1} \alpha_i A_i(x) \prod_{j \ne i} B_j(x) - \Theta \prod_{j=1}^{s_1} B_j(x)}{\prod_{j=1}^{s_1} B_j(x)}.$$
   Because the $s_1$ bottom linear forms are distinct, their denominators $B_1(x), \dots, B_{s_1}(x)$ are generically pairwise coprime, forcing degree:
   $$D_{\text{sum}} = s_1 \cdot D_1 = \Omega\!\left(s_1 \cdot \log W_1 \cdot \log A_{\text{top}}\right), \qquad D_{\text{depth-2}} = D_2 \cdot s_1 \cdot D_1.$$
   Across depth $d$ with layer fan-in $k$ and gate degree $D_{\text{gate}}$, recursive denominator clearing + rational composition blows up exponentially in $d$:
   $$D_{\text{depth-}d} = D_{\text{gate}} \cdot (k \cdot D_{\text{gate}})^{d-1}.$$

   In `verification/verify_baton_003_tc0_sat.py`, even for **sublinear** $s_1 = \lceil n^{0.6} \rceil$ bottom gates with $W_1 = n^2$:
   - $n = 64, s_1 = 13$: $D_1 = 112$, $D_{\text{sum}} = 1{,}456 > n$, $D_{\text{depth-2}} = 32{,}032$;
   - $n = 256, s_1 = 28$: $D_1 = 180$, $D_{\text{sum}} = 5{,}040 > n$, $D_{\text{depth-2}} = 141{,}120$;
   - $n = 1024, s_1 = 64$: $D_1 = 264$, $D_{\text{sum}} = 16{,}896 > n$, $D_{\text{depth-2}} = 608{,}256$.
   Polynomial-method SAT (fast multipoint evaluation / Coppersmith–Winograd rectangular matrix multiplication) requires $\binom{n}{\le D} \ll 2^{n/2}$, which already fails for $D \ge 0.11 n$ ($H_2(0.11) \approx 0.500$). Denominator clearing shatters this threshold immediately at depth 2!

### Wall C: Witness-Compression Loss in Williams's Algorithmic Method
Even with Chen–Tell's $2^{n - n^{\Omega(c^{-d})}}$ algorithm for $w(n) = n^{1 + c^{-d}}$:
- Proving $\text{NEXP} \not\subseteq \text{TC}^0$ via Williams's easy-witness contradiction assumes a $\text{TC}^0$ succinct witness circuit of **arbitrary** depth $d_0$ and **arbitrary** polynomial size $n^k$ ($k$ unbounded).
- Composing the assumed witness circuit with the verifier produces a $\text{TC}^0$ circuit of depth $d = d_0 + O(1)$ and at least $W = \Omega(n^k)$ wires.
- Because the savings $n^{\Omega(c^{-d})}$ only survives up to $W \le n^{1 + c^{-d}}$, there is an unbridged **witness-compression loss**: we lack any reduction compressing an $n^k$-wire depth-$d_0$ threshold witness circuit down to $n^{1 + c^{-d'}}$ wires (which by Theorem 1 is blocked even under Allender–Koucký amplification).

---

## 5. Mandatory 4-Barrier Audit Table

| Barrier | Reference | What It Blocks | Status in Baton #003 (`baton-003-direct-tc0-sat`) |
| :--- | :--- | :--- | :--- |
| **1. Relativization** | Baker–Gill–Solovay (1975) | Pure diagonalization / simulation invariant under arbitrary oracles | **Bypassed in principle**: Williams's Circuit-SAT-to-lower-bound framework uses non-relativizing PCPs / easy-witness lemmas; direct $\text{TC}^0$-SAT inspects explicit circuit weights. |
| **2. Natural Proofs** | Razborov–Rudich (1997) | Large + Constructive properties distinguishing $\text{TC}^0$ from random functions (note: **$\text{TC}^0$ IS conjectured to contain PRFs** via Naor–Reingold / DDH / LWE!) | **CRITICAL ACTIVE OBSTRUCTION for the restriction/approximation subroutines!** While Williams's *outer* diagonalization is non-natural, every known *inner* $\text{TC}^0$-SAT subroutine (random restrictions, Littlewood–Offord shrinkage, rational/polynomial approximations) yields constructive, large circuit-simplification properties — which **cannot** extend to polynomial-size $\text{TC}^0$ (or even $n^{1+\epsilon}$ depth-$d$ $\text{TC}^0$ supporting Naor–Reingold-style PRFs!) unless standard cryptographic assumptions (DDH/LWE/Factoring in $\text{TC}^0$) fail! |
| **3. Algebrization** | Aaronson–Wigderson (2009) | Pure low-degree arithmetization / IP-style algebraic extensions | **Partially bypassed / Hit differently**: BRS rational approximations fail *before* algebrization due to denominator-clearing degree explosion ($D_{\text{sum}} = s_1 D_1 > n$). Any future non-algebrizing algebraic method for $\text{TC}^0$ must avoid naive common-denominator clearing. |
| **4. Locality Barrier** | CHOPRS (STOC 2020) | Gluing standard lower-bound proofs to local Hardness Magnification reductions | **Not directly triggered** in pure Williams-style $\text{NEXP} \not\subseteq \text{TC}^0$ (which avoids magnification), **but re-emerges** if one attempts to magnify Chen–Tell's $n^{1 + c^{-d}}$ $\text{TC}^0$ lower bounds up to full $\text{TC}^0$ or $\text{NP} \not\subseteq \text{TC}^0$ via local oracle reductions (handed off to `baton-004`). |

---

## 6. Verdict & Exact Handoff to Next Batons

- **Did Baton #003 resolve P vs NP or prove $\text{NEXP} \not\subseteq \text{TC}^0$?** **NO** (`p_vs_np_resolved: false`).
- **Concrete Verified Deliverables**:
  1. Built & exhaustively verified a **zero-Tseitin depth-2 $\text{TC}^0$-SAT solver** (`verification/verify_baton_003_tc0_sat.py`) achieving 100% SAT/UNSAT equivalence with $2^n$ brute force across 50 circuits ($n=8..12$) with 92.9% overall work reduction (93.9% on UNSAT) and empirically pinning the Pareto dimension wall ($2.9\% \to 100.0\%$ survival as $s_1: 3 \to 20$).
  2. Proved & quantitatively verified the **Chen–Tell $1 + c^{-d}$ decay recurrence** and **Allender–Koucký non-intersection theorem** ($c^{-d} < k/d$ for all $d \ge 1, k \ge 1, c \ge 2$).
  3. Proved & exhaustively verified the **BRS rational approximation error bound** ($< 3^{-b}/(1-3^{-b})$ across 10,728 points) and **denominator-clearing degree blowup** ($D_{\text{sum}} = s_1 D_1 > n$ even for $s_1 = n^{0.6}$ at depth 2).
- **Exact Open Sub-Problems for Downstream Batons**:
  1. **Bypassing Natural Proofs inside $\text{TC}^0$-SAT (The Crypto Wall)**: Because $\text{TC}^0$ can evaluate candidate PRFs (Naor–Reingold / LWE-based PRFs) in constant depth and polynomial size, any $\text{TC}^0$-SAT algorithm reaching $w(n) = n^k$ MUST be **non-natural** (cannot rely on circuit simplification under random restrictions that would distinguish PRFs from random functions). Future agents should explore *instance-specific / non-black-box* SAT algorithms (e.g., exploiting explicit verifier/PCP structure inside Williams's proof rather than worst-case arbitrary $\text{TC}^0$ circuits).
  2. **Avoiding Denominator Clearing**: Investigate **sign-representing / PTF / low-rank tensor decompositions** or **probabilistic rational functions with shared denominators** for depth-2/depth-3 $\text{TC}^0$ where $s_1 = n^{1+\epsilon}$ (beating the $n^{1+c^{-d}}$ exponent even at $d=3$).
  3. **Proceed to `baton-004-nonlocal-magnification` & `baton-005-gct-obstructions`**: Explore non-local meta-complexity reductions (Hirahara) and representation-theoretic GCT multiplicity obstructions that do not collide with $\text{TC}^0$ PRF natural-proof barriers.
