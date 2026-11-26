# Baton #004: Attack on the CHOPRS Locality Barrier in Hardness Magnification & Hirahara's Non-Black-Box Reductions for MKtP / Gap-MCSP

- **Target Millennium Problem**: P versus NP (Clay Mathematics Institute — **Unsolved**)
- **Baton ID**: `baton-004` (`baton-004-nonlocal-magnification`)
- **Status**: `BLOCKED_BY_BARRIER` (Did **not** resolve P vs NP; rigorously analyzed the CHOPRS (STOC 2020) Locality Barrier, exact finite-domain `MCSP[s]` circuit complexity and local oracle decision trees, why Hirahara's non-black-box reductions evade black-box locality, and proved the **Non-Uniform Code-Size Paradox** plus two remaining structural walls blocking $\text{NP} \not\subseteq \text{P/poly}$)
- **Date**: 2026-11-26
- **Dependencies**: `route-1b-hardness-magnification`

---

## 1. Mission & Core Question

Baton #001 established that black-box Tseitin reductions from sub-exponential $3\text{-SAT}$ peak at $s^*(n) = \Theta(n\sqrt{\log n})$ and diagnosed that gluing super-linear circuit lower bounds to **Hardness Magnification** hits the **CHOPRS (STOC 2020) Locality Barrier**. Baton #004 directly attacks this barrier:

> **Core Question of Baton #004**:
> 1. Why do standard Hardness Magnification theorems (Oliveira–Santhanam 2018; Oliveira–Pich–Santhanam 2019; Chen–Jinan–Tell–Williams 2019) inevitably construct small-depth / small-fan-in local oracle reductions, and why does this unconditionally neutralize standard lower-bound techniques?
> 2. How do Shuichi Hirahara's *non-black-box* worst-case-to-average-case reductions (Symmetry of Information for $K^t$, NW/DPG reconstruction with explicit code substitution) bypass black-box locality?
> 3. What exact mathematical obstructions still block this non-black-box route from reaching $\text{NP} \not\subseteq \text{P/poly}$?

---

## 2. Anatomy of Standard Hardness Magnification & Local Oracle Reductions

### 2.1 The Magnification Mechanism (OS18, OPS19, CJTW19)

Consider a meta-complexity problem on Boolean truth tables $f \in \{0,1\}^N$ where $N = 2^n$:
- **$\text{MCSP}[s(N)]$**: Decide whether $f$ is computed by a Boolean circuit of size $\le s(N)$.
- **$\text{Gap-MCSP}[s_1(N), s_2(N)]$**: Distinguish YES instances ($\text{CC}(f) \le s_1$) from NO instances ($\text{CC}(f) > s_2$).
- **$\text{Gap-MKtP}[s_1(N), s_2(N)]$**: Distinguish low Levin time-bounded Kolmogorov complexity ($\text{Kt}(f) \le s_1$) from high ($\text{Kt}(f) > s_2$).

Standard Hardness Magnification theorems (Oliveira–Santhanam FOCS 2018; Oliveira–Pich–Santhanam CCC 2019; Chen–Jinan–Tell–Williams FOCS 2019) prove statements of the form:
$$\text{Gap-MCSP}[s_1, s_2] \notin \mathcal{C}\text{-SIZE}[N^{1+\epsilon}] \implies \text{NP} \not\subseteq \mathcal{C}$$
for circuit classes $\mathcal{C} \in \{\text{P/poly}, \text{NC}^1, \text{TC}^0, \text{Formula}, \text{BP}\}$ and sublinear thresholds $s_1(N) = N^\beta$ ($0 < \beta \ll \epsilon$).

The proof proceeds by contrapositive: assume $\text{NP} \subseteq \text{SIZE}[m^c]$ for some constant $c \ge 1$, and construct a circuit of size $O(N^{1+\epsilon})$ for $\text{Gap-MCSP}[s_1, s_2]$:

1. **Anti-Checker / Local Projection Lemma (Lipton–Young 1994; OS18; CJTW19)**:
   There are at most $2^{O(s_1 \log s_1)}$ circuits of size $s_1$ on $n = \log_2 N$ inputs. For a function $f$ that is $\delta$-far from every size-$s_1$ circuit (or after applying local list-decodable error correction / sparse-language hashing in CJTW19), a random coordinate subset $S \subseteq [N]$ of size
   $$m = |S| = O\!\left(\frac{s_1 \log s_1}{\delta}\right) = \tilde{O}(s_1) = N^{\beta + o(1)} \ll N$$
   witnesses that no size-$s_1$ circuit matches $f|_S$ with probability $\ge 1 - 2^{O(s_1 \log s_1)}(1-\delta)^m \ge 2/3$.
2. **Amplification & Derandomization (Non-Uniform Fixing)**:
   Repeating $t = O(N)$ independent samples $S_1, \dots, S_t \subseteq [N]$ reduces the failure probability below $2^{-N}$, so by a union bound over all $2^N$ truth tables there exists a **fixed** family $S_1, \dots, S_t$ (each of size $m \ll N$) such that:
   $$\text{Gap-MCSP}[s_1, s_2](f) \;=\; \bigwedge_{i=1}^{t} \mathcal{O}_{s_1, S_i}\!\left(f|_{S_i}\right)$$
   where $\mathcal{O}_{s_1, S}(w) = \mathbb{I}[\exists\, C \text{ of size } \le s_1 \text{ matching } w \text{ on } S]$ is an $\text{NP}$ predicate on inputs of length **only $m = \tilde{O}(s_1) \ll N$**!
   Equivalently, in decision-tree / adaptive sparse-language formulations (CJTW19; CHOPRS20), the reduction builds a **small-depth oracle decision tree** (depth $d \ll N$, or $O(N)$-fan-in AND/OR of short-arity oracle gates) querying $\mathcal{O}_m$ on local projections $f|_{S_i}$.
3. **Substituting the $\text{NP} \subseteq \text{SIZE}[m^c]$ Assumption**:
   Each local oracle gate $\mathcal{O}_m$ is replaced by a circuit of size $m^c = N^{c\beta + o(1)}$. Total circuit size:
   $$S_{\text{mag}}(N) = O(N) \cdot m^c = O\!\left(N^{1 + c\beta + o(1)}\right)$$
   Choosing $\beta < \epsilon / c$ yields $S_{\text{mag}}(N) \le N^{1+\epsilon}$!

### 2.2 Parameter-Window Collapse for $\text{P/poly}$

**Proposition 1 (Magnification Parameter-Window Collapse — Verified in `verify_baton_004_magnification_locality.py`)**:
To separate $\text{NP}$ from **all** of $\text{P/poly} = \bigcup_{c \ge 1} \text{SIZE}[n^c]$ using a fixed frontier lower bound $\text{Gap-MCSP}[s_1, s_2] \notin \text{SIZE}[N^{1+\epsilon}]$, the threshold $s_1(N) = N^\beta$ must satisfy:
$$\beta < \frac{\epsilon}{c} \quad \forall\, c \ge 1 \implies s_1(N) = N^{o(1)} \quad\text{and}\quad m(N) = \tilde{O}(s_1(N)) = N^{o(1)} \ll N.$$
Thus the oracle fan-in $m(N)$ is forced to be **sub-polynomial** ($N^{o(1)}$, e.g. $\text{polylog}(N)$) in the input length $N$!

---

## 3. The CHOPRS (STOC 2020) Locality Barrier

Chen, Hirahara, Oliveira, Pich, Rajgopal, and Santhanam (STOC 2020, *"Beyond Natural Proofs: Hardness Magnification and Locality"*) identified a **strictly unconditional** obstruction embedded in every magnification proof of the above form:

### 3.1 The Unconditional Local-Oracle Upper Bound

Notice that Steps 1–2 of Section 2.1 **never use the assumption $\text{NP} \subseteq \text{P/poly}$**! Unconditionally, the target meta-complexity problem $Q = \text{Gap-MCSP}[s_1, s_2]$ lies in the **local-oracle circuit class**:
$$Q \;\in\; \mathcal{C}\text{-SIZE}[O(N)]^{\mathcal{O}[m]} \quad (\text{and for low-depth reductions, } \text{DT}_d^{\mathcal{O}[m]} \text{ or } \text{AND}_{O(N)} \circ \mathcal{O}[m])$$
where $\mathcal{O}[m]$ denotes arbitrary (possibly computationally unbounded!) oracle gates of fan-in $m = N^{o(1)} \ll N$.

### 3.2 Why Standard Lower-Bound Techniques Relativize to Local Oracles

**Theorem (CHOPRS Locality Barrier, STOC 2020 — Structural Summary)**:
Let $\mathcal{T}$ be a lower-bound technique aiming to prove $Q \notin \mathcal{C}\text{-SIZE}[N^{1+\epsilon}]$. If $\mathcal{T}$ is *local-oracle invariant* — i.e., any lower bound proved by $\mathcal{T}$ against $\mathcal{C}\text{-SIZE}[s]$ also holds against $\mathcal{C}\text{-SIZE}[s]^{\mathcal{O}[m]}$ for oracle fan-in $m = N^{o(1)}$ — then **$\mathcal{T}$ mathematically cannot prove $Q \notin \mathcal{C}\text{-SIZE}[N^{1+\epsilon}]$**, because $Q$ is unconditionally computed inside $\mathcal{C}\text{-SIZE}[O(N)]^{\mathcal{O}[m]}$!

Why do almost all classical circuit lower-bound techniques fail this test?
1. **Random Restrictions & Switching Lemmas (Håstad, Subbotovskaya, Tal, Rossman)**:
   Under a random restriction leaving $pN$ variables alive with $p \ll 1/m$, an oracle gate of fan-in $m$ has all inputs fixed (or shrinks to tiny arity) with high probability; shrinkage exponents for De Morgan formulas ($\Gamma = 2$) and $\text{AC}^0$ switching lemmas extend with negligible degradation to $m$-local oracle gates.
2. **Polynomial Approximations (Razborov–Smolensky for $\text{AC}^0[p]$)**:
   Any Boolean function on $m$ bits has an exact multilinear polynomial of degree at most $m = N^{o(1)}$. Replacing each $m$-local oracle gate multiplies the approximating degree by at most $m = N^{o(1)}$, preserving the $\text{AC}^0[p]$ degree upper bound $o(\sqrt{N})$.
3. **Subfunction Counting (Nečiporuk / Khrapchenko for Formulas & Branching Programs)**:
   In a partition of $[N]$ into blocks of size $b \gg m$, an oracle gate of fan-in $m$ touching a block contributes at most $m$ boundary wires, so Nečiporuk's subfunction-counting bound degrades by at most an $m = N^{o(1)}$ factor.
4. **Unconditional Character (Stronger than Natural Proofs)**:
   Unlike Razborov–Rudich (1997), which assumes the existence of cryptographic PRFs inside $\mathcal{C}$, the CHOPRS Locality Barrier is **100% unconditional**: no cryptographic assumption is needed to prove that $\mathcal{T}$ cannot separate $Q$ from $\mathcal{C}\text{-SIZE}[O(N)]^{\mathcal{O}[m]}$.

---

## 4. Exact Finite-Domain Verification (`n = 3`, `N = 8`)

To ground the abstract theory in an exact, self-certifying computational testbed, `verification/verify_baton_004_magnification_locality.py` computes the **exact** minimum DAG circuit complexity (with full gate sharing, NOT merely formula size!) for all $2^8 = 256$ Boolean functions on $n = 3$ variables over fan-in-2 $\{\text{AND}, \text{OR}, \text{NOT}\}$ (counting binary gates with free wire inverters, i.e., AIG / De Morgan-with-internal-NOT complexity). Every witness circuit across all 14 NPN equivalence classes is independently re-evaluated on all 8 inputs.

### 4.1 Exact `MCSP[s]` Distribution for `n = 3` (`N = 8`)

| Exact DAG Size $s$ | Count of Functions | Cumulative $\text{MCSP}[s]$ (YES) | YES Density | NO Density ($\neg\text{MCSP}[s]$) | Representative NPN Functions |
| :---: | :---: | :---: | :---: | :---: | :--- |
| $0$ | $8$ | $8$ | $0.03125$ | $0.96875$ | Constants $0,1$ (`0x00`), literals $x_i, \neg x_i$ (`0x0f`) |
| $1$ | $24$ | $32$ | $0.12500$ | $0.87500$ | 2-literal $\text{AND}/\text{OR}$ (`0x03`) |
| $2$ | $64$ | $96$ | $0.37500$ | $0.62500$ | 3-literal minterms (`0x01`), $(x_0 \land x_1) \lor x_2$ (`0x07`) |
| $3$ | $30$ | $126$ | $0.49219$ | $0.50781$ | $\text{MUX}_3$ (`0x1b`), 2-var $\text{XOR}$ (`0x3c`) |
| $4$ | $104$ | $230$ | $0.89844$ | $0.10156$ | $\text{MAJ}_3$ (`0x17`), $(x_0 \oplus x_1) \land x_2$ (`0x06`, `0x19`, `0x1e`) |
| $5$ | $8$ | $238$ | $0.92969$ | $0.07031$ | $(x_0 x_1 \bar{x}_2) \lor (\bar{x}_0 \bar{x}_1 x_2)$ (`0x18`) |
| $6$ | $18$ | $256$ | $1.00000$ | $0.00000$ | $\text{EXACT-1}_3$ (`0x16`, 16 funcs), $\text{PARITY}_3$ (`0x69`, 2 funcs) |

### 4.2 Exact Density vs. Razborov–Rudich Largeness (Two-Level Distinction)

- On $n = 3$ at small threshold $s = 1$: $\text{MCSP}[1]$ YES-instances have low density $32/256 = 0.125$, while NO-instances (hard functions) have density $224/256 = 0.875 \gg 1/N$.
- Asymptotically (verified at $n \in \{8, 10, 12, 16\}$ with $s(N) = \lceil N^\beta \rceil$): by Shannon/Lupanov circuit counting, at $n = 12$ ($N = 4096$, $s = N^{0.25} = 8$), $\log_2 \mu(\text{MCSP}[s]) \le -4018.1$.
- **Critical Two-Level Subtlety**:
  - $\text{MCSP}[s]$ is **exponentially sparse** on YES-instances ($\mu \le 2^{-\Omega(N)}$), which enables CJTW19 sparse-language magnification.
  - Its complement $\neg\text{MCSP}[s]$ (the circuit-hardness property on $n$-variable functions) has density $\ge 1 - 2^{-\Omega(N)}$, **massively satisfying Razborov–Rudich Largeness** ($\ge 2^{-O(\log N)}$).
  - Even if PRFs did not exist in $\text{SIZE}[N^{1+\epsilon}]$ (neutralizing Natural Proofs at the $N$-input level), the CHOPRS Locality Barrier remains **unconditionally active**.

### 4.3 Concrete Depth $d \le 3$ Local Oracle Decision Tree Results

Simulating short-circuiting local oracle decision trees querying local projections $f|_S$ (fan-in $m < N = 8$) yields **100% completeness and 100% soundness**:

| Finite-Domain Problem | $|\text{YES}|$ | $|\text{NO}|$ | Tree Depth $d$ | Oracle Fan-in $m$ | Queries | Avg NO Queries | Exact Separation? |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: |
| $\text{Gap-MCSP}[0, 3]$ | $8$ | $160$ | $d = 3$ | $m = 4 = N/2$ | Subcubes `x0=0`, `x1=0`, `x2=0` | $1.30$ | **100% Exact** |
| $\text{Gap-MCSP}[0, 4]$ | $8$ | $130$ | $d = 2$ | $m = 4 = N/2$ | Subcubes `x0=0`, `x0=1` | $1.22$ | **100% Exact** |
| $\text{Gap-MCSP}[1, 6]$ | $32$ | $18$ | $d = 2$ | $m = 4 = N/2$ | Subcubes `x0=0`, `x0=1` | $1.44$ | **100% Exact** |
| $\text{Gap-MCSP}[2, 6]$ | $96$ | $18$ | $d = 2$ | $m = 4 = N/2$ | Subcubes `x0=0`, `x0=1` | $1.44$ | **100% Exact** |
| $\text{Gap-MCSP}[1, 5]$ | $32$ | $26$ | $d = 2$ | $m = 5$ | Subsets `(0..4)`, `(0..3,5)` | $\le 2$ | **100% Exact** |

- **Tight Anti-Checker Locality Boundary**: Function `0x18` (exact circuit size $5$) agrees with a size-$1$ circuit on **every** 2D subcube (`x_i = b`, fan-in $m=4$), fooling all six $m=4$ subcube consistency oracles simultaneously. Raising fan-in by a single bit ($m=5$, still $< N=8$) achieves 100% separation in depth $d=2$, concretely visualizing the exact anti-checker threshold $m = \Theta(s_1 \log s_1)$.

---

## 5. Hirahara's Non-Black-Box Program: How It Evades Black-Box Locality & What Exact Gap Remains

### 5.1 Mechanism of Hirahara's Non-Black-Box Reductions (FOCS 2018, STOC 2021, FOCS 2022)

Hirahara's landmark sequence of papers (FOCS 2018 *"Non-Black-Box Worst-Case to Average-Case Reductions within NP"*; FOCS 2022 *"Symmetry of Information from Meta-Complexity"*; Hirahara–Nanashima STOC 2024) avoids black-box barriers (both Bogdanov–Trevisan 2006 and CHOPRS black-box locality) via **explicit code substitution into PRG reconstruction**:

1. **Algorithm as PRG Distinguisher**:
   Assume a polynomial-time algorithm $M$ solves $\text{Gap-MK}^t\text{P}$ (or $\text{Gap-MCSP}$) on average ($\text{HeurBPP}$ / $\text{AvgP}$). Apply the **Nisan–Wigderson (NW)** generator or **Direct Product Generator (DPG)** $G_x(z)$ to a hard string $x \in \{0,1\}^N$. Outputs of $G_x$ have low $K^t$-complexity ($\le \ell + O(\log N)$), while uniform strings have $K^t \ge N - O(1)$. Hence $M$ distinguishes $G_x(U_\ell)$ from $U_N$.
2. **Non-Black-Box Reconstruction + Code-Size Accounting**:
   Standard NW/DPG reconstruction yields an oracle algorithm $R^M$ that reconstructs $x$ from short advice $\alpha(x)$ ($|\alpha(x)| \ll N$). A black-box reduction stops at $K^{t', M}(x) \le |\alpha(x)|$. **Hirahara explicitly hardwires the Turing machine description $\langle M \rangle$ into $R^M$**, yielding an *unrelativized* time-bounded Kolmogorov upper bound:
   $$K^{t'}(x) \;\le\; |R| + |\langle M \rangle| + |\alpha(x)| \;=\; O(1) + |\alpha(x)| \;\ll\; N.$$
   Combined with **Symmetry of Information** for $K^t$ ($K^{\text{poly}(t)}(x, y) \approx K^t(x) + K^{\text{poly}(t)}(y \mid x)$), this yields non-black-box worst-case-to-average-case reductions such as:
   $$\text{Gap}_{\text{poly}}\text{-MK}^t\text{P} \in \text{HeurBPP} \implies \text{NP} \subseteq \text{DTIME}\!\left(2^{O(n/\log n)}\right) \quad\text{and}\quad \text{DistNP} \subseteq \text{AvgBPP}.$$

### 5.2 Exact Proof of Why Hirahara Evades CHOPRS Black-Box Locality

Suppose we try to relativize Hirahara's proof by replacing $M$ with a CHOPRS local oracle $\mathcal{O}_m$ of fan-in $m = N^\beta \ll N$.
- An arbitrary (unbounded) oracle $\mathcal{O}_m : \{0,1\}^m \to \{0,1\}$ has description length $|\langle \mathcal{O}_m \rangle| = 2^m$ bits.
- For any magnification fan-in $m = \omega(\log N)$ (e.g., $m = N^{0.25} \log N$), we have:
  $$|\langle \mathcal{O}_m \rangle| = 2^m \gg N.$$
- Therefore, hardwiring $\mathcal{O}_m$ into $R^{\mathcal{O}_m}$ blows up the Kolmogorov complexity upper bound to $2^m + |\alpha(x)| \gg N$ — **completely destroying the proof**!
Hence Hirahara's code-substitution step is **genuinely non-black-box and does NOT relativize to CHOPRS local oracles**.

### 5.3 The Exact Remaining Gap to $\text{NP} \not\subseteq \text{P/poly}$ (Three Hard Walls)

Despite genuinely breaking black-box locality in the uniform setting, **three exact obstructions** prevent this approach from yielding $\text{NP} \not\subseteq \text{P/poly}$:

1. **Wall 1 — The Non-Uniform Code-Size Paradox (Fatal to Non-Uniform Magnification)**:
   To rule out $\text{NP} \subseteq \text{P/poly}$ via non-uniform Hardness Magnification, we must defeat a **non-uniform circuit** $C$ of size $N^{1+\epsilon}$ solving $\text{Gap-MKtP}$ / $\text{Gap-MCSP}$ on $N$-bit truth tables.
   - If we attempt to hardwire $C$'s description into $R^C$ (Hirahara's non-black-box step), the resulting description length is:
     $$|R| + |\langle C \rangle| + |\alpha(x)| \;\ge\; N^{1+\epsilon} \;>\; N \qquad (\forall\, N \ge 2,\; \epsilon > 0).$$
   - Because EVERY $N$-bit string trivially has Kolmogorov complexity $\le N + O(1)$, a description of length $> N$ proves **nothing**!
   - To get non-trivial compression ($< N$), we must have $|\langle C \rangle| \ll N$ — which holds ONLY if either (a) $C$ is **uniform** ($|M| = O(1)$, yielding only uniform consequences, not $\text{P/poly}$), or (b) $C$ is **sublinear / local** (reading only $m \ll N$ bits — which drops immediately **back into the CHOPRS Locality Barrier**!).
   - Verified quantitatively in `verify_baton_004_magnification_locality.py` (Test 4):
     $$\underbrace{|M| + \text{advice}}_{\text{Uniform Hirahara}} \;<\; N \;<\; \underbrace{|C| = N^{1+\epsilon}}_{\text{Non-Uniform Circuit}} \;\ll\; \underbrace{|\mathcal{O}_m| = 2^m}_{\text{Unbounded Local Oracle}}.$$

2. **Wall 2 — Conditional Equivalence vs. Unconditional Lower Bound**:
   Hirahara's theorems are *reductions* (e.g., $\text{Gap-MK}^t\text{P} \in \text{HeurBPP} \implies \text{NP} \subseteq \text{DTIME}(2^{O(n/\log n)})$). Concluding $\text{P} \neq \text{NP}$ or $\text{NP} \not\subseteq \text{P/poly}$ still requires an **unconditional lower bound** for $\text{Gap-MK}^t\text{P}$ (or $\text{Gap-MCSP}$). Current unconditional bounds for general $B_2$ circuits over $\text{NP}$ stand at $(3 + 1/86)N - o(N)$ (Find–Golovnev–Hirsch–Kulikov 2016; Li–Yang STOC 2022) — strictly linear, not even $\omega(N)$, let alone $N^{1+\epsilon}$ or $\text{HeurBPP}$.

3. **Wall 3 — Parameter-Window Mismatch**:
   Local magnification requires the lower bound to hold at exponentially sparse thresholds $s_1(N) = N^{o(1)}$ (Proposition 1), while known unconditional meta-complexity lower bounds (such as Hirahara–Santhanam's $\Omega(N^{2-o(1)})$ formula bound for $\text{MCSP}$) only hold in denser regimes or use local-oracle-invariant methods (Nečiporuk / shrinkage) that cannot cross the CHOPRS barrier. Moreover, Hirahara's $K^{\text{poly}(t)}$ vs $K^t$ polynomial time-bound gap prevents tight constant-factor magnification without losing the sparse window.

---

## 6. Mandatory Four-Barrier Audit Table

| Barrier | Reference | What It Blocks | Status for Baton #004 (Local Magnification vs. Hirahara Non-Black-Box) |
| :--- | :--- | :--- | :--- |
| **1. Relativization** | Baker–Gill–Solovay (1975) | Pure oracle-invariant diagonalization / simulation | **Bypassed** by Hirahara's non-black-box code substitution ($|\langle M\rangle| = O(1)$ fails relative to random/unbounded oracles) and by non-relativizing PCP/arithmetization in magnification. |
| **2. Natural Proofs** | Razborov–Rudich (1997) | Large + constructive properties separating $\text{P/poly}$ (assuming PRFs exist) | **Subtle / Partially Bypassed**: $\text{MCSP}[s]$ is exponentially sparse ($\mu \le 2^{-\Omega(N)}$), whereas $\neg\text{MCSP}[s]$ is overwhelmingly large ($\ge 1 - 2^{-\Omega(N)}$). Even without PRFs in $\text{SIZE}[N^{1+\epsilon}]$, CHOPRS blocks standard proofs unconditionally. |
| **3. Algebrization** | Aaronson–Wigderson (2009) | Arithmetization / low-degree extensions invariant under algebraic oracles | **Bypassed in principle** by non-black-box code substitution (an algebraic oracle $\tilde{\mathcal{O}}$ still has exponential description size), though open for algebraic magnification variants. |
| **4. Locality Barrier** | CHOPRS (STOC 2020) | Gluing local-oracle-invariant lower bounds to Hardness Magnification | **ACTIVE BLOCKER** for all known non-uniform local magnification routes; **Bypassed** in uniform setting by Hirahara's code-size accounting, but **Re-Triggered / Trapped** in non-uniform setting by the **Non-Uniform Code-Size Paradox** ($|C| = N^{1+\epsilon} > N$). |

---

## 7. Verdict & Concrete Handoff to Future Batons

- **Did Baton #004 prove $\text{P} \neq \text{NP}$ or bypass CHOPRS for $\text{NP} \not\subseteq \text{P/poly}$?** **NO.**
- **Concrete Verified Contributions of Baton #004**:
  1. Certified exact DAG circuit complexity distribution for all 256 Boolean functions on $n = 3$ ($N = 8$, 14 NPN classes, 100% witness-verified) via `verification/verify_baton_004_magnification_locality.py`.
  2. Verified exact depth $d \le 3$ local oracle decision trees (`Gap-MCSP[0,3]`, `[0,4]`, `[1,6]`, `[2,6]`, `[1,5]`) and the tight `0x18` anti-checker fan-in boundary ($m=4$ vs $m=5$).
  3. Quantitatively verified the CHOPRS parameter-window collapse ($\beta < \epsilon / c \to 0$), the two-level Razborov–Rudich density profile, and the **Non-Uniform Code-Size Paradox** ($|M|+\text{advice} < N < |C|=N^{1+\epsilon} \ll |\mathcal{O}_m|=2^m$).
- **Actionable Surviving Directions for Next Batons**:
  1. **Non-Local Magnification Theorems**: Construct a magnification theorem whose unconditional oracle reduction does *not* factor through $m = N^{o(1)}$-local oracle gates (e.g., global algebraic/interactive encodings where every query depends on $\Omega(N)$ bits of the truth table — avoiding the CHOPRS local-oracle class).
  2. **Uniform Bootstrapping & Non-Uniform Compression Bypass**: Investigate Chen–Tell (FOCS 2021) / Chen–Hirahara–Ren (STOC 2023) bootstrapping techniques that lift uniform or low-advice non-black-box lower bounds ($\text{S}_2\text{E}$, $\text{O}_2\text{P}$, $\text{MA}$) without hardwiring an entire $N^{1+\epsilon}$-size circuit into an $N$-bit string's description.
  3. **Unconditional Average-Case Meta-Complexity Bounds Against Restricted Classes**: Prove unconditional average-case lower bounds for $\text{Gap-MK}^t\text{P}$ against $\text{TC}^0$ or $\text{NC}^1$ (linking synergistically with `baton-003-direct-tc0-sat`).
