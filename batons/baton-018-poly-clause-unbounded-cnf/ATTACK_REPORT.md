# Baton #018: Polynomial-Clause Unbounded-Width CNF-SAT ($M = n^B$) vs. Valiant's $\Omega(n / \log\log n)$ Depth-Reduction Bridge

- **Target Millennium Problem**: P versus NP (Clay Mathematics Institute — **Unsolved** as of November 2026)
- **Baton ID**: `baton-018`
- **Node ID**: `baton-018-poly-clause-unbounded-cnf`
- **Dependencies**: `baton-014-cnf-sat-seth-unbounded-width`
- **Status**: `BLOCKED_BY_BARRIER` (Did **not** resolve P vs NP; implemented and verified the exact width-independent CNF-SAT $\to$ Orthogonal Vectors reduction and bit-parallel subtree-pruning OV solver 30/30 against brute force; derived and numerically verified the exact Abboud–Williams–Yu / Chan–Williams polynomial-method + rectangular-MM bottleneck equation across $M = n^2, n^3, n^5, n^{10}$ and $n = 100 \dots 2^{30}$; proved an intrinsic $\Theta((B-1)\log n / \log\log n)$ gap to Valiant's bridge that persists even under optimal $\omega = 2$ ($\alpha = 1$); discovered the exact boundary collision at $M = n \cdot \operatorname{polylog}(n)$; and proved via $\mathbb{F}_2$ pairwise independence + Chebyshev's inequality why probabilistic polynomial compression locks block savings at $O(n / \log(M/n))$)
- **Date**: 2026-11-26

---

## 1. Executive Mission & Connection to Baton #014

Baton #014 (`baton-014-cnf-sat-seth-unbounded-width`) sharpened the post-October-2026 fine-grained landscape by showing that **Linear-Clause Unbounded-Width CNF-SAT** ($\Delta = M/n = O(1)$, or $\log_2 \Delta = o(\log\log n / \log\log\log n)$) collapses to $2^{o(n)}$ via Ordered Schuler + IPZ + Oct2026, leaving **Polynomial-Clause Unbounded-Width CNF-SAT** ($M = n^B$, $B > 1$, clause widths $w = \omega(\log\log n / \log\log\log n)$) as the true surviving fortress of CNF-SAT-SETH.

At the same time, Baton #014 established that **Valiant's 1977 Depth-Reduction Bridge** reduces linear-size log-depth Circuit-SAT ($s = c n$, $d = c' \log_2 n$) to unbounded-width CNF-SAT (or sparse local-constraint SAT) provided one can achieve exponent savings $\sigma(n) = \omega(n / \log\log n)$ below $2^n$. Classical combinatorial width-splitting (**Schuler + PPZ**) stalls at $\sigma(n) = \Theta(n / \log(M/n))$, missing Valiant's threshold by $\Theta((B-1)\log n / \log\log n)$ at $M = n^B$.

**Core Question of Baton #018**: Can the strongest known **non-IPZ, non-branching, algebraic batch-evaluation** paradigm — **Split-and-Batch Orthogonal Vectors (OV)** combined with the **Abboud–Williams–Yu (SODA 2015) / Chan–Williams (SODA 2016) Polynomial Method + Rectangular Matrix Multiplication** — break past Schuler's $\Theta(n / \log(M/n))$ wall on $M = n^B$ unbounded-width CNF-SAT and reach Valiant's $\omega(n / \log\log n)$ threshold?

**Answer**: **NO — and the obstruction is exact, structural, and matrix-multiplication-independent.** Both combinatorial width-splitting (Schuler 2005) and algebraic polynomial-method batch evaluation (AWY15 / CW16) lock rigidly onto the **same** $\Theta(n / \log(M/n))$ savings ceiling. Even under optimal matrix multiplication ($\omega = 2 \iff \alpha = 1$), the polynomial method falls short of Valiant's threshold on $M = n^B$ by $\Theta((B-1)\log n / \log\log n)$ — and collides head-on with Valiant's $\Theta(n / \log\log n)$ scale precisely at the polylogarithmic clause density boundary $M = n \cdot (\log_2 n)^q$.

---

## 2. Theorem 1: Exact Width-Independent CNF-SAT $\to$ OV Reduction & Subtree-Pruning Audit (Check 1)

### 2.1 Reduction (Zero Width Dependence)

Let $\Phi(x_1, \dots, x_n) = \bigwedge_{j=1}^M C_j$ be **any** CNF formula on $n$ variables and $M$ clauses with completely arbitrary clause widths $k_j \in \{1, \dots, n\}$. Partition variables into two balanced halves $X_L = \{x_1, \dots, x_{n_1}\}$ and $X_R = \{x_{n_1+1}, \dots, x_n\}$ with $n_1 = \lfloor n/2 \rfloor$, $n_2 = \lceil n/2 \rceil$, and decompose each clause as $C_j = C_j^{(L)} \lor C_j^{(R)}$.

Define the $M$-bit **falsification indicator vectors** $u: \{0,1\}^{n_1} \to \{0,1\}^M$ and $v: \{0,1\}^{n_2} \to \{0,1\}^M$ by:
$$u(a)_j = 1 \iff C_j^{(L)}(a) = 0, \qquad v(b)_j = 1 \iff C_j^{(R)}(b) = 0.$$
Then for every $(a, b) \in \{0,1\}^{n_1} \times \{0,1\}^{n_2}$:
$$\Phi(a, b) = 1 \;\Longleftrightarrow\; \forall j \in [M],\; u(a)_j \cdot v(b)_j = 0 \;\Longleftrightarrow\; \langle u(a), v(b) \rangle = 0 \;\Longleftrightarrow\; (u(a) \mathbin{\&} v(b)) = 0.$$
Thus arbitrary-width CNF-SAT reduces identically (with **zero dependence on clause width $k$**) to **Orthogonal Vectors (OV)** on sets $U, V \subseteq \{0,1\}^d$ of sizes $N_1 = 2^{n_1}, N_2 = 2^{n_2}$ (balanced $N = 2^{n/2}$) and dimension $d = M$.

### 2.2 Exact Bit-Parallel + Subtree-Pruning OV Solver Verification

In `verification/verify_baton_018_poly_clause_cnf.py`, we pack each vector into an $M$-bit Python integer and organize $V$ into a coordinate-splitting binary trie storing at every node $S \subseteq V$ the exact invariant $\text{common\_ones}(S) = \bigwedge_{v \in S} v$ (bitwise AND). For any query $u \in U$:
1. If $u \mathbin{\&} \text{common\_ones}(S) \neq 0$, then every $v \in S$ shares at least one $1$-bit with $u$; the entire subtree $S$ is pruned in $O(1)$ bitmask time.
2. At splitting bit $j$, if $u_j = 1$, the $1$-child $S_1 = \{v \in S : v_j = 1\}$ is skipped completely.

**Empirical Result (Check 1)**: Across **30 random wide-CNF instances** ($n \in \{10, 11, 12, 13, 14\}$, $M = n^2 \in \{100, 121, 144, 169, 196\}$, every clause width $k \in [\lfloor n/2 \rfloor, n - 2]$: 10 uniform random SAT, 10 planted tight SAT, and 10 split-straddling wide-core UNSAT):
- **Brute-force equivalence**: **30 / 30 (100.0%)** exact SAT/UNSAT match and 100% verified satisfying witnesses.
- **Bit-parallel pruning speedup** (naive $2^n$ pairs vs. actual leaf bitmask checks): **10.40x overall**, **3.65x UNSAT-only** (`17,406` leaf checks vs. `63,488` naive pairs).

---

## 3. Theorem 2: Exact Abboud–Williams–Yu / Chan–Williams Polynomial-Method Bottleneck & Valiant Gap (Check 2)

### 3.1 Exact Derivation of the Rectangular-MM Degree-Entropy Equation

Given the OV instance $U, V \subseteq \{0,1\}^M$ of size $N = 2^{n/2}$ each:
1. **Block Partitioning**: Partition $U$ into $m = N / s$ blocks $A_1, \dots, A_m$ of size $s$ and $V$ into $m = N / s$ blocks $B_1, \dots, B_m$ of size $s$. Let $\sigma := 2 \log_2 s$, so $s^2 = 2^\sigma$ pairs per block and $m^2 = (N/s)^2 = 2^{n - \sigma}$.
2. **Probabilistic Polynomial for $\text{AND}_M$ over $\mathbb{F}_2$**: Draw $R \sim \operatorname{Uniform}(\mathbb{F}_2^{r_1 \times M})$ and form
   $$P_R(u, v) \;=\; \prod_{i=1}^{r_1} \left(1 + \sum_{j=1}^M R_{i,j} u_j v_j\right) \pmod 2.$$
   Since $u_j^2 = u_j$ and $v_j^2 = v_j$ over $\mathbb{F}_2$, every monomial in the product reduces multilinearly to the **diagonal bilinear form**:
   $$P_R(u, v) \;=\; \sum_{S \subseteq [M],\; |S| \le r_1} c_S(R) \cdot \left(\prod_{j \in S} u_j\right) \cdot \left(\prod_{j \in S} v_j\right) \pmod 2,$$
   whose exact inner feature dimension is
   $$L(M, r_1) \;=\; \sum_{k=0}^{r_1} \binom{M}{k}.$$
3. **Block-Level Schwartz–Zippel Batching**: To ensure that any non-orthogonal $s \times s$ block $(A_p, B_q)$ has false-positive probability $\le 2^{-7} = 1/128$ by union bound over $s^2 = 2^\sigma$ pairs, we set $r_1 = \lceil \sigma + 7 \rceil$. Choosing random block weights $\alpha, \beta \in \mathbb{F}_2^s$ and aggregating $\Phi(A_p) = \sum_{t=1}^s \alpha_t \tilde{\phi}(a_{p,t}) \in \mathbb{F}_2^L$, $\Psi(B_q) = \sum_{t'=1}^s \beta_{t'} \psi(b_{q,t'}) \in \mathbb{F}_2^L$:
   - On any block containing an orthogonal pair, $\Pr[\langle \Phi(A_p), \Psi(B_q) \rangle = 1] \ge 1/4$ (since $P_R$ has zero false negatives and $\alpha^T M \beta \neq 0$ with probability $\ge 1/4$ for any nonzero $\mathbb{F}_2$-matrix $M$).
   - On any block with no orthogonal pair, $\Pr[\langle \Phi(A_p), \Psi(B_q) \rangle = 1] \le 1/128$.
   Repeating $O(n)$ times boosts block accuracy to $1 - N^{-10}$ simultaneously across all $m^2$ blocks (and Chan–Williams SODA 2016 derandomizes this to deterministic $2^{n - \sigma + o(n)}$ via Chebyshev/symmetric polynomials).
4. **Rectangular Matrix Multiplication Constraint**: Computing the $m \times m$ product $\Phi \cdot \Psi^T$ in $m^{2 + o(1)} = 2^{n - \sigma + o(n)}$ time via rectangular matrix multiplication requires $L(M, r_1) \le m^{\alpha^*}$, where $\omega(1, \alpha^*, 1) = 2$ ($\alpha^* > 0.321334$ by Williams–Xu–Xu–Zhou, SODA 2024). Taking $\log_2$ yields the **exact Chan–Williams / AWY bottleneck equation**:
   $$\log_2\!\left(\sum_{k=0}^{\lceil \sigma + 7 \rceil} \binom{M}{k}\right) \;\le\; \frac{\alpha^*}{2} (n - \sigma).$$

### 3.2 Exact Asymptotic Solutions & Quantitative Verification Across Regimes (Check 2)

Writing $\gamma = \sigma / n$ and $\Delta = M / n$, Stirling's entropy expansion reduces the bottleneck equation to
$$\gamma \cdot \big(\log_2 \Delta - \log_2 \gamma + \log_2 e\big) \;=\; \frac{\alpha^*}{2} (1 - \gamma) + o(1),$$
whose asymptotic solution is
$$\sigma_{\text{CW}}(n, M) \;=\; \frac{\alpha^*}{2} \cdot \frac{n}{\log_2(M/n) + \log_2\log_2(M/n) + O(1)} \;=\; \Theta\!\left(\frac{\alpha^* n}{\log_2(M/n)}\right).$$

**Verified Quantitative Table for Polynomial-Clause Unbounded-Width CNF ($M = n^B$, $\alpha^* = 0.321334$, Check 2B)**:

| $B$ ($M = n^B$) | $n$ | $\sigma_{\text{CW}}(n)$ | Valiant Scale $n / \log_2\log_2 n$ | Ratio $\sigma_{\text{CW}} / \sigma_{\text{Val}}$ | Shortfall Factor | Normalized $\frac{\sigma_{\text{CW}}}{\sigma_{\text{Val}}} \cdot \frac{(B-1)\log_2 n}{\log_2\log_2 n}$ ($\to \frac{\alpha^*}{2} = 0.16067$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | $10^4$ | `6.634e+01` | `2.680e+03` | `0.024759` | `40.4x` | `0.08815` |
| 2 | $2^{20}$ | `5.782e+03` | `2.426e+05` | `0.023831` | `42.0x` | `0.11028` |
| 2 | $2^{30}$ | `4.362e+06` | `2.188e+08` | **`0.019935`** | **`50.2x`** | `0.12188` |
| 3 | $2^{30}$ | `2.451e+06` | `2.188e+08` | **`0.011202`** | **`89.3x`** | `0.13697` |
| 5 | $2^{30}$ | `1.314e+06` | `2.188e+08` | **`0.006005`** | **`166.5x`** | `0.14686` |
| 10 | $2^{30}$ | `6.109e+05` | `2.188e+08` | **`0.002792`** | **`358.2x`** | **`0.15362`** (95.6% of limit!) |

**Matrix-Multiplication Independence (Check 2C)**: Even under the strongest conceivable hypothesis $\omega = 2$ ($\alpha^* = 1.0$), at $B = 2, n = 2^{30}$ we obtain $\sigma_{\text{CW}} = 1.405 \times 10^7$ — still a **15.57x** shortfall that diverges monotonically as $\Theta((B-1)\log n / \log\log n)$. Thus **improving matrix multiplication cannot close the Polynomial-CNF vs. Valiant gap**.

### 3.3 Exact Boundary Collision at $M = n \cdot \operatorname{polylog}(n)$ (Check 2D)

Dropping $M$ from $n^B$ to **polylogarithmic density** $M = n \cdot (\log_2 n)^q$ sets $\log_2(M/n) = q \cdot \log_2\log_2 n$, causing $\sigma_{\text{CW}}$ to **collide directly onto Valiant's $\Theta(n / \log_2\log_2 n)$ threshold**:
$$\lim_{n \to \infty} \frac{\sigma_{\text{CW}}\big(n,\; n (\log_2 n)^q\big)}{n / \log_2\log_2 n} \;=\; \frac{\alpha^*}{2 q} \;=\; \Theta(1)!$$

| Clause-Count Regime $M(n)$ | Scale | $\sigma_{\text{CW}} / (n / \log_2\log_2 n)$ | Exact Limit | Status vs. Valiant $\omega(n/\log\log n)$ |
| :--- | :---: | :---: | :---: | :--- |
| $M = n \cdot (\log_2 n)^1$ | $\log_2 n = 30 \to 256 \to 2^{1000}$ | `0.06145` $\to$ `0.07903` $\to$ **`0.15841`** | `0.16067` ($\alpha^*/2$) | **Exact Boundary Collision ($\Theta(1)$)** |
| $M = n \cdot (\log_2 n)^2$ | $\log_2 n = 30 \to 256 \to 2^{1000}$ | `0.04321` $\to$ `0.05167` $\to$ **`0.07973`** | `0.08033` ($\alpha^*/4$) | **Exact Boundary Collision ($\Theta(1)$)** |
| $M = n \cdot (\log_2 n)^4$ | $\log_2 n = 30 \to 256 \to 2^{1000}$ | `0.02746` $\to$ `0.03088` $\to$ **`0.04001`** | `0.04017` ($\alpha^*/8$) | **Exact Boundary Collision ($\Theta(1)$)** |
| $M = n \cdot 2^{\sqrt{\log_2\log_2 n}}$ | $\log_2 n = 30 \to 900 \to 2^{1000}$ | `0.08096` $\to$ `0.14591` $\to$ **`3.89689`** | $+\infty$ | **Surpasses Valiant ($\omega(n/\log\log n)$)** |
| $M = n^B$ ($B > 1$) | $n = 2^{30}$ ($B = 2..10$) | `0.01994` $\dots$ `0.00279` | $0$ | **Blocked by $\Theta\big(\frac{(B-1)\log n}{\log\log n}\big)$ gap** |
| Valiant Raw $M = 2^{n^{0.25}}$ | $\log_2 n = 30$ | `4.848e-03` | $0$ | **Blocked by $\Theta(n^{0.25}/\log\log n)$ gap** |

**Complete Post-Oct-2026 5-Regime Synthesis (Baton #014 + Baton #018)**:
- $M = n \cdot 2^{o(\log\log n / \log\log\log n)}$: **Collapses to $2^{o(n)}$** via Schuler+IPZ+Oct2026 (Baton #014).
- $M = n \cdot 2^{\omega(\log\log n / \log\log\log n)}$ up to $n \cdot 2^{o(\log\log n)}$: Schuler+IPZ crashes, **but** Chan–Williams OV achieves $\omega(n / \log\log n)$ savings!
- $M = n \cdot (\log_2 n)^q$: **Exact Valiant threshold collision** ($\sigma_{\text{CW}} = \Theta(n / (q \log\log n))$).
- $M = n^B$ ($B > 1$): **True surviving Polynomial-Clause Fortress** ($\sigma_{\text{CW}} = \Theta(n / ((B-1)\log n))$, missing Valiant by $\Theta((B-1)\log n / \log\log n)$).
- $M = 2^{n^\epsilon}$: Valiant raw-CNF regime ($\sigma_{\text{CW}} = \Theta(n^{1-\epsilon})$, missing Valiant by $\Theta(n^\epsilon / \log\log n)$).

---

## 4. Theorem 3: Exact $\mathbb{F}_2$ Compression Rate & Pairwise-Independence Error-Boosting Wall (Check 3)

Why can't we compress the $M$-bit OV falsification vectors to $r \ll \sigma$ dimensions using $\mathbb{F}_2$ random linear combinations $y_R(u, v) = R(u \odot v) \in \mathbb{F}_2^r$ and thereby beat $\log(M/n)$?

### 4.1 Proof of the Pairwise-Independence Chebyshev Wall

1. **Exact Per-Pair Rate**: For any nonzero overlap $w = u \odot v \in \mathbb{F}_2^M \setminus \{0^M\}$ (independent of $M$ and Hamming weight $|w| \ge 1$), let $j^*$ satisfy $w_{j^*} = 1$. Conditioning on all columns $R_{:, j}$ ($j \neq j^*$), the column $R_{:, j^*}$ is uniform in $\mathbb{F}_2^r$, so $R w \sim \operatorname{Uniform}(\mathbb{F}_2^r)$ and $\Pr[R w = 0^r] = 2^{-r}$ **identically**; if $w = 0^M$, $\Pr[R w = 0^r] = 1$ (zero false negatives).
2. **Pairwise Independence of Distinct Overlap Patterns**: Let $W = \{w^{(1)}, \dots, w^{(K)}\} \subseteq \mathbb{F}_2^M \setminus \{0^M\}$ be the set of distinct nonzero overlap vectors occurring in an UNSAT instance (or a single $s \times s$ block). Any two distinct nonzero vectors $w^{(a)} \neq w^{(b)} \in \mathbb{F}_2^M \setminus \{0^M\}$ are **linearly independent over $\mathbb{F}_2$** (since $w^{(a)} + w^{(b)} \neq 0$). Hence the indicators $Z_t = \mathbf{1}[R w^{(t)} = 0^r]$ are **exactly pairwise independent** Bernoulli($2^{-r}$) variables!
3. **Chebyshev Lower Bound on $r$**: Setting $Z = \sum_{t=1}^K Z_t$, we have $\mathbb{E}[Z] = K 2^{-r}$ and $\operatorname{Var}(Z) = K 2^{-r}(1 - 2^{-r}) < \mathbb{E}[Z]$. By Chebyshev's inequality:
   $$\Pr[Z = 0] \;\le\; \frac{\operatorname{Var}(Z)}{(\mathbb{E}[Z])^2} \;<\; \frac{2^r}{K}.$$
   - **Global Compression ($K = \Theta(2^n)$)**: Suppressing false positives globally with probability $\ge 1/2$ forces $2^r \ge K/2 \implies r \ge \log_2 K - 1 = \Omega(n)$, which explodes the degree-$r$ monomial count $\binom{M}{r}$ past $2^{\Omega(n \log(M/n))} \gg 2^n$!
   - **Block Compression ($K_{\text{block}} = s^2 = 2^\sigma$)**: Suppressing false positives per block forces $r \ge \sigma - O(1)$, immediately enforcing $\log_2 \sum_{k=0}^r \binom{M}{k} \le \frac{\alpha^*}{2}(n - \sigma) \implies \sigma = O(n / \log(M/n))$.

### 4.2 Empirical Verification (Check 3A, 3B, 3C)

1. **Exact $2^{-r}$ Rate & Zero False Negatives (Check 3A)**: Across all 9 combinations $(M, r) \in \{64, 128, 256\} \times \{4, 8, 12\}$ mixing Hamming weights $|w| \in \{1, 2, M/4, M/2\}$ (`8,000`–`120,000` trials per cell):
   - **4,500 / 4,500** zero false negatives on $w = 0$.
   - All 9 empirical FP rates match exact $2^{-r}$ (`0.0625`, `0.003906`, `0.000244`) within standard binomial noise ($|z| \in [0.10, 3.19]$).
2. **Exact Diagonal Bilinear Monomial Expansion Identity (Check 3B)**: For $M = 10, r = 3$ ($L \le 176$ multilinear monomials), explicit DP construction of $c_S(R)$ verified $P_R(u, v) = \sum_{|S| \le 3} c_S \phi_S(u) \psi_S(v) \pmod 2$ on **500 / 500 (100%)** random pairs.
3. **Concrete UNSAT Wide-CNF Global-Compression Wall (Check 3C, $n = 12, M = 144$)**: Extracted $|W| = 569$ distinct nonzero overlap vectors ($\log_2 |W| = 9.15$):

| $r$ | Empirical $\Pr[\text{0 FPs}]$ | Chebyshev Bound $2^r / \|W\|$ | $\mathbb{E}[\text{FPs}] = \|W\| 2^{-r}$ | $\log_2 L(144, r)$ | Rect-MM Budget $\frac{\alpha^*}{2} n$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 4 | `0.0000` | `0.0281` | `35.562` | `24.08` | `1.93` |
| 8 | `0.1125` | `0.4499` | `2.223` | `41.86` | `1.93` |
| 12 | `0.9375` | `1.0000` | `0.139` | **`56.66`** | `1.93` |
| 16 | `0.9875` | `1.0000` | `0.009` | **`69.41`** | `1.93` |

Even at $n = 12$, pushing $r$ past $\log_2 |W| \approx 9.15$ to suppress false positives inflates the monomial dimension to $2^{56.66}$ — almost **30x** the log-budget of rectangular matrix multiplication!

---

## 5. Mandatory 4-Barrier Audit Table

| Barrier | Reference | What It Blocks | Status Under Baton #018 Findings |
| :--- | :--- | :--- | :--- |
| **1. Relativization** | Baker–Gill–Solovay (1975) | Oracle-invariant diagonalization / separation proofs | **Bypassable in Principle, Blocked by Quantitative Threshold.** The AWY15 / CW16 polynomial method is an *algorithmic* (white-box) method that feeds Williams's non-relativizing SAT-to-Lower-Bounds framework. However, because it stalls at $\sigma = \Theta(n / \log(M/n)) \ll \omega(n / \log\log n)$ on $M = n^B$ CNFs (and $\Theta(n^{1-\epsilon})$ on Valiant raw CNFs), it fails to trigger Williams's non-relativizing lower-bound engine for linear-size log-depth circuits. |
| **2. Natural Proofs** | Razborov–Rudich (1997) | Large + constructive combinatorial circuit properties (under $2^{n^\epsilon}$-hard PRFs) | **Bypassed by Paradigm, Not Yet Triggered.** Williams-style SAT algorithms yield *non-naturalizing* circuit lower bounds (via easy-witness + PCPs rather than large truth-table properties). No Natural Proofs violation occurs here because no super-linear log-depth lower bound is achieved; conversely, breaking $M = n^B$ CNF-SAT-SETH to $\omega(n/\log\log n)$ would not violate Razborov–Rudich unless it yielded $2^{n^\epsilon}$-time distinguishing of PRFs. |
| **3. Algebrization** | Aaronson–Wigderson (2009) | Pure low-degree arithmetization / algebraic extension proofs | **DIRECT QUANTITATIVE WALL HIT (Polynomial-Method Degree-Entropy Barrier).** While AWY15 / CW16 is an algorithmic (not proof-theoretic) application of low-degree polynomials over $\mathbb{F}_2$ / $\mathbb{Z}$, Check 2 and Check 3 expose the exact algebraic obstruction: representing $\text{AND}_M$ with one-sided error $2^{-r}$ forces polynomial degree $\Omega(r)$ and monomial entropy $r \log_2(e M / r)$. Pairwise independence of $\mathbb{F}_2$ linear hashes proves $r \ge \sigma - O(1)$ is unavoidable for generic $M$-dimensional OV, locking algebraic batch evaluation rigidly at $\sigma = O(n / \log(M/n))$ regardless of $\omega$. |
| **4. Locality Barrier** | CHOPRS (STOC 2020) | Gluing standard circuit lower bounds to local Hardness Magnification reductions | **Structurally Sidestepped (Different Target Regime).** Baton #018 attacks uniform Circuit-SAT / CNF-SAT-SETH via Valiant's depth-reduction bridge (targeting $\text{E}^{\text{NP}}$ / $\text{NEXP}$ super-linear log-depth bounds) rather than local MCSP magnification. However, the *clause-count vs. arity* tension mirrors locality: Valiant reduces to $O(n/\log\log n)$ local $n^\epsilon$-arity constraints, and flattening them to $M = 2^{n^\epsilon}$ destroys OV/polynomial-method efficiency. |

---

## 6. Verdict & Exact Handoff to Next Batons

- **Did Baton #018 resolve $\text{P}$ vs $\text{NP}$?** **NO.** (`p_vs_np_resolved: false`)
- **Status**: `blocked_by_barrier` — **Polynomial-Method Degree-Entropy & Pairwise-Independence Error-Boosting Wall Quantified**.
- **Exact Achievements**:
  1. Verified width-independent CNF-SAT $\to$ OV reduction + exact bit-parallel subtree-pruning OV solver (30/30 brute-force match across $n = 10..14$, $M = n^2$, widths $[n//2, n-2]$; 10.40x overall / 3.65x UNSAT pruning speedup).
  2. Derived and numerically verified the exact Abboud–Williams–Yu / Chan–Williams bottleneck equation across $M = n^2, n^3, n^5, n^{10}$ ($n = 100..2^{30}$), proving the $\Theta((B-1)\log n / \log\log n)$ shortfall persists even if $\omega = 2$ ($\alpha = 1$).
  3. Discovered the **exact boundary collision** at $M = n \cdot (\log_2 n)^q$ where $\sigma_{\text{CW}} / (n/\log_2\log_2 n) \to \alpha^*/(2q) = \Theta(1)$ (and exceeds Valiant for $M = n \cdot 2^{o(\log\log n)}$).
  4. Proved and empirically verified the exact $2^{-r}$ $\mathbb{F}_2$ compression rate, diagonal bilinear monomial expansion, and pairwise-independence Chebyshev wall forcing $r = \Omega(n)$ globally and locking block-batched OV to $O(n / \log(M/n))$.

### Concrete Handoff (What Must Break to Escape This Wall)
1. **Escape Route 18A — Non-Generic / Structured Local-Constraint SAT (Refining Sub-Lemma 14A)**: Generic OV treats the $M$ clauses as arbitrary unstructured coordinates, triggering our $\mathbb{F}_2$ pairwise-independence wall ($\binom{M}{r}$ monomials). Valiant's reduction does **not** produce arbitrary $M = n^B$ or $M = 2^{n^\epsilon}$ CNFs — it produces $m = O(n / \log\log n)$ **depth-$(\epsilon \log n)$ fan-in-2 subcircuits**! Attacking that representation directly (without flattening to $M$ clauses or generic OV) is the only surviving algebraic path to Valiant's $\omega(n/\log\log n)$ threshold.
2. **Escape Route 18B — Overcoming the $M = n \cdot \operatorname{polylog}(n)$ Collision by a Super-Constant Factor**: Notice how close $M = n \cdot (\log n)^q$ already is to Valiant ($\Theta(n / (q \log\log n))$)! Any *clause-compression* or *width-preserving sparsification* reducing $M = n^B$ unbounded-width CNFs to $2^{o(n / \log\log n)}$ instances with $M' = n \cdot 2^{o(\log\log n)}$ clauses would immediately compose with Chan–Williams OV to cross Valiant's threshold.
3. **Escape Route 18C — Non-Polynomial-Method Proof/Algorithm Paradigms**: Because both combinatorial Schuler width-splitting and algebraic AWY/CW polynomial batching independently converge to the identical $\Theta(n / \log(M/n))$ barrier, genuinely breaking Polynomial-Clause CNF-SAT-SETH requires a third mechanism (e.g., lifting the internal non-black-box structure of the October 2026 3-SAT algorithm directly to width $\Theta(\log n)$ without IPZ sparsification).
