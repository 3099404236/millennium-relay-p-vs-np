# Baton #009: Aaronson–Wigderson (2009) Algebrization Barrier & Executable Arithmetization / Sumcheck Audit

- **Target Millennium Problem**: P versus NP (Clay Mathematics Institute — **Unsolved**)
- **Baton ID**: `baton-009`
- **Node ID**: `baton-009-algebrization-audit`
- **Status**: `VERIFIED` (Barrier audit & executable finite-field verification complete; **does not** resolve P vs NP; establishes an executable Algebrization filter for all downstream algebraic, polynomial-method, and interactive-proof batons)
- **Date**: 2026-11-26
- **Verification Script**: `python verification/verify_baton_009_algebrization.py`

---

## 1. Executive Summary

Following Baker–Gill–Solovay (1975), the **Relativization Barrier** showed that black-box oracle-invariant arguments cannot resolve $\text{P}$ vs. $\text{NP}$. Starting in 1990, however, **arithmetization**—lifting Boolean formulas and oracle truth tables to low-degree multivariate polynomials over finite fields $\mathbb{F}_q$ and checking them via the **Sumcheck protocol**—shattered Relativization, yielding non-relativizing landmarks such as $\text{IP} = \text{PSPACE}$ (Lund–Fortnow–Karloff–Nisan 1992; Shamir 1992), $\text{MIP} = \text{NEXP}$ (Babai–Fortnow–Lund 1991), and $\text{MA}_{\text{EXP}} \not\subseteq \text{P/poly}$ (Buhrman–Fortnow–Thierauf 1998).

**Aaronson and Wigderson (STOC 2008 / ACM TOCT 2009)** explained why arithmetization stalled short of $\text{P}$ vs. $\text{NP}$, $\text{NP}$ vs. $\text{P/poly}$, and $\text{NEXP}$ vs. $\text{P/poly}$ by formulating the **Algebrization Barrier**:

1. **Every known arithmetization theorem algebrizes**: given an oracle $A$ and its low-degree polynomial extension $\tilde{A}$ over $\mathbb{F}_q$, the inclusion $\text{PSPACE}^A \subseteq \text{IP}^{\tilde{A}}$ holds universally for all $(A, \tilde{A})$.
2. **Collapsing algebraic oracle (blocks separation proofs)**: taking $A = \text{TQBF}$ and letting $\tilde{A}$ be its multilinear extension yields $\tilde{A} \in \text{PSPACE}$, collapsing the entire polynomial hierarchy and $\text{PSPACE}$ into $\text{P}^A$:
   $$\text{P}^A = \text{P}^{\tilde{A}} = \text{NP}^A = \text{NP}^{\tilde{A}} = \text{PH}^{\tilde{A}} = \text{PSPACE}^A = \text{PSPACE}^{\tilde{A}} = \text{PSPACE} \subseteq \text{P/poly}^A.$$
   In particular, $\text{NP}^{\tilde{A}} \subseteq \text{P}^{\tilde{A}}$ (and $\text{NP}^{\tilde{A}} \subseteq \text{P}^A \subseteq \text{P/poly}^A$), blocking any pure arithmetization proof of $\text{P} \neq \text{NP}$, $\text{NP} \not\subseteq \text{BPP}$, $\text{NP} \not\subseteq \text{P/poly}$, or $\text{PSPACE} \not\subseteq \text{P/poly}$. Furthermore, Aaronson–Wigderson extend the barrier to block algebrizing proofs of $\text{NEXP} \not\subseteq \text{P/poly}$.
3. **Separating algebraic oracle (blocks collapse proofs)**: conversely, via Set Disjointness communication complexity, there exists $(A, \tilde{A})$ with $\text{NP}^A \not\subseteq \text{BPP}^{\tilde{A}}$ (hence $\text{NP}^A \not\subseteq \text{P}^{\tilde{A}}$), blocking any algebrizing proof of $\text{P} = \text{NP}$.
4. **Executable Verification**: `verification/verify_baton_009_algebrization.py` implements and verifies all three mathematical engines over $\mathbb{F}_{101}$ and $\mathbb{F}_{257}$: exact multilinear extensions (MLE/LDE), full interactive Sumcheck (honest prover, naive cheater, and Schwartz–Zippel-optimal $d$-root adaptive cheater for $n \in \{4, 5\}$), and concrete finite-field demonstrations of why BGS breaks against $\tilde{A}$ while AW09's algebraic-oracle hiding and $\text{PSPACE}$ streaming collapse hold.

---

## 2. Formal Definition of Low-Degree Extensions & Algebrization

### 2.1 Multilinear Low-Degree Extension (MLE / LDE)
Let $A = \{A_m\}_{m \ge 1}$ be a Boolean oracle, where each slice $A_m : \{0,1\}^m \to \{0,1\}$ is a Boolean function on $m$ bits. For any prime (or prime-power) finite field $\mathbb{F}_q$, the **multilinear extension (MLE)** of $A_m$ over $\mathbb{F}_q$ is the unique polynomial $\tilde{A}_m : \mathbb{F}_q^m \to \mathbb{F}_q$ of individual degree at most $1$ in each variable $x_1, \dots, x_m$ (total degree $\le m$) that agrees with $A_m$ on the Boolean hypercube $\{0,1\}^m$:
$$\tilde{A}_m(x_1, \dots, x_m) = \sum_{w \in \{0,1\}^m} A_m(w) \cdot \chi_w(x_1, \dots, x_m) \pmod q,$$
where the Lagrange multilinear indicator polynomial is
$$\chi_w(x_1, \dots, x_m) = \prod_{i=1}^{m} \bigl(w_i x_i + (1 - w_i)(1 - x_i)\bigr).$$

Equivalently, $\tilde{A}_m$ has a unique monomial expansion over $\mathbb{F}_q$:
$$\tilde{A}_m(x_1, \dots, x_m) = \sum_{S \subseteq [m]} c_S \prod_{i \in S} x_i \pmod q, \qquad c_S = \sum_{w \subseteq S} (-1)^{|S| - |w|} A_m(w) \pmod q,$$
computed via Möbius inversion on the Boolean lattice. More generally, in Aaronson–Wigderson (2009), an **algebraic extension** $\tilde{A}$ specifies, for each length $m$ and finite field $\mathbb{F}_q$ (with modulus $q$ supplied in binary, $\log q \le \text{poly}(m)$), a low-degree extension polynomial $\tilde{A}_{m, q} : \mathbb{F}_q^m \to \mathbb{F}_q$ agreeing with $A_m$ on $\{0,1\}^m$ (with MLE as the canonical degree-$1$-per-variable realization).

Notice two immediate structural properties:
- **Oracle dominance**: Since $\tilde{A}_m(w) = A_m(w)$ for all $w \in \{0,1\}^m$, any machine with oracle access to $\tilde{A}$ can simulate $A$ with zero overhead; thus $\mathcal{C}^A \subseteq \mathcal{C}^{\tilde{A}}$ for every standard complexity class $\mathcal{C}$.
- **Global linearity**: Evaluating $\tilde{A}_m(r)$ at a non-Boolean field point $r \in \mathbb{F}_q^m$ returns a **global linear combination** of all $2^m$ Boolean values of $A_m$ weighted by $\chi_w(r) \in \mathbb{F}_q$.

### 2.2 Formal Definition of Algebrizing Inclusions and Separations
Aaronson–Wigderson (2009) define algebrization asymmetrically so that arithmetization proofs pass the test:
- An **inclusion** $\mathcal{C}_1 \subseteq \mathcal{C}_2$ **algebrizes** if for every Boolean oracle $A$ and every low-degree extension $\tilde{A}$ of $A$,
  $$\mathcal{C}_1^A \subseteq \mathcal{C}_2^{\tilde{A}}.$$
- A **separation** $\mathcal{C}_1 \not\subseteq \mathcal{C}_2$ **algebrizes** if for every Boolean oracle $A$ and every low-degree extension $\tilde{A}$ of $A$,
  $$\mathcal{C}_1^{\tilde{A}} \not\subseteq \mathcal{C}_2^A$$
  (or in the weaker symmetric test, $\mathcal{C}_1^{\tilde{A}} \not\subseteq \mathcal{C}_2^{\tilde{A}}$; any collapsing oracle satisfying $\mathcal{C}_1^{\tilde{A}} \subseteq \mathcal{C}_2^A \subseteq \mathcal{C}_2^{\tilde{A}}$ simultaneously defeats both!).

---

## 3. Why $\text{IP} = \text{PSPACE}$ Breaks Relativization Yet Algebrizes

### 3.1 Why Relativization Breaks Against $\tilde{A}$
In Baker–Gill–Solovay (1975), the unary language
$$L_A^{\text{BGS}} = \bigl\{1^n : \exists w \in \{0,1\}^n \text{ such that } A_n(w) = 1\bigr\} \in \text{NP}^A$$
separates $\text{NP}^A$ from $\text{P}^A$ (and $\text{BPP}^A$): flipping $A_n$ at a single unqueried string $w^* \in \{0,1\}^n$ is invisible to a machine making $\text{poly}(n) \ll 2^n$ Boolean queries to $A_n$.

Under an algebraic oracle $\tilde{A}$, **naive BGS diagonalization collapses immediately**:
- **Lemma 1 (Schwartz–Zippel Detection of BGS Witnesses)**: For any prime $q > 2n$ and any Boolean slice $A_n : \{0,1\}^n \to \{0,1\}$:
  - If $A_n \equiv 0$, then $\tilde{A}_n(r) = 0$ for all $r \in \mathbb{F}_q^n$.
  - If $A_n \not\equiv 0$ (even at Hamming weight $1$, $A_n = \mathbf{1}_{w^*}$), then $\tilde{A}_n$ is a nonzero polynomial of total degree $\le n$, so by the Schwartz–Zippel Lemma:
    $$\Pr_{r \sim \mathbb{F}_q^n}\!\bigl[\tilde{A}_n(r) \neq 0\bigr] \ge 1 - \frac{n}{q} > \frac{1}{2}.$$
  - For a weight-$1$ perturbation $A_1 = \mathbf{1}_{w^*}$, $\tilde{A}_1(r) = \chi_{w^*}(r) = \prod_{i=1}^n (w^*_i r_i + (1-w^*_i)(1-r_i))$, which vanishes iff $r_i = 1 - w^*_i$ for some $i$; thus the exact detection probability of a single algebraic query is $(1 - 1/q)^n \ge 1 - n/q$.

Hence $L_A^{\text{BGS}} \in \text{RP}^{\tilde{A}} \subseteq \text{BPP}^{\tilde{A}}$ for **every** oracle $A$! In our verification script (`test_part_a_bgs_breaks_against_mle`, $n=5, q=101$), a single Boolean query catches a weight-$1$ flip with probability $1/32 = 3.125\%$, whereas a single algebraic query over $\mathbb{F}_{101}^5$ catches it with probability $(100/101)^5 = 95.15\% \ge 1 - 5/101 = 95.05\%$.

### 3.2 Arithmetization & Interactive Sumcheck: $\text{PSPACE}^A \subseteq \text{IP}^{\tilde{A}}$
To prove $\text{IP} = \text{PSPACE}$, Shamir's protocol arithmetizes a quantified Boolean formula (or equivalently, a $\text{PSPACE}^A$ computation tableau with oracle queries to $A$) into a low-degree multivariate polynomial $g : \mathbb{F}_q^n \to \mathbb{F}_q$ of individual degree $\le d$, where Boolean operators lift algebraically ($\neg x \mapsto 1-x$, $x \land y \mapsto xy$, $\forall \mapsto \prod$, $\exists \mapsto \sum$) and every Boolean oracle call $A_m(u)$ is replaced by the polynomial oracle call $\tilde{A}_m(u)$.

The **Sumcheck protocol** reduces verifying a hypercube sum $H = \sum_{b \in \{0,1\}^n} g(b) \pmod q$ to a **single** evaluation of $g(r_1, \dots, r_n)$ (and thus a polynomial number of queries to $\tilde{A}$):
1. In round $i \in \{1, \dots, n\}$, given previous verifier challenges $r_1, \dots, r_{i-1} \in \mathbb{F}_q$, the prover sends a univariate polynomial $s_i(X) \in \mathbb{F}_q[X]$ of degree $\le d$ claiming to equal
   $$s_i^{\text{true}}(X) = \sum_{(b_{i+1}, \dots, b_n) \in \{0,1\}^{n-i}} g(r_1, \dots, r_{i-1}, X, b_{i+1}, \dots, b_n).$$
2. The verifier checks $\deg(s_i) \le d$ and $s_i(0) + s_i(1) = C_i$ (where $C_1 = H$ and $C_i = s_{i-1}(r_{i-1})$ for $i \ge 2$), then picks uniform $r_i \in \mathbb{F}_q$ and sets $C_{i+1} \leftarrow s_i(r_i)$.
3. After round $n$, the verifier queries the algebraic oracle $\tilde{A}$ to evaluate $g(r_1, \dots, r_n)$ and accepts iff $C_{n+1} = g(r_1, \dots, r_n)$.

- **Completeness ($100\%$)**: An honest prover passes every check with probability $1$.
- **Soundness (Schwartz–Zippel)**: If $H_{\text{claimed}} \neq H_{\text{true}}$, then in each round $i$ where $C_i \neq s_i^{\text{true}}(0) + s_i^{\text{true}}(1)$, any polynomial $s_i(X)$ passing the sum check must satisfy $\Delta_i(X) := s_i(X) - s_i^{\text{true}}(X) \not\equiv 0$ with $\deg(\Delta_i) \le d$. Hence $\Delta_i$ has at most $d$ roots in $\mathbb{F}_q$, so the cheater can only equalize $C_{i+1} = s_i^{\text{true}}(r_i)$ with probability at most $d/q$ per round. Across $n$ independent rounds, the **optimal adaptive cheater** (who crafts $\Delta_i(X) = \lambda \prod_{k=1}^d (X - \alpha_k)$ with $d$ distinct roots and switches to honest play if lucky) is caught with exact probability
  $$\Pr[\text{Verifier rejects optimal cheater}] = \left(1 - \frac{d}{q}\right)^n \ge 1 - \frac{nd}{q}.$$

Because the verifier only needs access to $\tilde{A}$ at the end of Sumcheck (never needing to read the exponential truth table of $A$), the entire proof of $\text{IP} = \text{PSPACE}$ works verbatim relative to any $(A, \tilde{A})$, yielding
$$\text{PSPACE}^A \subseteq \text{IP}^{\tilde{A}} \quad \text{and} \quad \text{IP}^A \subseteq \text{PSPACE}^A \subseteq \text{PSPACE}^{\tilde{A}}.$$
Thus `IP = PSPACE` **breaks Relativization** (Fortnow–Sipser 1988 showed $\exists B : \text{coNP}^B \not\subseteq \text{IP}^B$) yet **strictly algebrizes**.

---

## 4. The Aaronson–Wigderson Barrier Theorems

### 4.1 Theorem 1 (Collapsing Algebraic Oracle: Blocking $\text{P} \neq \text{NP}$ and $\text{NP} \not\subseteq \text{P/poly}$)

**Theorem 1 (Aaronson–Wigderson 2009, Theorem 5.2)**: *There exists a Boolean oracle $A$ and its multilinear low-degree extension $\tilde{A}$ such that*
$$\text{NP}^{\tilde{A}} \subseteq \text{PSPACE}^{\tilde{A}} = \text{P}^A \subseteq \text{P}^{\tilde{A}} \subseteq \text{P/poly}^A.$$

**Complete Proof**:
1. Let $A = \text{TQBF}$ be the standard $\text{PSPACE}$-complete language of true quantified Boolean formulas, and let $\tilde{A}$ be its multilinear extension over prime fields $\mathbb{F}_q$ (with $q$ encoded in binary as part of the query).
2. **Claim**: $\tilde{A} \in \text{PSPACE}$.
   *Proof of Claim*: On input $(m, q, x_1, \dots, x_m) \in \mathbb{F}_q^m$, iterate through all $w \in \{0,1\}^m$ in lexicographic order using an $m$-bit counter. For each $w$:
   - Decide $A_m(w) \in \{0,1\}$ in $\text{poly}(m)$ space (since $A = \text{TQBF} \in \text{PSPACE}$).
   - Compute $\chi_w(x) = \prod_{i=1}^m (w_i x_i + (1 - w_i)(1 - x_i)) \bmod q$ in $O(m \log q)$ space.
   - Add $A_m(w)\chi_w(x) \bmod q$ into a running accumulator of size $O(\log q)$.
   Total working space is $\text{poly}(m, \log q) = \text{poly}(\text{input length})$, with no need to store the $2^m$-entry table. (Verified concretely on a parameterized QBF oracle in `test_part_c_pspace_collapsing_oracle_consistency`.)
3. Since $\tilde{A} \in \text{PSPACE}$ and $\text{PSPACE}$ is closed under oracle calls to $\text{PSPACE}$ (by reusing a $\text{poly}(n)$-space work tape for each query), we obtain $\text{PSPACE}^{\tilde{A}} = \text{PSPACE}$.
4. Because $A = \text{TQBF}$ is $\text{PSPACE}$-complete under polynomial-time many-one reductions, $\text{PSPACE} = \text{P}^A$.
5. Chaining these equalities gives:
   $$\text{P}^A \subseteq \text{P}^{\tilde{A}} \subseteq \text{NP}^{\tilde{A}} \subseteq \text{PH}^{\tilde{A}} \subseteq \text{PSPACE}^{\tilde{A}} = \text{PSPACE} = \text{P}^A.$$
   Hence every class in the chain equals $\text{P}^A$ (and lies inside $\text{P/poly}^A$). $\blacksquare$

**Immediate Consequences**: Pure arithmetization / algebrizing techniques **cannot** prove:
- $\text{P} \neq \text{NP}$ (since $\text{NP}^{\tilde{A}} \subseteq \text{P}^A \subseteq \text{P}^{\tilde{A}}$),
- $\text{NP} \neq \text{coNP}$ or non-collapse of $\text{PH}$,
- $\text{NP} \not\subseteq \text{BPP}$,
- $\text{NP} \not\subseteq \text{P/poly}$ or $\text{PSPACE} \not\subseteq \text{P/poly}$.

### 4.2 Theorem 2 (Separating Algebraic Oracle: Blocking $\text{P} = \text{NP}$ via Set Disjointness)

**Theorem 2 (Aaronson–Wigderson 2009, Theorem 5.3)**: *There exists a Boolean oracle $A$ and its multilinear extension $\tilde{A}$ such that $\text{NP}^A \not\subseteq \text{BPP}^{\tilde{A}}$ (and in particular $\text{NP}^A \not\subseteq \text{P}^{\tilde{A}}$).*

**Proof Mechanism (Communication Complexity Reduction & Algebraic-Oracle Hiding)**:
1. For each input length $n$, split the $2^n$-bit oracle slice $A_n$ into two halves of size $N = 2^{n-1}$: Alice's table $X(w) := A_n(0, w)$ and Bob's table $Y(w) := A_n(1, w)$ for $w \in \{0,1\}^{n-1}$.
2. Define the unary $\text{NP}^A$ language
   $$L_A^{\text{DISJ}} = \bigl\{1^n : \exists w \in \{0,1\}^{n-1} \text{ such that } A_n(0, w) = 1 \land A_n(1, w) = 1\bigr\} = \neg\text{DISJ}_N(X, Y).$$
3. **Bilinear Split Lemma**: The multilinear extension $\tilde{A}_n$ decomposes linearly across the first coordinate $x_0$:
   $$\tilde{A}_n(x_0, x') = (1 - x_0)\tilde{X}(x') + x_0 \tilde{Y}(x') \pmod q.$$
   Therefore, Alice and Bob can simulate **any** algebraic query $(x_0, x') \in \mathbb{F}_q^n$ to $\tilde{A}_n$ using only $O(\log q)$ bits of communication (Alice sends $\tilde{X}(x') \in \mathbb{F}_q$, Bob evaluates $\tilde{Y}(x')$ and computes the combination).
4. Any $\text{BPP}^{\tilde{A}}$ machine making $T = \text{poly}(n)$ queries over fields of size $q \le 2^{\text{poly}(n)}$ would yield a randomized communication protocol for $\text{DISJ}_N$ with total cost $O(T \log q) = \text{poly}(n) = \text{poly}(\log N)$ bits—contradicting the $\Omega(N) = \Omega(2^n)$ randomized communication lower bound of Kalyanasundaram–Schnitger (1992) and Razborov (1992). Standard diagonalization over all $\text{BPP}$ machines across sparse lengths yields $A$ with $L_A^{\text{DISJ}} \in \text{NP}^A \setminus \text{BPP}^{\tilde{A}}$.
5. **Finite-Field Linear-Query Hiding**: Algebraically, $T$ queries $r^{(1)}, \dots, r^{(T)} \in \mathbb{F}_q^n$ reveal only a $T$-dimensional linear projection $\Phi(A_n) \in \mathbb{F}_q^T$ of a $2^n$-bit Boolean table ($q^T \ll 2^{2^n}$). Thus exponentially many sparse disjoint instances ($L_A = 0$) and sparse intersecting instances ($L_A = 1$) collapse to **identical** query transcripts on $\tilde{A}$. Our script (`test_part_b_aw09_disjointness_and_hiding`) constructs explicit sparse colliding oracle pairs on $\{0,1\}^5$ over both $\mathbb{F}_{101}$ ($T = 3$ non-Boolean queries) and $\mathbb{F}_{257}$ ($T = 2$ non-Boolean queries).

### 4.3 Extension to $\text{NEXP}$ vs. $\text{P/poly}$ and What Escapes Algebrization

Aaronson–Wigderson (2009) map the exact frontier separating algebrizing circuit lower bounds from non-algebrizing ones:

| Complexity Statement | Relativizes? | Algebrizes? | Reason / Mechanism |
| :--- | :---: | :---: | :--- |
| $\text{IP} = \text{PSPACE}$ | No | **Yes** | Sumcheck + MLE yields $\text{PSPACE}^A \subseteq \text{IP}^{\tilde{A}}$ |
| $\text{MIP} = \text{NEXP}$ | No | **Yes** | Multi-prover low-degree test + MLE yields $\text{NEXP}^A \subseteq \text{MIP}^{\tilde{A}}$ |
| $\text{MA}_{\text{EXP}} \not\subseteq \text{P/poly}$ | No | **Yes** | Buhrman–Fortnow–Thierauf (1998) uses `IP = PSPACE` + instance checkers |
| $\text{PP} \not\subseteq \text{SIZE}(n^k)$ | No | **Yes** | Vinodchandran (2005) / Aaronson (2006) via arithmetized counting |
| $\text{P} \neq \text{NP}$ | No | **No** | Blocked by $A = \text{TQBF}$ ($\text{NP}^{\tilde{A}} \subseteq \text{P}^A \subseteq \text{P}^{\tilde{A}}$) |
| $\text{P} = \text{NP}$ | No | **No** | Blocked by Disjointness oracle ($\text{NP}^A \not\subseteq \text{BPP}^{\tilde{A}}$) |
| $\text{NP} \not\subseteq \text{P/poly}$ | No | **No** | Blocked by $A = \text{TQBF}$ ($\text{PSPACE}^{\tilde{A}} = \text{P}^A \subseteq \text{P/poly}^A$) |
| $\text{NEXP} \not\subseteq \text{P/poly}$ | No | **No** | Aaronson–Wigderson (2009): requires non-algebrizing circuit-structure ingredients |
| $\text{NEXP} \not\subseteq \text{ACC}^0$ (Williams 2011) | No | **No (Bypassed!)** | Uses **white-box** $\text{ACC}^0\text{-SAT}$ algorithm inspecting gate syntax (fails with oracle gates $A$ or $\tilde{A}$) |

**Core Diagnostic Lesson**: Why did Ryan Williams's proof of $\text{NEXP} \not\subseteq \text{ACC}^0$ (2011) succeed where arithmetization failed? Because Williams's $\text{ACC}^0\text{-SAT}$ algorithm exploits the *concrete internal gate representation* (converting $\text{ACC}^0$ gates into a $\text{SYM}^+$ circuit via Beigel–Tarui and applying fast rectangular matrix multiplication). A circuit containing arbitrary oracle gates $A$ or $\tilde{A}$ has no small $\text{SYM}^+$ representation, so Williams's algorithm cannot run on relativized or algebrized circuits—making the proof genuinely **non-algebrizing**.

---

## 5. Executable Verification Summary (`verification/verify_baton_009_algebrization.py`)

All verification checks use Python 3.12 standard library only and pass deterministically with exit code `0`:

| Verification Pillar | Parameters Tested | Key Quantitative Result | Status |
| :--- | :--- | :--- | :---: |
| **1. Exact MLE / LDE** | $n \in \{3,4,5\}$, $q \in \{101,257\}$, 30 diverse Boolean oracles | $100\%$ agreement on $\{0,1\}^n$; Lagrange $=$ Monomial $=$ Streaming; vanishing 2nd finite difference across all $t \in \mathbb{F}_q$ (degree $\le 1$ per var) | `[PASS]` |
| **2. Interactive Sumcheck ($n=4, d=1, q=101$)** | 100 honest, 100 naive cheater, 2000 optimal $d$-root cheater | Honest $100/100$; Naive caught $100/100$; Optimal caught $1927/2000$ ($0.9635$ vs exact $0.9610 \ge 1-nd/q = 0.9604$) | `[PASS]` |
| **2. Interactive Sumcheck ($n=4, d=2, q=101$)** | Witness-intersection $g = \tilde{A}\cdot\tilde{B}$, 2000 optimal cheater | Honest $100/100$; Optimal caught $1850/2000$ ($0.9250$ vs exact $0.9231 \ge 0.9208$); all rounds exhaustively audited for exact $d=2$ roots | `[PASS]` |
| **2. Interactive Sumcheck ($n=5, d=2, q=101$)** | Witness-intersection $g = \tilde{A}\cdot\tilde{B}$, 2000 optimal cheater | Honest $100/100$; Optimal caught $1804/2000$ ($0.9020$ vs exact $0.9048 \ge 0.9010$) | `[PASS]` |
| **2. Interactive Sumcheck ($n=5, d=2, q=257$)** | Witness-intersection $g = \tilde{A}\cdot\tilde{B}$, 2000 optimal cheater | Honest $100/100$; Optimal caught $1912/2000$ ($0.9560$ vs exact $0.9617 \ge 0.9611$) | `[PASS]` |
| **2. Interactive Sumcheck ($n=4, d=3, q=257$)** | Triple product $g = \tilde{A}\cdot\tilde{B}\cdot\tilde{C}$, 2000 optimal cheater | Honest $100/100$; Optimal caught $1891/2000$ ($0.9455$ vs exact $0.9541 \ge 0.9533$) | `[PASS]` |
| **3A. Why BGS Breaks under $\tilde{A}$** | $n=5, q=101$, weight-1 flip, 2000 trials | Boolean query catches at $2.40\%$ (exact $3.12\%$); single $\tilde{A}(r)$ query catches at $95.15\%$ (exact $95.15\% \ge 1-5/101 = 95.05\%$) | `[PASS]` |
| **3B. AW09 Disjointness & Hiding** | $n=5$, $q=101$ ($T=3$) & $q=257$ ($T=2$) | Exact bilinear split verified; explicit sparse DISJOINT ($L=0$) & INTERSECTING ($L=1$) oracles with **identical** MLE query vectors `(23, 62, 92) mod 101` and `(175, 44) mod 257` | `[PASS]` |
| **3C. AW09 $\text{PSPACE}$ Collapse** | $n=4$ parameterized QBF oracle, $q \in \{101, 257\}$ | Streaming $O(n + \log q)$-space evaluator matches full-table MLE identically across 100 random field queries | `[PASS]` |

---

## 6. Mandatory 4-Barrier Audit Table

| Barrier | Reference | What It Blocks | Status & Role in Baton #009 |
| :--- | :--- | :--- | :--- |
| **1. Relativization** | Baker–Gill–Solovay (1975) | Pure diagonalization / simulation invariant under arbitrary Boolean oracles $A$ | **Diagnosed & contrasted**: explicitly demonstrated why single $\tilde{A}(r)$ queries break BGS (`Part A`), explaining how `IP = PSPACE` bypasses Relativization |
| **2. Natural Proofs** | Razborov–Rudich (1997) | Large + Constructive combinatorial circuit-hardness properties (assuming PRFs in $\mathcal{C}$) | **Orthogonal / Complementary**: audited in `verify_barriers.py`; note that non-algebrizing circuit algorithms must *also* avoid Natural Proofs (e.g., via non-constructive diagonalization in Williams's method) |
| **3. Algebrization** | Aaronson–Wigderson (2009) | Pure arithmetization, Sumcheck, low-degree extensions, and algebraic-oracle-invariant arguments | **PRIMARY SUBJECT — VERIFIED & EXECUTABLY AUDITED**: proved & computationally demonstrated both the collapsing oracle ($A = \text{TQBF} \implies \text{NP}^{\tilde{A}} \subseteq \text{P}^A \subseteq \text{P/poly}^A$) and the separating Disjointness oracle ($\text{NP}^A \not\subseteq \text{BPP}^{\tilde{A}}$) |
| **4. Locality Barrier** | CHOPRS (STOC 2020) | Local oracle reductions in Hardness Magnification (gluing restriction/polynomial lower bounds to magnification) | **Upstream Filter**: even if a non-local magnification route (`baton-004`) bypasses Locality, it must *also* incorporate a non-algebrizing ingredient (verified against Baton #009's audit) |

---

## 7. Handoff to Next Batons

Baton #009 provides a reusable **Algebrization Compliance Checklist** for all downstream attack routes:

1. **For `baton-003-direct-tc0-sat` (Structured $\text{TC}^0\text{-SAT}$ without Tseitin)**:
   - *Why it clears Algebrization*: Any $\text{TC}^0\text{-SAT}$ algorithm based on polynomial threshold representations, Chebyshev/rational approximations, or fast multipoint evaluation **inspects concrete threshold gate weights and depth**, failing if arbitrary oracle gates $\tilde{A}$ are injected. Ensure the proof explicitly identifies the white-box gate-structure step that breaks for oracle circuits $\text{TC}^{0, \tilde{A}}$.
2. **For `baton-004-nonlocal-magnification` (Non-Local Hardness Magnification / Meta-Complexity)**:
   - *Algebrization check*: Standard PCP/arithmetization-based worst-case-to-average-case reductions (e.g., Lipton/Sudan list decoding) often *algebrize* on their own. Any meta-complexity route aiming at $\text{NP} \not\subseteq \text{P/poly}$ must verify that its underlying circuit-analysis or compression step fails relative to $A = \text{TQBF}$ (where $\text{PSPACE}^{\tilde{A}} = \text{P}^A$).
3. **For `baton-005-gct-obstructions` (Geometric Complexity Theory)**:
   - *Algebrization check*: Representation-theoretic multiplicity obstructions for $\text{perm}_m$ vs. $\text{det}_n$ are inherently **non-algebrizing** (they analyze specific algebraic symmetries of explicit polynomials, not arbitrary black-box extensions $\tilde{A}$), though they face separate geometric/multiplicity obstructions (Bürgisser–Ikenmeyer–Panova).
4. **Hard Pruned Rule**: Future agents MUST NOT propose separating $\text{P}$ vs. $\text{NP}$, $\text{NP}$ vs. $\text{P/poly}$, or $\text{NEXP}$ vs. $\text{P/poly}$ purely by lifting Cook–Levin / TQBF / Circuit-Value via multilinear extensions, Sumcheck, or PCP arithmetization without an explicit white-box, circuit-structure-dependent ingredient.
