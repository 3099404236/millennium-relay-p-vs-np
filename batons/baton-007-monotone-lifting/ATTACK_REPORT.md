# Baton #007: Monotone Circuit Lower Bounds, GPW Query-to-Communication Lifting, and the Non-Monotone Cancellation Wall

- **Target Millennium Problem**: P versus NP (Clay Mathematics Institute — **Unsolved**)
- **Baton ID**: `baton-007` (`baton-007-monotone-lifting`)
- **Status**: `BLOCKED_BY_BARRIER` (Did **not** resolve P vs NP; mapped and computationally verified the complete Razborov/Alon–Boppana & Karchmer–Wigderson/GPW lifting pipeline, and pinpointed the exact mathematical wall blocking monotone methods from reaching general circuits: **Tardos's 1988 Exponential Gap & Non-Monotone Algebraic Cancellation**)
- **Date**: 2026-11-26
- **Verification Script**: `python verification/verify_baton_007_monotone_lifting.py`

---

## 1. Executive Summary & Core Question

One of the greatest triumphs of circuit complexity is the proof of **exponential lower bounds for monotone Boolean circuits** (circuits over $\{\land, \lor\}$ without `NOT` gates) computing explicit $\text{NP}$ functions such as $k$-CLIQUE and lifted monotone CSP-SAT:

1. **Razborov (1985)** and **Alon–Boppana (1987)** proved exponential monotone circuit lower bounds $\exp(\Omega((v/\log v)^{1/3}))$ for $k$-CLIQUE via the **Method of Approximations** and the **Erdős–Rado Sunflower Lemma**.
2. **Karchmer–Wigderson (1988)**, **Raz–McKenzie (1999)**, **Göös–Pitassi–Watson (GPW, FOCS 2015 / SICOMP 2020)**, and **Garg–Göös–Kamath–Sokolov (GGKS, STOC 2018)** unified monotone formula and monotone circuit lower bounds via **query-to-communication lifting**, reducing monotone circuit size to proof/query complexity (Resolution / Nullstellensatz / Cutting Planes) of unsatisfiable CSPs.

This raises the central question of Baton #007:

> **Core Question**: Can the Razborov/Alon–Boppana approximation lattice or the Karchmer–Wigderson + GPW query-to-communication lifting framework be extended across the negation boundary to yield super-polynomial lower bounds for **general** (non-monotone) circuits ($\text{NP} \not\subseteq \text{P/poly}$)?

**Verdict**: **NO — blocked by a provable, quantitative structural wall (Tardos 1988; Razborov 1985b; Markov 1958 / Fischer 1975).** Monotone methods are **fundamentally blind** to polynomial-time algorithms that exploit **non-monotone algebraic cancellation**. Worse still, by Markov/Fischer's negation-count theorem, introducing merely **$\lceil \log_2(N+1) \rceil$ `NOT` gates** suffices to trigger the full exponential collapse from $\exp(\Omega(N^{1/6 - o(1)}))$ monotone size down to $\mathrm{poly}(N)$ general circuit size.

---

## 2. Pillar I: Razborov / Alon–Boppana & Erdős–Rado Sunflower Approximations

### 2.1 The Erdős–Rado Sunflower Lemma & Approximator Lattice
A collection of $r$ distinct sets $S_1, \dots, S_r$ forms an **$r$-sunflower** with **core** $K$ if $S_i \cap S_j = K$ for all $i \neq j$ (equivalently, the **petals** $P_i = S_i \setminus K$ are pairwise disjoint).

> **Lemma (Erdős–Rado 1960)**: Every family $\mathcal{F}$ of sets of size at most $\ell$ with $|\mathcal{F}| > \ell!(r-1)^\ell$ contains an $r$-sunflower.

In Razborov's Method of Approximations for $k$-CLIQUE on $v$-vertex graphs (input length $N = \binom{v}{2}$), every gate $g$ of a monotone circuit $C$ is approximated by a small DNF $\tilde{g} = \bigvee_{A \in \mathcal{A}} \lceil A \rceil$, where each $A \subseteq [v]$ has $|A| \le \ell$, $\lceil A \rceil(G) = 1$ iff $A$ forms a clique in $G$, and $|\mathcal{A}| \le m = \ell!(r-1)^\ell$:

- **Approximate OR ($\sqcup$)**: Take $\mathcal{A} \cup \mathcal{B}$ and repeatedly **pluck** any $r$-sunflower $\{S_1, \dots, S_r\} \mapsto K$ until $|\mathcal{A}| \le m$.
- **Approximate AND ($\sqcap$)**: Distribute $\lceil A \rceil \land \lceil B \rceil \mapsto \lceil A \cup B \rceil$, **discard** all sets of size $> \ell$, and pluck $r$-sunflowers until size $\le m$.

### 2.2 Exact Error Analysis on $\mathcal{D}_+$ and $\mathcal{D}_-$
Evaluate approximation error on two adversarial test distributions:
- **Positive test instances ($\mathcal{D}_+$)**: All $\binom{v}{k}$ minimal $k$-clique graphs (each has only $\binom{k}{2}$ edges).
- **Negative test instances ($\mathcal{D}_-$)**: Complete $(k-1)$-partite graphs $G_c$ induced by uniform vertex colorings $c: [v] \to [k-1]$ (edge $\{u,w\} \in E(G_c) \iff c(u) \neq c(w)$).

For a single pluck $\{S_1, \dots, S_r\} \mapsto K$:
1. **Zero False Negatives on $\mathcal{D}_+$**: Because $K \subseteq S_i$, every graph containing clique $S_i$ automatically contains clique $K$; hence $\lceil K \rceil(G) \ge \bigvee_{i=1}^r \lceil S_i \rceil(G)$ pointwise for *every* graph $G$.
2. **Exact Independence Formula for False Positives on $\mathcal{D}_-$**: A vertex set $A$ is a clique in $G_c$ iff $c$ is injective on $A$. Conditioned on $c|_K$ being injective, the events $E_i = \{c \text{ is injective on } K \cup P_i\}$ depend on **pairwise disjoint** petals $P_1, \dots, P_r$ and are therefore **mutually independent**:
   $$\Pr_{c \sim [k-1]^v}\!\Big[\lceil K \rceil(G_c) = 1 \;\land\; \bigwedge_{i=1}^r \lceil S_i \rceil(G_c) = 0\Big] = \Pr[c \text{ inj on } K] \cdot \prod_{i=1}^r \Big(1 - \Pr[c \text{ inj on } S_i \mid c \text{ inj on } K]\Big).$$

For $k = 3$ ($k-1 = 2$ colors), $\ell = 2$, and any $r$-sunflower of edges (whether a star with $|K|=1$ or a matching with $K = \emptyset$), every petal yields conditional acceptance probability $1/2$, so the exact false-positive probability is **$2^{-r}$**. Choosing $\ell = \Theta((v/\log v)^{1/3})$, $r = \Theta((v/\log v)^{1/3} \log v)$, and $k = \lfloor (v/\log v)^{2/3} \rfloor$ yields Alon–Boppana's lower bound:
$$C_+(\text{$k$-CLIQUE}_v) \ge \exp\!\left(\Omega\!\left(\left(\frac{v}{\log v}\right)^{1/3}\right)\right) = \exp\!\left(\Omega\!\left(N^{1/6 - o(1)}\right)\right).$$

**Computational Verification (`verify_baton_007_monotone_lifting.py`, Module 1)**:
- Exact backtracking $3$-sunflower extraction confirmed Erdős–Rado's bound $2!(3-1)^2 = 8$ exhaustively across all $10/10$ nine-edge subgraphs of $K_5$, while certifying that $C_5$ ($5$ edges) and $2K_3$ ($6$ edges) are $3$-sunflower-free.
- Exact plucking checks over all minimal $3$-cliques ($\mathcal{D}_+$) and all $2^v$ $2$-colorings ($\mathcal{D}_-$) confirmed $0$ false negatives and exact false-positive counts $4/32$ ($v=5$, $3$-star) and $8/64$ ($v=6$, both $3$-star and $3$-matching), plus exact count $441/729 = (7/9)^2$ for $k=4, v=6, \ell=3, r=2$ across all $3^6 = 729$ $3$-colorings.

---

## 3. Pillar II: Karchmer–Wigderson Games & GPW Query-to-Communication Lifting

### 3.1 Karchmer–Wigderson Equivalence ($\mathrm{mKW}_f$ vs. $\mathrm{KW}_f$)
For any Boolean function $f: \{0,1\}^N \to \{0,1\}$, Alice receives $x \in f^{-1}(1)$ and Bob receives $y \in f^{-1}(0)$:
- **General KW game ($\mathrm{KW}_f$)**: Output any $i \in [N]$ such that $x_i \neq y_i$ (allowing both $(1,0)$ and $(0,1)$). Minimal general formula depth equals $D^{\mathrm{cc}}(\mathrm{KW}_f)$; minimal formula size equals protocol leaf count.
- **Monotone KW game ($\mathrm{mKW}_f$, for monotone $f$)**: Output any $i \in [N]$ such that $x_i = 1$ and $y_i = 0$. Minimal monotone formula depth equals $D^{\mathrm{cc}}(\mathrm{mKW}_f)$; minimal monotone formula size equals protocol leaf count; and minimal **monotone circuit size** equals minimal **rectangle-DAG (triangle-DAG)** size solving $\mathrm{mKW}_f$ (Raz–McKenzie 1999; Sokolov 2017; GGKS 2018).

### 3.2 GPW Query-to-Communication Lifting Pipeline
Let $S \subseteq \{0,1\}^n \times \mathcal{O}$ be a total search problem (typically $\mathrm{Search}(\phi)$ for an unsatisfiable CNF $\phi$, such as a Tseitin or pebbling contradiction) with deterministic decision tree depth $D^{\mathrm{dt}}(S)$ (or Resolution/Nullstellensatz/Cutting-Planes refutation size). Define the **index gadget** $\mathrm{IND}_m: [m] \times \{0,1\}^m \to \{0,1\}$ by $\mathrm{IND}_m(a, b) = b_a$, and consider the lifted search problem $S \circ \mathrm{IND}_m^n$ where $z_i = (y_i)_{x_i}$.

> **Theorem (Göös–Pitassi–Watson 2015/2020; GGKS 2018)**:
> 1. **Tree Lifting (Formulas)**: For $m = \mathrm{poly}(n)$ (improved to $m = O(n \log n)$ by Lovett–Meka–Mertz–Pitassi–Zhang 2022),
>    $$D^{\mathrm{cc}}(S \circ \mathrm{IND}_m^n) = \Theta\!\left(D^{\mathrm{dt}}(S) \cdot \log m\right).$$
> 2. **DAG Lifting (Circuits)**: Rectangle-DAG size for $\mathrm{Search}(\phi) \circ \mathrm{IND}_m^n$ is lower-bounded by $\exp(\Omega(\text{Resolution-width}(\phi)))$ (and via Cutting Planes / Nullstellensatz lifting for stronger gadgets), embedding directly into $\mathrm{mKW}_f$ for an explicit monotone $\text{NP}$ function $f$ to yield exponential monotone circuit lower bounds $\exp(\Omega(N^\epsilon))$.

**How the GPW Simulation Works**: Whenever a communication protocol partitions $A \times B$, the GPW simulation tracks **blockwise min-entropy** of Alice's pointer set $A \subseteq [m]^n$. As long as $A$ stays dense in every unqueried block $i \in [n] \setminus I$, Alice's pointers look nearly uniform on block $i$, so Bob's truth table $y_i$ reveals almost nothing about $z_i$. The simulator only queries $z_i$ in the decision tree when Alice's transcript drops block $i$'s min-entropy by $\Omega(\log m)$ bits—forcing $\Omega(\log m)$ communication bits per decision tree query!

### 3.3 Why Lifting Breaks at the Non-Monotone Boundary (Verified Computationally)
Our verification script (`verify_baton_007_monotone_lifting.py`, Modules 2 & 3) demonstrates both halves of this phenomenon on concrete finite instances:

1. **GPW Lifting on $\mathrm{Tseitin}(K_3) \circ \mathrm{IND}_m^3$ (Module 3)**:
   - Exhaustive minimax DP proves exact deterministic query depth $D^{\mathrm{dt}}(\mathrm{Tseitin}(K_3)) = 3$.
   - Lifting via $\mathrm{IND}_2$ ($8 \times 64 = 512$ input pairs) gives an exact simulated communication protocol of depth $3(\log_2 2 + 1) = 6$ bits verified on $512/512$ inputs.
   - Exhaustive search over all $2^8 - 1 = 255$ nonempty Alice subsets confirms the **exact maximum monochromatic rectangle area** is $64/512 = 1/8 = \frac{1}{2m^2}$, generalizing to exact density $\frac{1}{2m^2}$ for $m = 2, 4, 8$ and proving $D^{\mathrm{cc}}(\mathrm{Tseitin}(K_3) \circ \mathrm{IND}_m^3) \ge 2\log_2 m + 1$ (explicitly exhibiting the $\Theta(\log m)$ GPW entropy blowup per certified constraint).

2. **Monotone vs. General KW Collapse on `3-CLIQUE vs 2-COLORABLE` ($v=5$, Module 2)**:
   - On $v = 5$ vertices ($10$ edges), let $X$ be all $\binom{5}{3} = 10$ minimal triangles and $Y_{\text{nonempty}}$ be all $15$ nonempty complete bipartite graphs ($150$ pairs; $160$ including $\emptyset$).
   - **Monotone KW ($\mathrm{mKW}$)**: For every edge $e = \{u,w\}$, pairing triangle $\{u,w,z\}$ with the $2$-coloring separating $\{u,w\}$ from the remaining $3$ vertices makes $e$ the **unique** $(x_e=1, y_e=0)$ witness! Thus every single one of the $10$ maximal monotone rectangles $R_e^+$ is strictly unavoidable: exact rectangle cover $C^N(\mathrm{mKW}) = 10$, max rectangle area $= 3 \times 7 = 21$, forcing $D^{\mathrm{cc}}(\mathrm{mKW}) \ge \lceil \log_2 10 \rceil = 4$ bits (matched by an explicit $6$-bit two-way protocol with $30$ verified monochromatic leaves).
   - **General KW ($\mathrm{KW}$)**: Allowing $(x_e=0, y_e=1)$ shortcuts jumps the max monochromatic rectangle area from $21 \to 56$ ($7 \times 8$) and drops the cover number strictly from $10 \to 7$ via the explicit cover `+(0,1)` plus the $6$ negative rectangles `-(0,w), -(1,w)` for $w \in \{2,3,4\}$!
   - **Structural takeaway**: In $\mathrm{mKW}_f$, Alice's minterms $X$ and Bob's maxterms $Y$ lock into a bipartite partial-order structure where lifted gadgets $S \circ \mathrm{IND}_m^n$ embed faithfully. In general $\mathrm{KW}_f$, the symmetric $(0,1)$ witnesses create massive non-monotone rectangle shortcuts outside the lifted search relation, shattering the reduction!

---

## 4. Pillar III: The Non-Monotone Cancellation Wall (Tardos 1988)

The failure to lift monotone lower bounds to general circuits is **not** a mere gap in our proof techniques—it reflects a provable **exponential separation** between monotone circuit complexity and general circuit complexity for the *same* monotone functions.

### 4.1 Tardos's Theorem (1988) via Lovász's $\vartheta$-Function
For any graph $G = (V, E)$, **Lovász's Sandwich Theorem (1979)** gives:
$$\omega(G) \le \vartheta(\bar{G}) \le \chi(G),$$
where $\vartheta(\bar{G})$ has the dual semidefinite (eigenvalue-minimization) characterization:
$$\vartheta(\bar{G}) = \min \left\{ \lambda_{\max}(A) : A = A^\top \in \mathbb{R}^{v \times v},\; A_{ii} = 1,\; A_{ij} = 1 \text{ whenever } \{i,j\} \in E(G) \right\}.$$

Define Tardos's monotone Boolean function $f_{\text{Tardos}, k}(G) = \mathbf{1}\!\left[\vartheta(\bar{G}) \ge k - \frac{1}{2}\right]$:
1. **Monotonicity**: Adding an edge to $G$ only *adds* equality constraints $A_{ij} = 1$, so the minimum over feasible matrices $A$ cannot decrease; hence $f_{\text{Tardos}, k}$ is **monotone**.
2. **Exponential Monotone Lower Bound**: Every $k$-clique graph satisfies $\vartheta(\bar{G}) \ge \omega(G) \ge k$ (every feasible $A$ contains an all-ones $k \times k$ principal submatrix $J_k$, so by Cauchy Interlacing $\lambda_{\max}(A) \ge \lambda_{\max}(J_k) = k$). Every $(k-1)$-colorable graph satisfies $\vartheta(\bar{G}) \le \chi(G) \le k-1$. Therefore $f_{\text{Tardos}, k}$ separates $\mathcal{D}_+$ ($k$-CLIQUE) from $\mathcal{D}_-$ ($(k-1)$-COLORABLE), so **Alon–Boppana's lower bound applies verbatim**:
   $$C_+(f_{\text{Tardos}, k}) \ge \exp\!\left(\Omega\!\left(N^{1/6 - o(1)}\right)\right).$$
3. **Polynomial General Circuits**: Because $\vartheta(\bar{G})$ is a semidefinite program computable to additive error $2^{-\mathrm{poly}(v)}$ in polynomial time (Grötschel–Lovász–Schrijver 1981), $f_{\text{Tardos}, k} \in \text{P} \subseteq \text{P/poly}$!

**Where the Negation / Cancellation Happens**: Look at our explicit feasible matrix certifying $\vartheta(\bar{G}) \le 2$ for every $2$-colorable graph $G$ with coloring $c \in \{+1, -1\}^v$:
$$A = 2I - cc^\top \implies A_{ii} = 1,\quad A_{ij} = +1 \text{ on edges } (c_i \neq c_j),\quad A_{ij} = \mathbf{-1} \text{ on non-edges } (c_i = c_j).$$
The eigenvalues of $A$ are $\{2, \dots, 2, 2 - v\}$, so $\lambda_{\max}(A) = 2$ **solely because negative entries $-1$ on non-edges cancel the positive correlations of the $+1$ edge entries!** Similarly, for $C_5$, setting non-edge entries to $(\sqrt{5}-3)/2 < 0$ yields $\lambda_{\max}(A) = \sqrt{5} \in (2, 3)$ (all verified to $10^{-9}$ via pure-stdlib Jacobi eigensolver in Module 4C).

### 4.2 Perfect Matching, Kirchhoff Cancellation, and Markov–Fischer Negation Collapse
Three additional theorems sharpen the exact boundary of this wall:

1. **Bipartite Perfect Matching (Razborov 1985b vs. Edmonds 1965 / Lovász 1979)**:
   $\mathrm{PM}_n$ has monotone circuit size $n^{\Omega(\log n)}$, yet lies in $\text{P}$ via Edmonds's augmenting paths or Lovász's randomized Tutte determinant (algebraic cancellation over a large field; note that naive $\mathbb{F}_2$ determinant computes parity of matchings and fails on $K_{3,3}$ where $6 \equiv 0 \pmod 2$).
2. **Kirchhoff Matrix-Tree Theorem (1847) & Jerrum–Snir (1982)**:
   In arithmetic circuits, the monotone spanning-tree polynomial $T_{K_n}(x) = \sum_{T \in \mathcal{T}(K_n)} \prod_{e \in T} x_e$ requires $2^{\Omega(n)}$ monotone $\{+, \times\}$ gates, but equals the $(n-1)\times(n-1)$ Laplacian determinant $\det(L^{(n)}(x))$ in $O(n^3)$ general $\{+, -, \times\}$ gates. In Module 4B we symbolically verified on $K_4$ that the positive diagonal product creates $27$ raw monomials (including $+2 x_{01}x_{02}x_{12}$ and squared edges), and subtraction **exact-cancels** all $11$ invalid/cycle terms to leave exactly the $16$ monotone spanning trees (alongside Strassen's $7$-multiplication vs $8$-monotone-multiplication exact $2 \times 2$ cancellation).
3. **Why One Layer / $\lceil \log_2(N+1) \rceil$ `NOT` Gates Shatters Everything (Markov 1958; Fischer 1975)**:
   By Markov–Fischer's inverter construction, *any* general circuit of size $S$ on $N$ inputs can be simulated by a circuit of size $O(S + N^2 \log N)$ containing at most **$\lceil \log_2(N+1) \rceil$ `NOT` gates**! Even on $\mathrm{MAJ}_3$ ($n=3$), Module 4A proves exhaustively that $C_+(\mathrm{MAJ}_3) = 4$ nonlinear gates, while the `XOR` circuit $g_1 = x_1 \oplus x_2$, $g_2 = x_1 \oplus x_3$, $g_3 = g_1 \land g_2$, $\mathrm{MAJ}_3 = x_1 \oplus g_3$ uses **only $1$ `AND` gate**—and **all $3$ internal wires violate monotonicity**, immediately invalidating Razborov's monotone approximator lattice!
4. **Why Berkowitz's Slice-Monotonization Cannot Rescue Razborov (Hamming-Weight Inversion)**:
   On a single Hamming-weight slice $|x| = k$, Berkowitz (1982) showed negations can be replaced monotonically via pseudo-complements $\neg x_i \equiv \mathrm{TH}_k^{N-1}(x_{-i})$. Why doesn't this contradict Tardos (1988)? Because in $k$-CLIQUE vs $(k-1)$-COLORABLE (and $f_{\text{Tardos}}$), **YES-instances have strictly LOWER Hamming weight than maximal NO-instances** (e.g., for $v=6, k=3$: minimal $K_3$ has **$3$ edges**, whereas complete bipartite $K_{3,3}$ has **$9$ edges**)! No Hamming-weight threshold can simulate $\neg x_e$ across inverted weight layers.

---

## 5. Mandatory 4-Barrier Audit (+ Monotone Cancellation Wall)

| Barrier | Reference | Interaction with Monotone / Lifting Route | Status in Baton #007 |
| :--- | :--- | :--- | :--- |
| **1. Relativization** | Baker–Gill–Solovay (1975) | Circuit lower bounds are combinatorial/non-uniform, so monotone proofs do not use relativizing TM diagonalization; however, black-box query lifting alone does not yield a non-relativizing uniform separation of $\text{P}$ vs $\text{NP}$. | Insufficient alone (needs non-monotone engine) |
| **2. Natural Proofs** | Razborov–Rudich (1997) | Monotone proofs *evade* Natural Proofs **only** because monotone functions form an exponentially sparse fraction ($2^{O(\binom{N}{N/2})} / 2^{2^N}$) of all Boolean functions (violating Largeness). Any naive generalization of sunflower/rectangle measures to arbitrary Boolean functions with poly-time constructivity immediately hits Natural Proofs (assuming PRFs in $\text{P/poly}$). | **Latent Blocker** if generalized naively |
| **3. Algebrization** | Aaronson–Wigderson (2009) | Monotone combinatorial methods do not directly invoke arithmetization, whereas **algebraic cancellation** (SDP duality, Tutte/Laplacian determinants) is precisely what defeats monotone barriers from the algorithmic side. | Does not unblock general circuits |
| **4. Locality Barrier** | CHOPRS (STOC 2020) | Does not block monotone lower bounds directly, but blocks naive Hardness Magnification attempts to amplify slightly super-linear general circuit bounds (or bounded-negation bounds) via local oracle reductions. | Blocks naive magnification bridge |
| **5. Non-Monotone Cancellation Wall** | Razborov (1985b); Tardos (1988); Markov–Fischer | Proves an exponential gap ($\exp(\Omega(N^{1/6-o(1)}))$ vs $\mathrm{poly}(N)$) between monotone and general circuits—collapsing with merely $\lceil \log_2(N+1) \rceil$ `NOT` gates. | **ACTIVE PRIMARY BLOCKER** |

---

## 6. Verdict & Actionable Handoff to Next Batons

- **Did Baton #007 resolve P vs NP?** **NO.**
- **What did Baton #007 prove and verify?**
  1. Built and passed `verification/verify_baton_007_monotone_lifting.py` (stdlib-only, exit code 0), verifying exact Erdős–Rado sunflower extraction & Razborov plucking errors ($v=5,6$), the exact `3-CLIQUE vs 2-COLORABLE` KW rectangle cover gap ($10 \to 7$), exact GPW index-gadget lifting on $\mathrm{Tseitin}(K_3) \circ \mathrm{IND}_m^3$ (density $1/(2m^2) \implies D^{\mathrm{cc}} \ge 2\log_2 m + 1$), and all three facets of the Non-Monotone Cancellation Wall (Boolean `MAJ_3`/`MAJ_5` `XOR` cancellation, Kirchhoff $K_4$ Laplacian determinant + Strassen cancellation, and Tardos's Lovász $\vartheta$ SDP separation on $K_3$, all $48$ $2$-colorable graphs for $v=5,6$, and $C_5$).
  2. Formally classified pure monotone lifting / sunflower approximation routes as **`blocked_by_barrier`** for general $\text{P/poly}$ lower bounds.

### Surviving Adjacent Directions for Future Batons
1. **Bounded-Negation Frontier ($t \ll \log N$ `NOT` gates)**: Prove super-polynomial circuit lower bounds for circuits with $t = \omega(1)$ (toward $o(\log N)$) `NOT` gates, tracking exactly where Razborov/GPW invariants fail as $t$ approaches $\lceil \log_2(N+1) \rceil$ (following Guo–Malkin–Oliveira–Santhanam 2015 / Rossman 2015 / Blais et al.).
2. **Non-Monotone Algebraic Lower Bounds (`baton-005-gct-obstructions`)**: Attack algebraic cancellation *directly* over characteristic $0$ (VP vs VNP, Permanent vs Determinant via GCT multiplicity obstructions) rather than forbidding cancellation.
3. **Structure-Preserving Circuit-SAT (`baton-003-direct-tc0-sat`) & Non-Local Meta-Complexity (`baton-004-nonlocal-magnification`)**: Bypass both the Cancellation Wall and Natural Proofs via algorithmic/meta-complexity lower bounds against non-monotone classes ($\text{TC}^0$, $\text{NC}^1$).
