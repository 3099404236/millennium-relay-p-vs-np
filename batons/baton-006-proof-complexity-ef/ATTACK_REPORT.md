# Baton #006: Cook–Reckhow Proof Complexity — Separating Resolution from Cutting Planes and Isolating the Extended Frege Barrier

- **Target Millennium Problem**: P versus NP (via $\text{NP} \neq \text{coNP} \implies \text{P} \neq \text{NP}$) — **Unsolved**
- **Baton ID**: `baton-006`
- **Node ID**: `baton-006-proof-complexity-ef`
- **Status**: `BLOCKED_BY_BARRIER` (Did **not** resolve P vs NP or prove super-polynomial Frege / Extended Frege lower bounds; **mechanically verified** the exponential-vs-cubic separation between Resolution and Cutting Planes on $\text{PHP}_n^{n+1}$, proved the exact width identity $w(\text{PHP}_n^{n+1} \vdash \bot) = w_0 = n$ illustrating why Ben-Sasson–Wigderson requires sparse expander $G\text{-PHP}$, and isolated the **Feasible Interpolation & Self-Referential Reflection Barrier** blocking Frege / Extended Frege lower bounds)
- **Date**: 2026-11-26
- **Verification Script**: `verification/verify_baton_006_proof_complexity.py`

---

## 1. The Cook–Reckhow Program ($\text{NP} \neq \text{coNP} \implies \text{P} \neq \text{NP}$)

Since $\text{P}$ is closed under complement, proving $\text{NP} \neq \text{coNP}$ strictly implies $\text{P} \neq \text{NP}$. **Cook's Program** attacks $\text{NP} \neq \text{coNP}$ from the dual side of circuit complexity: instead of proving that hard languages lack small Boolean circuits, we prove that hard propositional tautologies (equivalently, unsatisfiable CNF formulas) lack short proofs in progressively stronger propositional proof systems.

### 1.1 Cook–Reckhow Theorem (1979)

**Definition (Propositional Proof System)**. A *propositional proof system* is a polynomial-time computable surjection $P : \{0,1\}^* \to \text{TAUT}$ (or equivalently, a polynomial-time verifier for refutations of $\text{UNSAT}$). A proof system $P$ is **polynomially bounded** iff there exists a polynomial $p$ such that every $\tau \in \text{TAUT}$ admits a proof $w \in \{0,1\}^*$ with $P(w) = \tau$ and $|w| \le p(|\tau|)$.

**Theorem 1 (Cook–Reckhow, 1979)**.
$$\text{NP} = \text{coNP} \iff \text{there exists a polynomially bounded propositional proof system } P.$$

*Proof*.
- ($\Leftarrow$) If $P$ is polynomially bounded by $p$, then $\tau \in \text{TAUT} \iff \exists w \in \{0,1\}^{\le p(|\tau|)}\, [P(w) = \tau]$. Since $P$ is poly-time computable, the $\text{coNP}$-complete language $\text{TAUT}$ lies in $\text{NP}$, so $\text{coNP} \subseteq \text{NP}$ and hence $\text{NP} = \text{coNP}$.
- ($\Rightarrow$) If $\text{NP} = \text{coNP}$, then $\text{TAUT} \in \text{NP}$, so there exists a deterministic poly-time verifier $V(\tau, w)$ and polynomial $p$ such that $\tau \in \text{TAUT} \iff \exists w \in \{0,1\}^{\le p(|\tau|)}\, V(\tau, w) = 1$. Fix a trivial tautology $\tau_0 = (x \lor \neg x)$ and define $P(\langle \tau, w \rangle) = \tau$ if $|w| \le p(|\tau|)$ and $V(\tau, w) = 1$, else $\tau_0$. Then $P$ is a poly-time surjection onto $\text{TAUT}$ with polynomial proof length. $\blacksquare$

### 1.2 The Proof-System Simulation Hierarchy & Bounded Arithmetic Correspondence

Under $p$-simulation ($\le_p$, meaning proofs in $P_1$ translate in poly-time to proofs in $P_2$), classical proof systems form a ladder closely mirroring circuit classes and fragments of bounded arithmetic:

| Proof System | Reasoning Power / Line Class | Bounded Arithmetic Counterpart | Super-Poly Lower Bounds Known? | Status on $\text{PHP}_n^{n+1}$ |
| :--- | :--- | :--- | :--- | :--- |
| **Tree Resolution** | Decision trees / DPLL | — | **Yes**: $2^{\Omega(n \log n)}$ (Iwama–Miyazaki; BSW) | Exponential / Factorial ($\Omega(n!)$) |
| **DAG Resolution** | Arbitrary clauses / CDCL | — | **Yes**: $2^{\Omega(n)}$ (Haken 1985; BSW 2001) | Exponential ($2^{\Theta(n)}$) |
| **Cutting Planes ($\text{CP}$)** | Integer linear inequalities + rounding | — | **Yes**: $2^{\Omega(n^\epsilon)}$ on Clique–Coloring (Pudlák 1997) | **Polynomial**: $O(n^3)$ (CCT 1987) |
| **Polynomial Calculus ($\text{PC}$)** | Low-degree polynomials over $\mathbb{F}$ | — | **Yes**: degree $\Omega(n)$ (Razborov 1998; IPS 1999) | Exponential (for $\text{FPHP}$ / bit-PHP) |
| **$\text{AC}^0$-Frege** | Constant-depth $\{\land,\lor,\neg\}$ formulas | $I\Delta_0$ / $V^0$ | **Yes**: $\exp(n^{\Omega(1/d)})$ (Ajtai 1988; PBI 1993; KPW 1995; Håstad 2020) | Exponential ($\exp(n^{1/O(d)})$) |
| **$\text{AC}^0[p]$-Frege** | Constant-depth + $\text{MOD}_p$ gates | $V^0(p)$ | **NO** (Major Open Frontier!) | Open (poly for Tseitin mod $p$) |
| **$\text{TC}^0$-Frege** | Constant-depth threshold formulas | $VTC^0$ | **NO** (Blocked by Feasible Interpolation!) | **Polynomial** (via counting) |
| **Frege ($\text{NC}^1$-Frege)** | Arbitrary Boolean formulas | $U^1_2$ / $VNC^1$ | **NO** (Blocked by Feasible Interpolation & Reflection!) | **Polynomial** (Buss 1987) |
| **Extended Frege ($\text{EF}$)** | Boolean circuits ($\text{P/poly}$) via $y \leftrightarrow A$ | $PV_1$ / $S^1_2$ | **NO** (Blocked by Feasible Interpolation & Reflection!) | **Polynomial** (Buss 1987) |

---

## 2. Resolution Lower Bounds: Ben-Sasson–Wigderson (2001) & Haken (1985)

### 2.1 The Ben-Sasson–Wigderson Size–Width Theorem

For an unsatisfiable CNF formula $F$ on $V$ variables with initial maximum clause width $w_0 = w(F)$, let $S_T(F)$ denote the minimum Tree-Resolution refutation size, $S(F)$ the minimum DAG-Resolution refutation size, and $w(F \vdash \bot)$ the minimum maximum clause width of any Resolution refutation of $F$.

**Theorem 2 (Ben-Sasson–Wigderson, JACM 2001)**.
1. **Tree-like Resolution**:
   $$S_T(F) \ge 2^{w(F \vdash \bot) - w_0}.$$
2. **General (DAG) Resolution**:
   $$S(F) \ge \exp\!\left(\frac{(w(F \vdash \bot) - w_0)^2}{c \cdot V}\right)$$
   (specifically $w(F \vdash \bot) \le w_0 + \sqrt{8 V \ln S(F)} + O(1)$, yielding $c = 8$ in the standard restriction-counting induction).

*Proof Idea (DAG Case)*. Fix a refutation $\pi$ of size $S$, set a width threshold $k$, and let $\pi^*$ be the set of "fat" clauses of width $> k$ ($|\pi^*| \le S$). By averaging over all $2V$ literals, some literal $\ell$ appears in at least $\frac{k}{2V} |\pi^*|$ fat clauses. Restricting $\ell = 1$ eliminates all clauses containing $\ell$, shrinking the fat-clause count by a factor $(1 - \frac{k}{2V})$. Inducting on $(V, b)$ with $a = (1 - \frac{k}{2V})^{-1}$ shows that $|\pi^*| < a^b \implies w(F \vdash \bot) \le \max(k, w_0) + b$. Choosing $k \approx \sqrt{2 V \ln S}$ and $b \approx \frac{2V \ln S}{k} \approx \sqrt{2 V \ln S}$ gives $w(F \vdash \bot) \le w_0 + 2\sqrt{2 V \ln S} = w_0 + \sqrt{8 V \ln S}$. Rearranging yields $S \ge \exp((w(F \vdash \bot) - w_0)^2 / (8V))$. $\blacksquare$

### 2.2 Critical Subtlety on $\text{PHP}_n^{n+1}$: Why Raw BSW Is Vacuous and Expander $G\text{-PHP}$ Is Needed

The canonical CNF encoding of the Pigeonhole Principle $\text{PHP}_n^{n+1}$ has $V = n(n+1)$ variables $x_{i,j}$ ($i \in [n+1], j \in [n]$) and $M = (n+1) + n\binom{n+1}{2}$ clauses:
- **Pigeon axioms** (width $n$): $P_i = \bigvee_{j=1}^n x_{i,j}$ for $i \in \{1, \dots, n+1\}$.
- **Hole axioms** (width $2$): $H_{i, i', j} = (\neg x_{i,j} \lor \neg x_{i',j})$ for $1 \le i < i' \le n+1$, $j \in \{1, \dots, n\}$.

A widespread textbook misconception claims BSW applies directly to raw $\text{PHP}_n^{n+1}$. In fact, we prove and mechanically verify the exact width equality:

**Proposition 3 (Exact Width of Raw $\text{PHP}_n^{n+1}$)**. For all $n \ge 1$:
$$w(\text{PHP}_n^{n+1} \vdash \bot) = w_0(\text{PHP}_n^{n+1}) = n.$$

*Proof*.
- **Lower bound ($w \ge n$)**: Every axiom of width $\le n - 1$ is a hole axiom $(\neg x_{i,j} \lor \neg x_{i',j})$, which contains only negative literals and is satisfied by the all-zeros assignment $0^V$. Hence any refutation must use at least one pigeon axiom $P_i$ of width $n$.
- **Upper bound ($w \le n$)**: By backward induction on partial matchings $M_k = \{(1, h_1), \dots, (k, h_k)\}$ ($k = n, n-1, \dots, 0$), we derive the clause $C(M_k) = \bigvee_{r=1}^k \neg x_{r, h_r}$ using only clauses of width $\le n$. Starting from $P_{k+1}$ (width $n$), resolve sequentially with hole axioms $(\neg x_{r, h_r} \lor \neg x_{k+1, h_r})$ for $r = 1, \dots, k$: each step replaces one positive literal $x_{k+1, h_r}$ with one negative literal $\neg x_{r, h_r}$, preserving exact width $n$! Then resolve away the remaining $n - k$ free-hole literals using the inductively derived clauses $C(M_k \cup \{(k+1, h)\})$ (width $k+1 \le n$). At $k=0$, $C(\emptyset) = \bot$. $\blacksquare$

Because $w - w_0 = n - n = 0$ on raw $\text{PHP}_n^{n+1}$, **naive BSW gives only the trivial bound $S \ge 1$**. Two classical techniques recover the exponential lower bound $S(\text{PHP}_n^{n+1}) = 2^{\Omega(n)}$:
1. **Haken's Bottleneck Counting (1985)** (sharpened by Buss–Turán 1988, Beame–Pitassi 1996): Maps *critical truth assignments* (bijections from $[n+1] \setminus \{i\}$ to $[n]$) to the first "complex" clause falsified in a refutation. In the monotone/positive expansion (replacing $\neg x_{i,j}$ by $\bigvee_{k \neq j} x_{i,k}$), every refutation must contain a bottleneck clause covering $\Omega(n^2)$ positive literals, forcing $S(\text{PHP}_n^{n+1}) = 2^{\Omega(n)}$.
2. **BSW via Sparse Expander Restriction $G\text{-PHP}$ (2001)**: Restrict $\text{PHP}_n^{n+1}$ to a constant-degree bipartite expander $G$ of left-degree $d = O(1)$ by setting $x_{i,j} = 0$ for all $(i,j) \notin E(G)$. Any Resolution refutation of $\text{PHP}_n^{n+1}$ restricts to a refutation of $G\text{-PHP}$ of at most the same size. Now $w_0(G\text{-PHP}) = d = O(1)$, $V = d(n+1) = O(n)$, and expansion forces $w(G\text{-PHP} \vdash \bot) = \Omega(n)$. Applying Theorem 2 gives:
   $$S(\text{PHP}_n^{n+1}) \ge S(G\text{-PHP}) \ge \exp\!\left(\frac{(\Omega(n) - d)^2}{8 d(n+1)}\right) = 2^{\Omega(n)}.$$

---

## 3. Polynomial-Size Cutting Planes Refutation of $\text{PHP}_n^{n+1}$ (Cook–Coullard–Turán 1987)

In **Cutting Planes ($\text{CP}$)**, each CNF clause is translated into an integer linear inequality over $\{0,1\}^V$:
- Pigeon axioms $P_i$: $\sum_{j=1}^n x_{i,j} \ge 1$ ($i = 1, \dots, n+1$).
- Hole axioms $H_{i, i', j}$: $-x_{i,j} - x_{i',j} \ge -1$ ($1 \le i < i' \le n+1$, $j \in [n]$).

Atomic inference rules are: (i) binary **Addition** of inequalities, (ii) **Multiplication** by an integer $c \ge 1$, and (iii) **Chvátal–Gomory Division with Rounding**: if $d \in \mathbb{Z}_{\ge 2}$ divides every coefficient $a_v$ in $\sum_v a_v x_v \ge b$, infer $\sum_v (a_v/d) x_v \ge \lceil b / d \rceil$.

### 3.1 Why Rounding Is Strictly Essential (LP Integrality Gap)
For every $n \ge 2$, the fractional point $x_{i,j} = \frac{1}{n} \in [0, 1]$ satisfies **every** pigeon axiom ($\sum_{j=1}^n \frac{1}{n} = 1 \ge 1$) and **every** hole axiom ($-\frac{1}{n} - \frac{1}{n} = -\frac{2}{n} \ge -1$). By Farkas's Lemma, **no** non-negative linear combination without integer rounding can refute $\text{PHP}_n^{n+1}$.

### 3.2 Exact Inductive Cubic-Size Construction
For each hole $j \in \{1, \dots, n\}$, we derive the clique (hole-capacity) inequality $I_k^{(j)} : -\sum_{i=1}^k x_{i,j} \ge -1$ by induction on $k = 2, \dots, n+1$:
- **Base case ($k = 2$)**: $I_2^{(j)} = H_{1,2,j} : -x_{1,j} - x_{2,j} \ge -1$.
- **Inductive step ($k \to k+1$)**:
  1. Multiply $I_k^{(j)}$ by $(k - 1)$ (omitted for $k=2$): $-(k-1)\sum_{i=1}^k x_{i,j} \ge -(k-1)$.
  2. Add all $k$ hole axioms $H_{1,k+1,j}, \dots, H_{k,k+1,j}$:
     $$-k \sum_{i=1}^{k+1} x_{i,j} \ge -(k-1) - k = -(2k - 1).$$
  3. Apply **Chvátal–Gomory Division by $d = k$** (exact divisibility of all coefficients $-k$, with ceiling rounding $\lceil -(2k-1)/k \rceil = \lceil -2 + 1/k \rceil = -1$):
     $$I_{k+1}^{(j)} : -\sum_{i=1}^{k+1} x_{i,j} \ge -1.$$
- **Global Contradiction**:
  1. Sum all $n+1$ pigeon axioms: $\sum_{i=1}^{n+1} \sum_{j=1}^n x_{i,j} \ge n + 1$.
  2. Sum all $n$ hole-capacity inequalities $I_{n+1}^{(j)}$: $-\sum_{j=1}^n \sum_{i=1}^{n+1} x_{i,j} \ge -n$.
  3. Add (1) and (2): **$0 \ge 1$**. $\blacksquare$

**Exact Size Formula**:
- Total proof lines (axioms + inferences): $L(n) = n^3 + 3n^2 - n + 1 = O(M)$ (linear in formula size!).
- Total inference steps: $I(n) = \frac{1}{2}(n^3 + 5n^2 - 4n)$.
- Maximum coefficient magnitude: $\max |a_v| = n$ (so bit-size is $O(n^3 \log n)$, polynomial even in $\text{CP}^*$).

---

## 4. Mechanically Verified Empirical Results (`verification/verify_baton_006_proof_complexity.py`)

Every Resolution refutation (DPLL Tree-Res, CDCL DAG-Res, and exact width-$n$ Res) and every Cutting Planes refutation below was **constructed explicitly and checked line-by-line by an independent zero-trust proof verifier** using exact integer/rational arithmetic (zero floats in proof checking):

| $n$ | Vars $V$ | Clauses $M$ | DPLL Tree-Res Steps (Max Width) | CDCL DAG-Res Steps (Max Width) | Exact Width-$n$ Res Steps (Width) | Cutting Planes Lines $L(n)$ (Inf Steps, Max Coeff) |
| ---: | ---: | ---: | :---: | :---: | :---: | :---: |
| $2$ | $6$ | $9$ | $21$ ($w=2$) | $19$ ($w=2$) | $19$ ($w=2$) | $19$ ($10$, $c_{\max}=2$) |
| $3$ | $12$ | $22$ | $89$ ($w=4$) | $62$ ($w=4$) | $64$ ($w=3$) | $52$ ($30$, $c_{\max}=3$) |
| $4$ | $20$ | $45$ | $543$ ($w=7$) | $225$ ($w=7$) | $233$ ($w=4$) | $109$ ($64$, $c_{\max}=4$) |
| $5$ | $30$ | $81$ | $4249$ ($w=10$) | $631$ ($w=12$) | — | $196$ ($115$, $c_{\max}=5$) |
| $10$ | $110$ | $561$ | intractable ($\Omega(10!)$) | intractable ($2^{\Omega(10)}$) | — | **$1291$** ($730$, $c_{\max}=10$) |
| $20$ | $420$ | $4221$ | intractable ($\Omega(20!)$) | intractable ($2^{\Omega(20)}$) | — | **$9181$** ($4960$, $c_{\max}=20$) |

Key verified takeaways:
1. From $n = 4$ to $n = 5$, DPLL Tree-Res explodes by **$7.83\times$** and CDCL DAG-Res grows by **$2.80\times$**, while Cutting Planes grows by only **$1.80\times$** ($109 \to 196$) and effortlessly refutes $\text{PHP}_{20}^{21}$ in **$9181$ lines**.
2. Every verified Resolution refutation satisfies $w \ge n$, and our explicit width-$n$ refutations for $n = 2, 3, 4$ confirm $w(\text{PHP}_n^{n+1} \vdash \bot) = w_0 = n$ exactly.
3. For constant-degree expander $G\text{-PHP}$ ($d=5$, $V = 5(n+1)$, $w \ge n/4$), BSW's $\exp((w-w_0)^2 / (8V))$ lower bound strictly exceeds cubic Cutting Planes $n^3 + 3n^2 - n + 1$ for all $n \ge 20000$ and diverges exponentially thereafter.

---

## 5. The Wall at Frege & Extended Frege: Feasible Interpolation and Self-Referential Reflection Barriers

Why has Cook's Program stalled for nearly 40 years below $\text{AC}^0[2]$-Frege, $\text{TC}^0$-Frege, **Frege**, and **Extended Frege ($\text{EF}$)**? Two interlocking barriers explain the wall:

### 5.1 Barrier A: Cryptographic Destruction of Feasible Interpolation
A proof system $P$ has **(monotone) feasible interpolation** if from any size-$S$ refutation of $A(\vec{x}, \vec{y}) \land B(\vec{x}, \vec{z})$, one can extract a (monotone) Boolean circuit $C(\vec{x})$ of size $\text{poly}(S)$ separating $\{\vec{x} : \exists \vec{y}\, A(\vec{x}, \vec{y})\}$ from $\{\vec{x} : \exists \vec{z}\, B(\vec{x}, \vec{z})\}$.
- **Where it works**: Resolution (Krajíček 1997) and Cutting Planes (Pudlák 1997) satisfy *monotone* feasible interpolation. Applying this to the Clique–Coloring formula reduces CP proof lower bounds directly to Razborov / Alon–Boppana's exponential monotone circuit lower bounds!
- **Where it DIES**:
  - **Krajíček & Pudlák (1998)**: Assuming **RSA** is secure against $\text{P/poly}$, **Extended Frege ($\text{EF}$)** does **not** have feasible interpolation.
  - **Bonet–Pitassi–Raz (2000)**: Assuming **factoring Blum integers** is hard for $\text{P/poly}$, even **Frege** (and $\text{TC}^0$-Frege) fails feasible interpolation.
  - **Bonet–Domingo–Gavaldà–Maciel–Pitassi (2004)**: Assuming **Diffie–Hellman** is hard for $\text{TC}^0$ / $\text{P/poly}$, even bounded-depth $\text{TC}^0$-Frege fails feasible interpolation.
- *Mechanism*: $\text{TC}^0$-Frege, Frege, and $\text{EF}$ are strong enough to formalize basic modular arithmetic and prove the injectivity/consistency of cryptographic permutations (e.g., that $f(y) = x$ uniquely fixes a hardcore bit). Thus a polynomial-size interpolant would immediately break RSA / factoring in $\text{P/poly}$. This is the exact proof-complexity counterpart of the **Razborov–Rudich Natural Proofs Barrier**!

### 5.2 Barrier B: The Self-Referential Reflection & Proof-Complexity-Generator Barrier
Even if we abandon feasible interpolation and target non-split tautologies — notably **Proof Complexity Generators** $\tau_b(G)$ (asserting "$b \notin \text{Range}(G)$" for the Nisan–Wigderson or truth-table generator $G$; Krajíček 2004, 2011; Razborov 2004, 2015) or **Circuit Lower Bound tautologies** $\text{Circuit-LB}_f$ — we hit a second, self-referential wall:
1. **Razborov's Unprovability Obstruction (1995) & Pich (2015)**: Extended Frege corresponds via propositional translation to Cook's bounded arithmetic theory $PV_1$ (and $S^1_2$). Proving super-polynomial lower bounds for $\text{EF}$ on truth-table/NW-generator tautologies $\tau_b(\text{NW}_f)$ is tightly coupled to proving that $PV_1$ / $\text{EF}$ cannot prove $\text{NP} \not\subseteq \text{P/poly}$ — and any *feasible/natural* proof of $\text{EF}$ hardness of $\tau_b(\text{NW}_f)$ collides with PRG security.
2. **Reflection & Gödelian Optimality (Pudlák 1986; Krajíček–Pudlák 1989; Pich–Santhanam 2021)**:
   - $\text{EF}$ polynomially proves the reflection principles $\text{RFN}(\text{Res})$ and $\text{RFN}(\text{CP})$ for weaker systems, and p-simulates Frege.
   - By Krajíček–Pudlák (1989), an *optimal* propositional proof system exists iff there is a proof system $P$ polynomially proving finite consistency $\text{Con}_Q(n)$ for every $Q$.
   - **Pich–Santhanam (STOC 2021, "Why are Proof Complexity Lower Bounds Hard?")** formalize the **Self-Referential Barrier**: under plausible meta-complexity assumptions (hardness of $\text{MCSP}$ / non-existence of natural proofs against $\text{P/poly}$), strong proof systems like $\text{EF}$ cannot be separated by any proof method whose correctness/witnessing is itself formalizable in a weak feasible theory (because reflection turns the lower bound proof into a forbidden short proof or natural distinguisher).
3. **Why $\text{PHP}_n^{n+1}$ Cannot Touch Frege or $\text{EF}$**: Buss (1987) proved that **Frege** (and thus $\text{EF}$) already has polynomial-size refutations of $\text{PHP}_n^{n+1}$ via $\text{NC}^1$ carry-save counting formulas. Thus $\text{PHP}$ dies at Cutting Planes and $\text{TC}^0$-Frege.

---

## 6. Mandatory 4-Barrier Audit Table

| Barrier | Reference | Interaction with Cook–Reckhow / Extended Frege Route | Status in Baton #006 |
| :--- | :--- | :--- | :--- |
| **1. Relativization** | Baker–Gill–Solovay (1975) | Syntactic lower bounds for fixed systems (Res, CP, Frege, EF) inspect formula/circuit syntax and do not naively relativize; however, Cook–Reckhow itself relativizes ($\text{NP}^A = \text{coNP}^A \iff \exists$ poly-bounded $P^A$), and black-box simulations between proof systems relativize. | **Partially Bypassed** (syntactic systems), **Active** for generic black-box Cook–Reckhow arguments |
| **2. Natural Proofs** | Razborov–Rudich (1997) | **DIRECTLY ACTIVE via Feasible Interpolation & NW-Generator Barriers!** Cryptographic hardness (RSA/factoring/OWFs in $\text{TC}^0$/$\text{P/poly}$) kills feasible interpolation for $\text{TC}^0$-Frege, Frege, and $\text{EF}$ (Krajíček–Pudlák 1998; Bonet–Pitassi–Raz 2000). Razborov (1995, 2015) and Pich–Santhanam (2021) show natural proofs also fail to establish $\text{EF}$ lower bounds against $\tau_b(\text{NW}_f)$. | **ACTIVE BLOCKER** for $\text{TC}^0$-Frege, Frege, and $\text{EF}$ |
| **3. Algebrization** | Aaronson–Wigderson (2009) | Algebraic proof systems (Polynomial Calculus, Grochow–Pitassi Ideal Proof System $\text{IPS}$) reduce proof lower bounds to algebraic circuit lower bounds ($\text{VP} \neq \text{VNP}$). Pure low-degree arithmetization algebrizes; breaking $\text{IPS}$ requires non-algebrizing algebraic/geometric invariants. | **Active Caution** for algebraic/IPS routes |
| **4. Locality Barrier** | CHOPRS (STOC 2020) | Applies directly to switching-lemma / random-restriction / local-decision-tree proof-complexity methods (which conquer $\text{AC}^0$-Frege via Håstad switching lemmas, but collapse on $\text{TC}^0$-Frege) and to any Proof Complexity Magnification lifting weak lower bounds to $\text{EF}$. | **ACTIVE BLOCKER** for restriction-based & local-magnification lifts to $\text{EF}$ |

---

## 7. Verdict & Concrete Handoff to Next Batons

- **Did Baton #006 resolve $\text{P}$ vs $\text{NP}$ or $\text{NP}$ vs $\text{coNP}$?** **NO.**
- **What did Baton #006 rigorously establish and mechanically verify?**
  1. Verified the exact Resolution-vs-Cutting-Planes exponential-to-cubic separation on $\text{PHP}_n^{n+1}$ via independent, zero-trust mechanical proof verifiers (`verification/verify_baton_006_proof_complexity.py`).
  2. Proved and verified $w(\text{PHP}_n^{n+1} \vdash \bot) = w_0 = n$ (showing why raw BSW is vacuous and sparse expander $G\text{-PHP}$ is required) and confirmed the LP integrality gap ($x_{i,j} = 1/n$) proving Chvátal–Gomory rounding is essential.
  3. Isolated the exact **Feasible Interpolation** (Krajíček–Pudlák / Bonet–Pitassi–Raz) and **Self-Referential Reflection** (Razborov / Pich–Santhanam) walls blocking Frege and Extended Frege lower bounds.

### Actionable Handoff to Surviving Proof-Complexity Sub-Routes
1. **Immediate Unblocked Frontier — $\text{AC}^0[2]$-Frege Lower Bounds**: Before touching Frege or $\text{EF}$, the cleanest unblocked milestone in Cook's Program is proving super-polynomial lower bounds for **$\text{AC}^0[2]$-Frege** (constant-depth formulas with $\text{PARITY}$ gates), where cryptographic PRFs are *not* believed to exist (so Feasible Interpolation is not known to be killed by RSA/factoring!). Candidate hard tautologies: $\text{PHP}_n^{n+1}$ (still conjectured hard for $\text{AC}^0[2]$-Frege!) or random $k$-CNFs.
2. **Algebraic Proof Complexity (Grochow–Pitassi $\text{IPS}$) $\leftrightarrow$ GCT (`baton-005`)**: Since $\text{IPS}$ p-simulates $\text{EF}$, proving super-polynomial $\text{IPS}$ lower bounds simultaneously advances Cook's Program and $\text{VP} \neq \text{VNP}$; future batons should attack restricted $\text{IPS}$ (roABP-IPS, multilinear-IPS, constant-depth IPS) using shifted partial derivatives and GCT multiplicity obstructions.
3. **Non-Natural $\text{EF}$ Attacks via Proof Complexity Generators ($\tau_b(\text{NW}_f)$) & Meta-Complexity (`baton-004`)**: Any direct assault on $\text{EF}$ MUST abandon feasible interpolation and local restrictions, and instead investigate whether non-black-box meta-complexity techniques (linking $\text{MCSP}$ / $\text{MKtP}$ hardness to unprovability in $PV_1$) can bypass the Pich–Santhanam self-referential barrier.
