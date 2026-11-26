# Baton #012: Walking into the $\text{AC}^0[2]$-Frege / $\text{Res}(\oplus)$ / Polynomial Calculus ($\mathbb{F}_2$) Crack

- **Target Millennium Problem**: P versus NP (via Cook–Reckhow $\text{NP} \neq \text{coNP} \implies \text{P} \neq \text{NP}$) — **Unsolved**
- **Baton ID**: `baton-012`
- **Node ID**: `baton-012-ac0-mod2-frege-php`
- **Status**: `VERIFIED` (Did **not** resolve P vs NP or prove super-polynomial DAG $\text{Res}(\oplus)$ / $\text{AC}^0[2]$-Frege lower bounds on $\text{PHP}_n^{n+1}$; **computed exact $\mathbb{F}_2$ Polynomial Calculus (`PC`) and Static Nullstellensatz (`NS`) refutation degrees and zero-trust-verified dual witnesses** for $\text{FPHP}_n^{n+1}$ ($n = 2, 3, 4$) and $\text{Count}_3(m)$ ($m = 4, 5, 7, 8, 10$), **discovered & proved two strict dynamic-PC vs static-NS separations** (`FPHP_4^5`: $3 < 4$; `Count_3(7)`: $2 < 3$), **mechanically verified zero-trust $\text{Res}(\oplus)$ $O(|E|)$-Gaussian refutations** of $\text{Tseitin}(K_4, K_5, K_6, \text{Heawood})$, proved the **Frobenius Linear-Extension Degree Invariance Theorem**, and isolated the exact **Linear-Restriction / Error-Accumulation Wall** blocking lifting $\text{PC}/\mathbb{F}_2$ dual witnesses to DAG $\text{Res}(\oplus)$ and $\text{AC}^0[2]$-Frege)
- **Date**: 2026-11-26
- **Dependencies**: `baton-006-proof-complexity-ef`
- **Verification Script**: `verification/verify_baton_012_ac0_mod2_frege.py`

---

## 1. Why $\text{AC}^0[2]$-Frege / $\text{Res}(\oplus)$ Is the Cleanest Unblocked Crack in Proof Complexity

Baton #006 established that proof-complexity lower bounds above $\text{AC}^0$-Frege collide with cryptographic **Feasible Interpolation** (Krajíček–Pudlák 1998; Bonet–Pitassi–Raz 2000; BDGMP 2004) and **Self-Referential Reflection** (Pich–Santhanam 2021) once the proof lines reach $\text{TC}^0$-Frege, Frege, or Extended Frege ($\text{EF}$). Between conquered $\text{AC}^0$-Frege (Ajtai 1988; PBI 1993; KPW 1995; Håstad 2020) and cryptographically fortified $\text{TC}^0$-Frege sits one of the narrowest surviving cracks in all of complexity theory:

$$\text{Resolution} \;<\; \text{PC}/\mathbb{F}_2 \;<\; \text{Res}(\oplus) \;(\text{depth-2 }\text{AC}^0[2]\text{-Frege}) \;<\; \text{AC}^0[2]\text{-Frege} \;<\; \text{TC}^0\text{-Frege}.$$

Why this crack is uniquely prized:
1. **No cryptographic PRF obstruction**: By Razborov (1987) and Smolensky (1987), $\text{AC}^0[2]$ circuits cannot compute $\text{MAJ}$ or $\text{MOD}_3$ in sub-exponential size; strong pseudorandom functions (PRFs) and RSA/factoring arithmetic are **not** believed to live in $\text{AC}^0[2]$. Thus the Natural Proofs / cryptographic Feasible Interpolation barrier that kills $\text{TC}^0$-Frege does **not** immediately kill $\text{AC}^0[2]$-Frege!
2. **Yet super-polynomial lower bounds have been open since 1987**: Even at **depth 2** — the system **$\text{Res}(\oplus)$** (Itsykson–Sokolov 2020, resolution over $\mathbb{F}_2$-linear equations, where lines are disjunctions of parities $\bigvee_r (f_r(x) = b_r)$) — **no super-polynomial DAG refutation lower bound is known for any explicit tautology**, and $\text{PHP}_n^{n+1}$ / $\text{Count}_3(m)$ remain prime conjectured hard benchmarks!

---

## 2. Exact Polynomial Calculus ($\text{PC}$) vs Static Nullstellensatz ($\text{NS}$) over $\mathbb{F}_2$

### 2.1 Algebraic Definitions and Exact Linear-Algebraic Duality

Work in the multilinear Boolean quotient ring $R = \mathbb{F}_2[x_1, \dots, x_N] / \langle x_1^2 - x_1, \dots, x_N^2 - x_N \rangle$, with basis $\mathcal{M}_{\le d}$ of all multilinear monomials of degree $\le d$ ordered by non-decreasing degree (with $1 = \emptyset$ at index $0$). Given polynomial axioms $\mathcal{F} \subseteq R$:

- **Static Nullstellensatz ($\text{NS}$) at degree $d$**: Let $W_d = \text{span}_{\mathbb{F}_2}\{ m \cdot f \bmod (x_v^2 - x_v) : f \in \mathcal{F},\, m \in \mathcal{M},\, \deg(m) + \deg(f) \le d \}$. A degree-$d$ NS refutation exists iff $1 \in W_d$.
- **Dynamic Polynomial Calculus ($\text{PC}$) at degree $d$**: Let $V_d \subseteq R_{\le d}$ be the smallest $\mathbb{F}_2$-subspace containing $\{f \in \mathcal{F} : \deg(f) \le d\}$ and closed under variable multiplication of degree-$\le (d-1)$ elements:
  $$p \in V_d,\; \deg(p) \le d - 1,\; v \in [N] \;\implies\; x_v \cdot p \bmod (x_v^2 - x_v) \in V_d.$$
  A degree-$d$ PC refutation exists iff $1 \in V_d$. Note $W_d \subseteq V_d$, so $d_{\text{PC}}(\mathcal{F}) \le d_{\text{NS}}(\mathcal{F})$.

**Lemma 1 (Exact Highest-Bit Echelon Fixed-Point Computation)**.
*Order the bit positions of $\mathcal{M}_{\le d}$ by non-decreasing degree ($0$ for $1$, then degree $1, 2, \dots, d$), and maintain an $\mathbb{F}_2$-echelon basis $B$ of $V_d$ whose pivot for each row is its highest set bit. Then a polynomial $p \in \text{span}(B)$ satisfies $\deg(p) \le d - 1$ if and only if $p$ is a linear combination solely of basis rows whose pivot index lies in $\mathcal{M}_{\le d-1}$. Moreover, $1 \in \text{span}(B) \iff \text{pivot } 0 \in B$.*

*Proof*. In a highest-bit echelon basis, the highest set bit of any non-empty XOR of basis rows equals the maximum of their pivots; hence degree cancellations cannot drop below the largest contributing pivot. Since bit $0$ is minimal, $1$ lies in $\text{span}(B)$ iff some basis row has pivot $0$ (which must be $1$ itself). $\blacksquare$

**Theorem 2 (Exact $\mathbb{F}_2$ PC/NS Dual Witness / Pseudo-Expectation Duality)**.
*For any polynomial system $\mathcal{F}$ over $\mathbb{F}_2$ and degree $d \ge 1$, there is **no** degree-$d$ dynamic PC refutation of $\mathcal{F}$ if and only if there exists a linear functional (pseudo-expectation) $E : R_{\le d} \to \mathbb{F}_2$ satisfying:*
1. $E(1) = 1$,
2. $E(f) = 0$ *for every axiom* $f \in \mathcal{F}$ *with* $\deg(f) \le d$ *(and consequently $E(m \cdot f) = 0$ whenever $\deg(m) + \deg(f) \le d$)*,
3. *Dynamic invariance*: $E(x_v \cdot b) = 0$ *for every* $b \in V_d$ *with* $\deg(b) \le d - 1$ *and every variable* $x_v$.

*Proof*. $1 \notin V_d \iff \exists E \in (R_{\le d})^*$ with $E(1) = 1$ and $E|_{V_d} \equiv 0$. Given the echelon basis $B$ with $0 \notin B$, setting $E(1) = 1$, $E(m_j) = 0$ for all non-pivot $j > 0$, and back-substituting in increasing pivot order $E(m_p) = \bigoplus_{j < p,\, j \in \text{supp}(B_p)} E(m_j)$ constructs an explicit certificate $E$ verified independently against conditions (1)–(3). $\blacksquare$

**Lemma 3 (Exact Matching-Quotient Isomorphism for Conflict-Closed Systems)**.
*Let $\mathcal{F} = \mathcal{F}_{\text{lin}} \cup \{x_a x_b : (a,b) \in C\}$ where $\mathcal{F}_{\text{lin}}$ has degree $1$. For every degree $d \ge 2$, every conflicting monomial $M$ of degree $k \in [2, d]$ (containing some pair $(a,b) \in C$) is derivable in degree $k \le d$ directly from $x_a x_b = 0$ via $k - 2$ variable multiplications. Hence quotienting $R_{\le d}$ by all conflicting monomials — restricting the basis to valid partial matchings of size $\le d$ — preserves both $1 \in V_d$, $1 \in W_d$, and the exact dual-witness codimension $\dim(R_{\le d}/V_d)$.*

Our script `verification/verify_baton_012_ac0_mod2_frege.py` checks **both** the zero-shortcut full-monomial solver and the matching-quotient solver on $\text{FPHP}_2^3$, $\text{FPHP}_3^4$, and $\text{Count}_3(4, 5, 7)$, asserting 100% agreement on refutability and exact dual-witness codimension!

---

### 2.2 Exact Verified Degree Table on $\text{FPHP}_n^{n+1}$ (Comparison with Razborov 1998)

The **Functional Pigeonhole Principle** $\text{FPHP}_n^{n+1}$ over $\mathbb{F}_2$ has $N = n(n+1)$ variables $x_{i,j}$ ($i \in [n+1], j \in [n]$) and axioms:
- Pigeon axioms (deg 1): $\sum_{j=1}^n x_{i,j} + 1 = 0$ for $i \in [n+1]$,
- Functionality (deg 2): $x_{i,j} x_{i,j'} = 0$ for $j < j'$,
- Injectivity / Hole axioms (deg 2): $x_{i,j} x_{i',j} = 0$ for $i < i'$.

**Razborov (1998)** proved that over **any field $\mathbb{F}$** (including $\mathbb{F}_2$), $d_{\text{PC}}(\text{FPHP}_n^m) \ge \lceil n/2 \rceil + 1$ for all $m > n$. Our exact $\mathbb{F}_2$ solver computes:

| Instance | Vars $N$ | Basis Mode | Degree $d$ | Monomials | NS Rank (Status) | PC Rank (Status) | Exact $d_{\text{PC}}$ | Razborov $\lceil n/2 \rceil + 1$ | Exact $d_{\text{NS}}$ |
| :--- | ---: | :--- | ---: | ---: | :---: | :---: | :---: | :---: | :---: |
| $\text{FPHP}_2^3$ | 6 | Full (zero-shortcut) | 1 | 7 | 3 (DUAL) | 3 (DUAL) | — | — | — |
| $\text{FPHP}_2^3$ | 6 | Full (zero-shortcut) | 2 | 22 | 21 (REFUTED) | 22 (REFUTED) | **2** | **2** | **2** |
| $\text{FPHP}_3^4$ | 12 | Full (zero-shortcut) | 1 | 13 | 4 (DUAL) | 4 (DUAL) | — | — | — |
| $\text{FPHP}_3^4$ | 12 | Full (zero-shortcut) | 2 | 79 | 64 (DUAL, dim 15) | 64 (DUAL, dim 15) | — | — | — |
| $\text{FPHP}_3^4$ | 12 | Full (zero-shortcut) | 3 | 299 | 298 (REFUTED) | 299 (REFUTED) | **3** | **3** | **3** |
| $\text{FPHP}_4^5$ | 20 | Exact Matching-Quotient | 1 | 21 | 5 (DUAL) | 5 (DUAL) | — | — | — |
| $\text{FPHP}_4^5$ | 20 | Exact Matching-Quotient | 2 | 141 | 75 (DUAL, dim 66) | 75 (DUAL, dim 66) | — | — | — |
| $\text{FPHP}_4^5$ | 20 | Exact Matching-Quotient | 3 | 381 | **325 (DUAL, dim 56)** | **381 (REFUTED)** | **3** | **3** | — |
| $\text{FPHP}_4^5$ | 20 | Exact Matching-Quotient | 4 | 501 | 500 (REFUTED) | 501 (REFUTED) | **3** | **3** | **4** |

**Key Findings on $\text{FPHP}_n^{n+1}$**:
1. **Exact Tightness of Razborov (1998) at $n = 2, 3, 4$**: $d_{\text{PC}}^{\mathbb{F}_2}(\text{FPHP}_n^{n+1}) = \lceil n/2 \rceil + 1$ holds with **exact equality** ($2, 3, 3$).
2. **Strict Dynamic-PC vs Static-NS Separation at $n = 4$**: Static Nullstellensatz requires full degree $d_{\text{NS}}(\text{FPHP}_4^5) = 4$ (with a **56-dimensional** degree-3 NS dual witness space!), whereas dynamic Polynomial Calculus refutes $\text{FPHP}_4^5$ in degree **$3 < 4$** by canceling degree-3 terms to form new degree-2 consequences and dynamically multiplying them!
3. **Zero-Trust Dual Witness at $n = 3, d = 2$**: Our extracted explicit pseudo-expectation $E : \mathbb{F}_2[x]_{\le 2} \to \mathbb{F}_2$ for $\text{FPHP}_3^4$ has $E(1) = 1$, support counts `{deg 0: 1, deg 1: 4, deg 2: 18}`, and passes all axiom-ideal and dynamic-invariance checks $E(x_v \cdot b) = 0$.

---

### 2.3 Exact Verified Degree Table on $\text{Count}_3(m)$ over $\mathbb{F}_2$ vs $\mathbb{F}_3$

For $m \not\equiv 0 \pmod 3$, $\text{Count}_3(m)$ has $N = \binom{m}{3}$ variables $x_e$ ($e \in \binom{[m]}{3}$), vertex-partition axioms $\sum_{e \ni v} x_e + 1 = 0$ (deg 1), and disjointness axioms $x_e x_{e'} = 0$ for $e \neq e',\, e \cap e' \neq \emptyset$ (deg 2).

- **Over $\mathbb{F}_3$ (Degree 1 for ALL $m \not\equiv 0 \pmod 3$)**: Summing all $m$ vertex axioms yields $\sum_{v \in [m]} (\sum_{e \ni v} x_e - 1) = 3 \sum_e x_e - m \equiv -m \not\equiv 0 \pmod 3$, giving an immediate **degree-1** refutation (verified explicitly for $m \in \{4, 5, 7, 8, 10\}$).
- **Over $\mathbb{F}_2$ (Buss–Grigoriev–Impagliazzo–Pitassi 1999: $\Omega(m)$ degree)**:

| Instance | Vars $\binom{m}{3}$ | Basis Mode | Degree $d$ | Monomials | NS Rank (Status) | PC Rank (Status) | Dual Dim (PC) | $d_{\text{PC}}^{\mathbb{F}_2}$ vs $d_{\text{PC}}^{\mathbb{F}_3}$ |
| :--- | ---: | :--- | ---: | ---: | :---: | :---: | ---: | :---: |
| $\text{Count}_3(4)$ | 4 | Full | 1 / 2 | 5 / 11 | 4 (DUAL) / 11 (REF) | 4 (DUAL) / 11 (REF) | 1 / 0 | **2** vs 1 |
| $\text{Count}_3(5)$ | 10 | Full | 1 / 2 | 11 / 56 | 5 (DUAL) / 56 (REF) | 5 (DUAL) / 56 (REF) | 6 / 0 | **2** vs 1 |
| $\text{Count}_3(7)$ | 35 | Full | 1 | 36 | 7 (DUAL) | 7 (DUAL) | 29 | — |
| $\text{Count}_3(7)$ | 35 | Full | 2 | 631 | **630 (DUAL, dim 1!)** | **631 (REFUTED)** | 0 | **2** ($d_{\text{NS}}=3$) vs 1 |
| $\text{Count}_3(8)$ | 56 | Quotient | 1 / 2 | 57 / 337 | — | 8 (DUAL) / 337 (REF) | 49 / 0 | **2** vs 1 |
| $\text{Count}_3(10)$ | 120 | Quotient | 1 | 121 | — | 10 (DUAL) | 111 | — |
| $\text{Count}_3(10)$ | 120 | Quotient | 2 | 2221 | — | **805 (DUAL)** | **1416** | **$\ge 3$** vs 1 |

**Theorem 4 (Exact Kneser-Graph Dynamic-PC vs Static-NS Separation on $\text{Count}_3(7)$)**.
*Over $\mathbb{F}_2$, $\text{Count}_3(7)$ satisfies $d_{\text{PC}}^{\mathbb{F}_2}(\text{Count}_3(7)) = 2 < 3 = d_{\text{NS}}^{\mathbb{F}_2}(\text{Count}_3(7))$.*
*Proof*.
1. *Static NS Lower Bound ($d_{\text{NS}} \ge 3$)*: Define $E_{\text{sym}}(M) = 1$ on all $1 + 35 + 70 = 106$ valid matching monomials of degree $\le 2$ (and $0$ on all conflicting monomials). For any $v \in [7]$, $E_{\text{sym}}(\sum_{e \ni v} x_e + 1) = \binom{6}{2} + 1 = 15 + 1 = 16 \equiv 0 \pmod 2$. For any 3-subset $f$ and any $v \notin f$, $E_{\text{sym}}(x_f(\sum_{e \ni v} x_e + 1)) = \binom{7-3-1}{2} + 1 = \binom{3}{2} + 1 = 3 + 1 = 4 \equiv 0 \pmod 2$. Thus $E_{\text{sym}}$ is the **unique** (codimension $631 - 630 = 1$, verified!) degree-2 NS dual witness. (Since no 3-matching exists in 7 vertices, $d_{\text{NS}} = 3$.)
2. *Dynamic PC Upper Bound ($d_{\text{PC}} = 2$)*: Fix any 3-subset $f$ (leaving 4 uncovered vertices $U = [7] \setminus f$). Summing the 4 degree-2 equations $x_f(\sum_{e \ni v,\, e \subseteq U} x_e + 1) = 0$ over $v \in U$ gives $3 \sum_{e \subseteq U} x_f x_e + 4 x_f \equiv \sum_{e \subseteq U} x_f x_e = 0 \pmod 2$. Adding the single equation for $v \in U$ isolates $x_f x_{U \setminus \{v\}} + x_f = 0$ for every $e' = U \setminus \{v\}$ disjoint from $f$. By symmetry, $x_{e'} x_f + x_{e'} = 0$; adding these two degree-2 polynomials cancels $x_f x_{e'}$ and yields the **degree-1 identity $x_f + x_{e'} = 0$** across every edge of the connected Kneser graph $KG(7, 3)$! Chaining two Kneser edges gives $x_f + x_{e''} = 0$ for a *conflicting* pair $(f, e'')$; dynamically multiplying this degree-1 polynomial by $x_f$ gives $x_f^2 + x_f x_{e''} = x_f = 0$ (degree 2), hence $1 = 0$! Note why $E_{\text{sym}}$ fails dynamically: $E_{\text{sym}}(x_f + x_{e''}) = 1 + 1 = 0$, yet $E_{\text{sym}}(x_f(x_f + x_{e''})) = 1 + 0 = 1 \neq 0$! $\blacksquare$

Finally, at $m = 10$, the Kneser-degree-2 collapse fails completely: even **dynamic PC** has rank only $805 / 2221$ at $d = 2$ (a **1416-dimensional** zero-trust-verified degree-2 PC dual witness space!), certifying $d_{\text{PC}}^{\mathbb{F}_2}(\text{Count}_3(10)) \ge 3$ and marking the exact onset of BGIP's $\Omega(m)$ linear degree growth over $\mathbb{F}_2$.

---

## 3. Walking into the $\text{Res}(\oplus)$ / Depth-2 $\text{AC}^0[2]$-Frege Crack

In **$\text{Res}(\oplus)$** (Itsykson–Sokolov 2020), lines are disjunctions of $\mathbb{F}_2$-linear equations $C = \bigvee_{r=1}^w (f_r(x) = b_r)$, with resolution on arbitrary linear forms $f$ and $\mathbb{F}_2$-sound linear weakening/tautology rules.

### 3.1 Verified $O(|E|)$-Gaussian Collapse of $\text{Tseitin}(G)$ in $\text{Res}(\oplus)$

For any undirected graph $G = (V, E)$ with odd total charge $\bigoplus_{v \in V} c(v) = 1$, our script constructs complete **from-raw-CNF** $\text{Res}(\oplus)$ refutations (lifting each vertex's $2^{\deg(v)-1}$ CNF clauses to a unit XOR-clause $U_v = (\bigoplus_{e \ni v} x_e = c(v))$ and summing the $|V|$ unit XOR-clauses via $|V| - 1$ Gaussian additions to $(0 = 1) \vdash \bot$), verified line-by-line by an independent zero-trust $\mathbb{F}_2$-soundness checker:

| Tseitin Graph $G$ | $|V|$ | $|E|$ | CNF Clauses | $\text{Res}(\oplus)$ Total Steps | Gaussian Additions ($|V|-1$) | DPLL-Resolution Nodes |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| $\text{Tseitin}(K_4)$ | 4 | 6 | 16 | 54 (VERIFIED) | **3** | 15 |
| $\text{Tseitin}(K_5)$ | 5 | 10 | 40 | 128 (VERIFIED) | **4** | 127 |
| $\text{Tseitin}(K_6)$ | 6 | 15 | 96 | 298 (VERIFIED) | **5** | **2047** |
| $\text{Tseitin}(\text{Heawood})$ (3-reg expander) | 14 | 21 | 56 | 194 (VERIFIED) | **13** | **511** |

While ordinary DPLL-Resolution blows up exponentially ($15 \to 127 \to 2047$), $\text{Res}(\oplus)$ refutes every bounded-degree Tseitin graph in $O(|E|)$ steps via $|V| - 1$ Gaussian additions.

### 3.2 Why $\text{PHP}_n^{n+1}$ Resists Parity Gates: Three Verified Theorems & Probes

1. **$\mathbb{F}_2$-Linear Blindness of $\text{FPHP}$ vs Instant Collapse of $\text{onto-FPHP}$**:
   - Adding the surjectivity axioms $\bigoplus_{i=1}^{n+1} x_{i,j} = 1$ ($\text{onto-FPHP}_n^{n+1}$) makes the $\mathbb{F}_2$-linear system immediately inconsistent in $2n$ Gaussian steps: $\sum_i P_i + \sum_j H_j = (n+1) + n \equiv 1 \pmod 2$.
   - **Without** the onto axiom (standard $\text{PHP}_n^{n+1}$ / $\text{FPHP}_n^{n+1}$, where holes may hold $0$ or $1$ pigeons), the pigeon parities have rank $n + 1$ on $n(n+1)$ variables and **$2^{(n-1)(n+1)}$ $\mathbb{F}_2$-solutions** (verified for $n = 2..5$: $2^3, 2^8, 2^{15}, 2^{24}$). Hole capacity $\sum_i x_{i,j} \le 1$ is a threshold constraint invisible to $\mathbb{F}_2$-parity!

2. **Theorem 5 (Frobenius Linear-Extension Degree Invariance of $\text{PC}/\mathbb{F}_2$)**:
   *Augmenting any polynomial system $\mathcal{F}$ over $\mathbb{F}_2$ with arbitrarily many $\mathbb{F}_2$-linear extension variables $y_k = \bigoplus_{v \in S_k} x_v$ (parity gates of arbitrary width!) together with $y_k^2 - y_k = 0$ **cannot decrease $d_{\text{PC}}^{\mathbb{F}_2}(\mathcal{F})$**.*
   *Proof*. Define $\phi : \mathbb{F}_2[x, y] \to \mathbb{F}_2[x]/(x_v^2 - x_v)$ by $\phi(x_v) = x_v$ and $\phi(y_k) = \bigoplus_{v \in S_k} x_v$. Because $\phi$ maps every variable to a **degree-1** linear form, $\deg(\phi(P)) \le \deg(P)$. By the **characteristic-2 Frobenius identity**,
   $$\phi(y_k)^2 = \left(\sum_{v \in S_k} x_v\right)^2 = \sum_{v \in S_k} x_v^2 + 2 \sum_{u < v} x_u x_v \equiv \sum_{v \in S_k} x_v = \phi(y_k) \pmod{2,\, x_v^2 - x_v}.$$
   Thus $\phi$ kills every extension axiom and Boolean axiom identically, mapping any degree-$d$ PC refutation of $\mathcal{F}_{\text{ext}}$ to a degree-$\le d$ PC refutation of $\mathcal{F}$, and lifting every dual witness $E \mapsto E \circ \phi$! $\blacksquare$
   *(Verified computationally in Check 5b: augmenting $\text{FPHP}_2^3$ and $\text{FPHP}_3^4$ with 3 width-2/3 parity variables leaves $d_{\text{PC}} = 2, 3$ strictly unchanged with verified dual witnesses at $d = 1, 2$!)*

3. **Corollary 6 ($\text{Res}(\oplus)$ Width Lower Bound on $\text{FPHP}_n^{n+1}$)**:
   Every width-$w$ $\text{Res}(\oplus)$ clause $\bigvee_{r=1}^w (f_r(x) = b_r)$ encodes as the degree-$w$ polynomial $\prod_{r=1}^w (f_r(x) + b_r + 1) = 0$ over $\mathbb{F}_2$; simulating resolution and $\mathbb{F}_2$-weakening requires PC degree $\le 2w$. By Razborov (1998) and Theorem 5, **every $\text{Res}(\oplus)$ refutation of $\text{FPHP}_n^{n+1}$ requires clause width $w \ge \frac{1}{2}(\lceil n/2 \rceil + 1) = \Omega(n)$**.

4. **Empirical Parity-Gate Probe on $\text{PHP}_n^{n+1}$ (Check 5c)**:
   Augmenting $\text{PHP}_2^3, \text{PHP}_3^4, \text{PHP}_4^5$ with width-2 hole-pair parity gates $y_j \leftrightarrow x_{0,j} \oplus x_{1,j}$ produces **zero compression** in DPLL-Resolution (`plain = 3, 11, 63` nodes vs `std = 3, 11, 63`, and forcing parity-first branching *increases* search to `15, 55, 307` nodes!).

---

## 4. The Exact Open Wall: Why $\text{PC}/\mathbb{F}_2$ Dual Witnesses Do Not Lift to DAG $\text{Res}(\oplus)$ / $\text{AC}^0[2]$-Frege

We already have **linear degree/width lower bounds** ($d_{\text{PC}} = \lceil n/2 \rceil + 1$, $w_{\text{Res}(\oplus)} = \Omega(n)$) and **explicit zero-trust dual witnesses** for $\text{FPHP}$ and $\text{Count}_3$. What exact wall blocks lifting these into **super-polynomial size lower bounds** for DAG $\text{Res}(\oplus)$ and $\text{AC}^0[2]$-Frege?

### Wall A — Complete Collapse of Ben-Sasson–Wigderson Size–Width Averaging in $\text{Res}(\oplus)$
In ordinary Resolution (Baton #006), there are only $2V$ literals, so $S$ fat clauses of width $> k$ guarantee a literal appearing in $\ge \frac{k}{2V} S$ fat clauses; restricting it kills a $\frac{k}{2V}$ fraction of fat clauses. In $\text{Res}(\oplus)$:
1. **Exponential Linear-Literal Diversity**: There are $2(2^V - 1)$ linear literals $(f(x) = b)$. Even $S = \text{poly}(V)$ fat clauses of width $k$ can use **100% pairwise distinct linear literals** (maximum frequency $= 1$, vs BSW threshold $\frac{Sk}{2V}$ — verified concretely in Check 5d for $V=20, k=6, S=100$: max freq $= 1 < 15.0$).
2. **Variable-Restriction Immunity**: Setting a single Boolean variable $x_0 = b$ does **not** satisfy any parity literal of weight $\ge 2$ — it merely flips the RHS ($0/100$ fat clauses killed in Check 5d!).
3. **Random Affine-Restriction Miss**: Restricting a random hyperplane $g(x) = c$ satisfies a fixed linear literal $(f = b)$ with probability only $2^{-V}$. While **tree-like** $\text{Res}(\oplus)$ was conquered by Itsykson–Sokolov (2020) via affine Prover–Delayer games, **DAG $\text{Res}(\oplus)$** reuses wide clauses across exponentially many paths, breaking both Prover–Delayer games and BSW averaging.

### Wall B — The Razborov–Smolensky Error-Accumulation Wall for $\text{AC}^0[2]$-Frege
Why can't we apply Razborov–Smolensky (1987) directly to a size-$S$ $\text{AC}^0[2]$-Frege proof of $\text{PHP}_n^{n+1}$?
- Razborov–Smolensky approximates any depth-$d$, size-$S$ $\text{AC}^0[2]$ formula by a randomized $\mathbb{F}_2$-polynomial of degree $O((\log S)^d \log(1/\varepsilon))$ with pointwise error $\varepsilon$.
- To translate a **size-$S$ proof** line-by-line into a low-degree $\text{PC}/\mathbb{F}_2$ refutation (or to preserve soundness under a dual witness $E$), **every single inference step** across all $S$ proof lines must simultaneously preserve soundness! Union-bounding over $S$ lines forces $\varepsilon < 1/\text{poly}(S)$ (or worse, proving that the *error polynomial* itself stays inside the ideal!), which inflates the degree to $O((\log S)^{d+1})$ — and crucially, **unlike static circuit evaluation on random inputs**, a proof's intermediate cuts can steer into the exact $\varepsilon$-fraction error set where the polynomial approximator disagrees with the $\text{AC}^0[2]$ gate!
- Even for **depth-2 $\text{Res}(\oplus)$**, replacing a wide XOR-clause $\bigvee_{r=1}^w (f_r = b_r)$ by a randomized degree-$O(\log(1/\varepsilon))$ polynomial $\prod_{t=1}^{\ell} (\sum_r \alpha_{t,r} (f_r + b_r + 1))$ introduces false positives on an $\varepsilon$-fraction of assignments, destroying exact algebraic ideal membership required by $\text{PC}/\mathbb{F}_2$ dual witnesses $E$!

---

## 5. Mandatory 4-Barrier Audit Table

| Barrier | Reference | Interaction with $\text{AC}^0[2]$-Frege / $\text{Res}(\oplus)$ / $\text{PC}(\mathbb{F}_2)$ | Status in Baton #012 |
| :--- | :--- | :--- | :--- |
| **1. Relativization** | Baker–Gill–Solovay (1975) | Syntactic proof-system lower bounds for $\text{PC}/\mathbb{F}_2$, $\text{Res}(\oplus)$, and $\text{AC}^0[2]$-Frege inspect fixed gate/algebraic structure and do not relativize. | **Bypassed** (syntactic systems) |
| **2. Natural Proofs** | Razborov–Rudich (1997) | **NOT AN ACTIVE BLOCKER YET!** Cryptographic PRFs and RSA/factoring arithmetic are not believed to exist in $\text{AC}^0[2]$ (Razborov–Smolensky 1987); hence Feasible Interpolation for $\text{AC}^0[2]$-Frege is *not* ruled out by cryptography (unlike $\text{TC}^0$-Frege / Frege / $\text{EF}$ in Baton #006!). | **UNBLOCKED** (surviving crack!) |
| **3. Algebrization** | Aaronson–Wigderson (2009) | $\text{PC}/\mathbb{F}_2$ degree bounds and dual witnesses operate directly in the low-degree polynomial ring $\mathbb{F}_2[x]$; pure low-degree algebraic arguments stay inside the algebraic world (cannot alone jump to $\text{EF}$/$\text{P}\neq\text{NP}$ without non-algebrizing structure). | **Active Caution** (for lifts beyond $\text{AC}^0[2]$-Frege) |
| **4. Locality Barrier** | CHOPRS (STOC 2020) | **ACTIVE MECHANISM WALL**: Local Håstad random restrictions & BSW literal-frequency averaging conquer $\text{AC}^0$-Frege / Resolution, but **fail completely on parity gates** (verified in Check 5d: $x_0 = b$ kills $0/100$ parity clauses; linear literals number $2^V$). Overcoming $\text{Res}(\oplus)$ requires **global affine/subspace restrictions** (subspace-switching lemmas or non-local algebraic lifting). | **ACTIVE BLOCKER** for local restriction / BSW lifts |

---

## 6. Verdict & Actionable Handoff to Next Batons

- **Did Baton #012 resolve $\text{P}$ vs $\text{NP}$ or prove super-polynomial DAG $\text{Res}(\oplus)$ / $\text{AC}^0[2]$-Frege lower bounds?** **NO.**
- **What did Baton #012 rigorously establish and verify (`verification/verify_baton_012_ac0_mod2_frege.py`, 0.36s, exit 0)?**
  1. Computed exact $\mathbb{F}_2$ $\text{PC}$ and $\text{NS}$ degrees for $\text{FPHP}_n^{n+1}$ ($n=2,3,4$: $d_{\text{PC}} = 2, 3, 3 = \lceil n/2 \rceil + 1$ tight; strict separation $d_{\text{PC}} = 3 < 4 = d_{\text{NS}}$ at $n=4$) and $\text{Count}_3(m)$ ($m=4,5,7,8,10$: $d_{\text{PC}}^{\mathbb{F}_3} = 1$, strict Kneser-graph separation $d_{\text{PC}}^{\mathbb{F}_2} = 2 < 3 = d_{\text{NS}}^{\mathbb{F}_2}$ on $\text{Count}_3(7)$, linear onset $d_{\text{PC}}^{\mathbb{F}_2} \ge 3$ with 1416-dim dual space on $\text{Count}_3(10)$).
  2. Extracted and independently zero-trust-verified explicit $\mathbb{F}_2$ dual witnesses (pseudo-expectations $E$) certifying all degree lower bounds via linear-algebraic duality.
  3. Built and zero-trust-verified from-CNF $\text{Res}(\oplus)$ refutations of $\text{Tseitin}(K_4, K_5, K_6, \text{Heawood})$ in $|V| - 1 = O(|E|)$ Gaussian additions vs exponential DPLL blowup ($15 \to 127 \to 2047$).
  4. Proved and verified the **Frobenius Linear-Extension Degree Invariance Theorem**, $\text{FPHP}$'s $2^{(n-1)(n+1)}$ $\mathbb{F}_2$-linear blindness (vs $\text{onto-FPHP}$'s $2n$-step collapse), zero compression under width-2 parity extensions in DPLL, and the exact BSW literal-frequency breakdown for $\text{Res}(\oplus)$.

### Exact Next-Baton Attack Directions Inside the $\text{Res}(\oplus)$ / $\text{AC}^0[2]$-Frege Crack
1. **Affine/Subspace-Restriction Switching Lemma for DAG $\text{Res}(\oplus)$**: Instead of single-variable restrictions (provably dead on parity literals), test whether **codimension-$t$ affine subspace restrictions** $A x = b$ combined with **lifting theorems** (e.g., $\text{PHP} \circ \text{XOR}$ or lifted Tseitin/Count gadgets, cf. Garg–Göös–Kamath–Sokolov / Part–Tzameret) can shrink DAG $\text{Res}(\oplus)$ width without hitting the $2^V$ literal diversity wall.
2. **Error-Tolerant / Approximate Dual Witnesses (Bridging Razborov–Smolensky to $\text{PC}/\mathbb{F}_2$)**: Formalize whether a **distribution over $\mathbb{F}_2$ dual witnesses** $\{E_\omega\}$ (matching the randomized Razborov–Smolensky polynomial approximator) can witness soundness on *structured* fragments of $\text{Res}(\oplus)$ (e.g., bounded-bottom-fan-in $\text{Res}(\oplus)$, regular $\text{Res}(\oplus)$, or constant-$\text{rank}$ XOR-clauses) before tackling unrestricted DAG $\text{Res}(\oplus)$.
3. **Feasible Interpolation for $\text{AC}^0[2]$-Frege / $\text{Res}(\oplus)$**: Since $\text{AC}^0[2]$ cannot host PRFs, test whether **$\text{Res}(\oplus)$ admits $\text{AC}^0[2]$ or $\text{NC}^2/\mathbb{F}_2$-span-program feasible interpolation** on Clique–Coloring or $\text{Count}_3$-split tautologies (which would immediately yield exponential $\text{Res}(\oplus)$ lower bounds via known span-program / $\text{AC}^0[2]$ lower bounds!).
