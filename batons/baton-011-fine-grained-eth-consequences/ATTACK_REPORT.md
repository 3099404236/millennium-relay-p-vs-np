# Baton #011: Post-October-2026 ETH Refutation Audit — What Collapses vs. What Survives for `P vs NP`?

- **Target Millennium Problem**: P versus NP (Clay Mathematics Institute — **Unsolved** as of November 2026)
- **Baton ID**: `baton-011`
- **Node ID**: `baton-011-fine-grained-eth-consequences`
- **Dependencies**: `route-1a-blackbox-tseitin-eth`
- **Status**: `VERIFIED` (Did **not** resolve P vs NP; rigorously mapped the post-October-2026 fine-grained complexity fallout, proved and computationally verified the IPZ Sparsification leaf-density & $k$-SAT propagation theorems, quantified the doubly-exponential galactic crossover and unbounded-width breakdown preserving CNF-SAT-SETH, and established the exact exponential survival gap separating ETH refutation from $\text{P} = \text{NP}$ and Natural Proofs PRFs)
- **Date**: 2026-11-26

---

## 1. Executive Question & Scope

Following the **October 2026** Lean-verified refutation of the **Exponential Time Hypothesis (ETH)** — establishing a deterministic $3\text{-SAT}$ algorithm running in sub-exponential time
$$T_{3\text{-SAT}}(n) = \exp\!\left(\frac{n}{(\log n)^{1/2 + o(1)}}\right)$$
— Baton #001 (`route-1a-blackbox-tseitin-eth`) pruned black-box Tseitin reductions to $\text{P/poly}$ via the *Tseitin–ETH Scaling Dichotomy* (peaking at circuit size $s^*(n) = \Theta(n\sqrt{\log n})$).

Baton #011 performs a complete **structural fallout audit** of the October 2026 result across fine-grained complexity, parameterized complexity, cryptography, and the `P vs NP` landscape:

1. **What collapses immediately** (and *why*: separating refuted hypotheses from merely invalidated conditional *proofs*)?
2. **How does the unconditional Impagliazzo–Paturi–Zane (IPZ 2001) Sparsification Lemma invert direction** — shifting from a hardness-transfer tool into an algorithmic speedup propagator from sparse $3\text{-SAT}$ to dense $3\text{-SAT}$ and fixed-width $k\text{-SAT}$ — and where does IPZ break down?
3. **What survives completely unscathed**, and exactly how far is $\exp(n / \sqrt{\log n})$ from $\text{P} = \text{NP}$, Quasi-ETH, Sub-Polynomial ETH, and cryptographic / Natural Proofs barriers?

---

## 2. The Unconditional IPZ Sparsification Engine (Direction Reversal)

A common misconception after ETH's refutation is that the **Impagliazzo–Paturi–Zane (IPZ 2001) Sparsification Lemma** (and its simplification by Calabro–Impagliazzo–Paturi 2006) somehow depended on ETH. In reality, IPZ is an **unconditional combinatorial theorem** about $k\text{-CNF}$ formulas. Pre-October-2026 it was invoked contrapositively to transfer *hardness* (e.g., $\text{SETH} \implies \text{ETH}$). Post-October-2026, it **flips direction** into an unconditional *algorithmic propagator*.

### 2.1 Exact 3-CNF Flower/Sunflower Sparsification Theorem (Verified in Code)

For a subsumption-free, tautology-free $3\text{-CNF}$ formula $\Phi$ on $n$ variables (with unit propagation applied, leaving $n_{\text{act}}$ active variables and clause sets $C_2, C_3$ of widths $2$ and $3$), define three branching thresholds $(b_1, b_2, b_1')$:
- **Rule 1 — $(1, b_1)$-flower in $C_2$**: A literal $\ell$ appears in $b_1$ distinct $2$-clauses $\{\ell, p_1\}, \dots, \{\ell, p_{b_1}\}$.
- **Rule 2 — $(2, b_2)$-flower in $C_3$**: A literal pair $H = \{\ell_1, \ell_2\}$ appears in $b_2$ distinct $3$-clauses $H \cup \{p_1\}, \dots, H \cup \{p_{b_2}\}$.
- **Rule 3 — $(1, b_1')$-sunflower in $C_3$**: A literal $\ell$ whose link graph $G_\ell = (V_\ell, E_\ell)$ (edges $\{u,v\}$ iff $\{\ell, u, v\} \in C_3$) admits a maximal matching of $b_1'$ pairwise-disjoint size-$2$ petals $P_1, \dots, P_{b_1'}$.

For any heart $H$ and petals $P_1, \dots, P_b$, the exact Boolean distributive identity
$$\bigwedge_{j=1}^b (H \lor P_j) \;\equiv\; H \;\lor\; \left(\bigwedge_{j=1}^b P_j\right)$$
splits $\Phi$ into two branches (Branch 1 adds $H$ and subsumes all $H \cup P_j$; Branch 2 replaces each $H \cup P_j$ by $P_j$). Every rule strictly decreases the lexicographic potential $(n_{\text{act}}, |C_3|)$ in both branches, guaranteeing termination and **exact solution-set identity**:
$$\mathrm{Sol}(\Phi) \;=\; \bigcup_{j=1}^t \mathrm{Sol}(\Phi_j).$$

**Theorem 1 (Exact 3-CNF Leaf-Density Bound — Proved & Verified in `verification/verify_baton_011_eth_consequences.py`)**:
At every surviving leaf $\Phi_j$ where Rules 1–3 do not apply:
1. Every literal appears in at most $b_1 - 1$ clauses of $C_2$, so by handshaking:
   $$|C_2(\Phi_j)| \;\le\; (b_1 - 1)\, n_{\text{act}}.$$
2. For every literal $\ell$, its link graph $G_\ell$ has maximum degree $\Delta(G_\ell) \le b_2 - 1$ (no Rule 2 flower) and maximal matching size $|M| \le b_1' - 1$ (no Rule 3 sunflower). Every edge of $G_\ell$ must touch at least one endpoint of $M$, while each edge of $M$ is counted twice when summing $\deg(v)$ over $V(M)$:
   $$|E(G_\ell)| \;\le\; 2|M|\Delta(G_\ell) - |M| \;\le\; (b_1' - 1)(2b_2 - 3).$$
   Summing over all $2n_{\text{act}}$ literals counts each $3$-clause three times, yielding:
   $$|C_3(\Phi_j)| \;\le\; \frac{2}{3}\, n_{\text{act}}\, (b_1' - 1)(2b_2 - 3).$$

For $(b_1, b_2, b_1') = (3, 3, 3)$, every surviving leaf satisfies $|C_2| \le 2 n_{\text{act}}$ and $|C_3| \le 4 n_{\text{act}}$ (at most $6 n_{\text{act}}$ non-unit clauses total), regardless of initial density $M/n$. Our verification script confirms 100% exact solution-set equality $\mathrm{Sol}(\Phi) = \bigcup_j \mathrm{Sol}(\Phi_j)$ across 12 dense SAT and UNSAT $3\text{-CNF}$ instances ($n = 8..10$, density drop averaging $21.6$ clauses/var, $\max |\{\text{leaves}\}|/2^n = 0.0039$).

---

## 3. Quantitative Propagation Theorem & Collapse of SETH

Let $s_k := \inf \{ c > 0 : k\text{-SAT} \in \mathrm{DTIME}(2^{cn}) \}$ and $s_\infty := \lim_{k \to \infty} s_k$. ETH asserts $s_3 > 0$; SETH asserts $s_\infty = 1$.

Suppose sparse $3\text{-SAT}$ on $m$ variables and $O(m)$ clauses is solvable in time
$$T_3(m) = \exp\!\left(\frac{m}{(\log_2 m)^\alpha}\right), \qquad \alpha > 0 \quad (\text{Oct 2026: } \alpha = 1/2).$$
Given an arbitrary dense $k\text{-CNF}$ $\Phi$ on $n$ variables (fixed $k \ge 3$):
1. **IPZ Sparsification** with parameter $\epsilon = \epsilon(n) \in (0, 1/2)$ produces $t \le 2^{\epsilon n}$ formulas $\Phi_1, \dots, \Phi_t$, each having at most $M \le C(k, \epsilon)\, n$ clauses, where $C(k, \epsilon) = (c_0 k / \epsilon)^{\gamma_k}$ ($\gamma_k = \Theta(k)$; e.g. $\gamma_k \le 3k$ in CIP 2006).
2. **Tseitin Clause-Width Splitting** converts each $k$-clause $(\ell_1 \lor \dots \lor \ell_k)$ ($k \ge 4$) into $k - 2$ width-$3$ clauses using $k - 3$ fresh auxiliary variables:
   $$(\ell_1 \lor \ell_2 \lor z_1) \land (\neg z_1 \lor \ell_3 \lor z_2) \land \dots \land (\neg z_{k-3} \lor \ell_{k-1} \lor \ell_k),$$
   yielding $m = n + (k - 3)M \le \big(1 + (k - 3)C(k, \epsilon)\big) n$ variables and $M' = (k - 2)M = O(m)$ clauses.
3. **Balancing the Exponents**: Total runtime satisfies
   $$\frac{\ln T_k(n)}{n} \;\le\; \epsilon \ln 2 \;+\; \frac{1 + \mu_k (c_0 k / \epsilon)^{\gamma_k}}{(\log_2 m)^\alpha} + o(1), \qquad \mu_k = \max(1, k - 3).$$

**Theorem 2 (IPZ-ETH Propagation Law & Galactic Crossover — Proved & Verified)**:
Optimizing $\epsilon^*(n) = \Theta_k\!\left((\log_2 n)^{-\frac{\alpha}{1 + \gamma_k}}\right)$ yields:
1. **Asymptotic Speedup & SETH Collapse**: For every fixed $k \ge 3$, dense $k\text{-SAT}$ is solvable in time
   $$T_k(n) \;=\; \exp\!\left(O_k\!\left(\frac{n}{(\log_2 n)^{\beta_k}}\right)\right), \qquad \beta_k \;=\; \frac{\alpha}{1 + \gamma_k} \;>\; 0.$$
   Hence **$s_k = 0$ for every fixed $k \ge 3$**, and consequently **$s_\infty = \lim_{k \to \infty} s_k = 0 \neq 1$**: **SETH collapses completely.**
2. **Doubly-Exponential Galactic Crossover**: Because $\beta_k = \Theta(\alpha / k)$, beating brute force ($\ln T_k(n) < n \ln 2$) via black-box IPZ requires $(\log_2 n)^\alpha \gg (c_0 k)^{\gamma_k}$, i.e.,
   $$\log_2 n_{\text{cross}}(k) \;=\; \Theta\!\left((c_0 k)^{\gamma_k / \alpha}\right) \;=\; (c_0 k)^{\Theta(k)}.$$
   For $\alpha = 1/2$, $c_0 = 2$, $\gamma_k = 2k$, numerical verification gives $\log_2 n_{\text{cross}} \approx 10^{12.1}$ ($k=3$), $10^{17.5}$ ($k=4$), and $10^{30.2}$ ($k=6$): asymptotically lethal to SETH, yet practically galactic for $k \ge 4$.
3. **Unbounded-Width Breakdown (CNF-SAT-SETH Survival)**: If clause width grows with $n$ beyond
   $$k(n) \;=\; \omega\!\left(\frac{\log\log n}{\log\log\log n}\right),$$
   then $(c_0 k(n))^{\gamma_{k(n)}} \gg (\log_2 n)^\alpha$ and black-box IPZ fails to beat $2^n$ (verified explicitly at $k(n) = \lfloor \log_2 n \rfloor$). Thus **unbounded-width CNF-SAT-SETH is NOT refuted** by black-box IPZ + ETH refutation!

---

## 4. Complete Post-October-2026 Fallout Matrix: Collapses vs. Survives

A rigorous audit must distinguish between **(i) a hypothesis being refuted**, **(ii) a conditional *proof* losing its premise while the target statement stays open**, and **(iii) a hypothesis remaining completely untouched**.

| Hypothesis / Lower Bound | Post-Oct-2026 Status | Exact Mathematical Reason |
| :--- | :--- | :--- |
| **ETH** ($s_3 > 0$) | **COLLAPSES (Refuted)** | Directly refuted by Lean-verified $\exp(n/(\log n)^{1/2+o(1)})$ $3\text{-SAT}$ algorithm. |
| **SETH** ($\lim_{k\to\infty} s_k = 1$) | **COLLAPSES (Refuted)** | Theorem 2: IPZ Sparsification + width splitting forces $s_k = 0$ for every fixed $k \ge 3 \implies s_\infty = 0$. |
| **$2^{\Omega(n)}$ lower bounds for $O(n)$-reducible NP-complete problems** ($k$-SAT, 3-Coloring, Independent Set, Vertex Cover, Dominating Set) | **COLLAPSES (Refuted)** | Linear-size reductions to $3\text{-SAT}$ (plus IPZ) give genuine $\exp(n/(\log n)^{\Theta(1)})$ algorithms. |
| **ETH-based proofs of $n^{\Omega(k)}$ hardness** ($k$-Clique, $k$-Dominating Set) & **$\text{ETH} \implies \text{FPT} \neq \text{W}[1]$** | **PROOF INVALIDATED; TARGET SURVIVES** | Reduction runs $3\text{-SAT} \le k\text{-Clique}$ ($N$ vars $\to n=2^{N/k}$ vertices). Refuting ETH removes the contradiction, but gives **no** $n^{o(k)}$ algorithm for $k$-Clique. $\text{FPT} \neq \text{W}[1]$ remains open. |
| **SETH-based proofs of quadratic hardness** (Low-Dim OVH, Edit Distance, LCS, Fréchet, Graph Diameter) | **SETH-PROOF INVALIDATED; OVH & LOWER BOUNDS SURVIVE** | Williams (2005) reduces $k\text{-SAT} \le \text{OV}$ ($N = 2^{n/2}, d = O(\log N)$). Refuting SETH kills `SETH => LDOVH`, but gives **no** $N^{2-\delta}$ algorithm for OV/Edit Distance/LCS. Moreover, **moderate-dim OVH** ($d = \omega(\log N)$) still follows from surviving **CNF-SAT-SETH**! |
| **Unbounded-Width CNF-SAT-SETH** ($m = \text{poly}(n)$ clauses, arbitrary width) | **SURVIVES (Open)** | Theorem 2(3): IPZ factor $(k/\epsilon)^{\Theta(k)}$ breaks down once $k = \omega(\log\log n / \log\log\log n)$. |
| **Circuit-SAT-SETH** (size $n^{1+\epsilon}$ or even $O(n \log n)$ circuits) | **SURVIVES (Open)** | Baton #001 Tseitin–ETH Dichotomy: black-box Tseitin fails beyond $s^*(n) = \Theta(n\sqrt{\log n})$. |
| **APSP Hypothesis** ($n^{3-o(1)}$) & **3SUM Hypothesis** ($n^{2-o(1)}$) | **SURVIVES (Completely Independent)** | Neither relies on ETH/SETH; unaffected by sub-exponential $3\text{-SAT}$. |
| **Sub-Polynomial ETH ($\text{SP-ETH}(\epsilon)$)**: $3\text{-SAT} \notin \mathrm{DTIME}(2^{n^\epsilon})$ | **SURVIVES (Open)** | Exponentially stronger than ETH; log-runtime gap is $\frac{n^{1-\epsilon}}{\ln 2 \sqrt{\log_2 n}} = \omega(n^{1-\epsilon-o(1)})$. |
| **Quasi-ETH ($\text{QETH}$)**: $3\text{-SAT} \notin \mathrm{DTIME}(2^{\text{polylog } n})$ | **SURVIVES (Open)** | Equivalent to $\text{NP} \not\subseteq \text{QP}$; exponent gap is $\Theta(n / (\log n)^{d+1/2})$. |
| **$\text{P} \neq \text{NP}$ & $\text{NP} \not\subseteq \text{P/poly}$** | **SURVIVES (Completely Open)** | Exponent ratio vs $\mathrm{DTIME}(n^{10})$ exceeds $2^{982}$ at $n = 2^{1000}$. |
| **Cryptographic Primitives (OWFs, PRGs, PRFs, LWE) & Natural Proofs** | **SURVIVES (100% Intact)** | Even $2^{n^{0.5}}$-hard PRFs require breaking time $2^{\sqrt{n}} \ll \exp(n/\sqrt{\log n})$ (at $n=10^6$: $2^{1000}$ vs $2^{323150}$). |

---

## 5. Exact Survival Gap Analysis: Why Refuting ETH Is Exponentially Far from `P = NP`

Compare $\log_2 T(n)$ across the post-October-2026 complexity spectrum (verified in `verification/verify_baton_011_eth_consequences.py`):

| Regime | Runtime $T(n)$ | Exponent $\log_2 T(n)$ | Exponent Ratio $\frac{\log_2 T_{\text{Oct2026}}(n)}{\log_2 T(n)}$ at $n = 2^{1000}$ |
| :--- | :--- | :--- | :--- |
| Brute Force | $2^n$ | $n$ | $2^{-4.45}$ (Oct 2026 saves $\approx 21.9\times$ in exponent) |
| **Oct 2026 ETH Refutation** | $\exp(n / \sqrt{\log_2 n})$ | $\frac{n}{\ln 2 \cdot \sqrt{\log_2 n}}$ | $1$ (baseline) |
| **$\text{SP-ETH}(0.9)$** | $2^{n^{0.9}}$ | $n^{0.9}$ | **$2^{95.5}$** |
| **$\text{SP-ETH}(0.5)$** | $2^{n^{0.5}}$ | $n^{0.5}$ | **$2^{495.5}$** |
| **Quasi-ETH ($\text{QETH}$)** | $2^{(\log_2 n)^3}$ | $(\log_2 n)^3$ | **$2^{965.6}$** |
| **Polynomial ($\text{P}$, $n^{10}$)** | $n^{10}$ | $10 \log_2 n$ | **$2^{982.3}$** |

Two sharp consequences follow immediately:
1. **Distance to $\text{P} = \text{NP}$**: Refuting ETH shaves a $(\log n)^{1/2}$ factor off the *exponent* $n$, leaving $\log_2 T(n) = n^{1 - o(1)}$. Reaching $\text{SP-ETH}(\epsilon)$ requires replacing $n^{1-o(1)}$ with $n^\epsilon$; reaching $\text{QETH}$ requires collapsing it to $(\log n)^{O(1)}$; reaching $\text{P}$ requires $O(\log n)$.
2. **Survival of Razborov–Rudich Natural Proofs**: Natural Proofs only requires PRFs secure against $2^{n^\epsilon}$-size circuits (for some $\epsilon > 0$). At $n = 10^6$, a $2^{n^{0.5}}$-secure PRF withstands $2^{1000}$ time, whereas the October 2026 solver requires $\approx 2^{323{,}150}$ time. Thus **the Natural Proofs barrier is completely undamaged**.

*Note on Williams's Algorithmic Method*: While $\exp(n/\sqrt{\log n})$ beats $2^n$ on circuits of size $o(n\sqrt{\log n})$ via Tseitin (Baton #001), lifting Circuit-SAT speedups into unconditional $\text{NEXP}$ circuit lower bounds via Williams (2011/2014) / Murray–Williams (2018) incurs Easy Witness / PCP simulation overhead (polylogarithmic to polynomial blowup in circuit size). Therefore, one **must not** casually claim unconditional $\text{NEXP} \not\subseteq \text{SIZE}(o(n\sqrt{\log n}))$ without carefully accounting for the PCP/witness overhead inside the target circuit class.

---

## 6. Mandatory 4-Barrier Audit Table

| Barrier | Reference | What It Blocks | Status Under Baton #011 Findings |
| :--- | :--- | :--- | :--- |
| **1. Relativization** | Baker–Gill–Solovay (1975) | Pure diagonalization / oracle-invariant simulations | **Intact.** IPZ Sparsification and Tseitin width splitting are combinatorial formula transformations, not oracle-breaking circuit lower-bound proofs. Any downstream lower bound still requires non-relativizing tools (PCPs / arithmetization). |
| **2. Natural Proofs** | Razborov–Rudich (1997) | Large + Constructive combinatorial circuit properties (assuming $2^{n^\epsilon}$-hard PRFs) | **100% Intact (Verified).** Because $\exp(n/\sqrt{\log n}) \gg 2^{n^\epsilon}$ for every $\epsilon < 1$, sub-exponentially secure PRFs survive completely unbroken; Natural Proofs continues to block combinatorial $\text{P/poly}$ lower bounds. |
| **3. Algebrization** | Aaronson–Wigderson (2009) | Arithmetization / low-degree extensions alone | **Intact.** ETH refutation does not resolve $\text{NP} \not\subseteq \text{P/poly}$ or bypass algebrization; any algebraic extension of ETH-refutation techniques to $\text{TC}^0$/$\text{NC}^1$ must still audit algebrization. |
| **4. Locality Barrier** | CHOPRS (STOC 2020) | Gluing standard lower-bound methods to local Hardness Magnification reductions | **Intact.** Because black-box IPZ + Tseitin cannot push Circuit-SAT past $o(n\sqrt{\log n})$ (nor lower bounds down from $\text{NEXP}$ to $\text{NP}$), the CHOPRS locality barrier for $\text{MKtP}$/$\text{MCSP}$ magnification remains an active wall. |

---

## 7. Verdict & Handoff to Next Batons

- **Did Baton #011 resolve $\text{P}$ vs $\text{NP}$?** **NO.** (`p_vs_np_resolved: false`)
- **Verified Contributions**:
  1. Implemented and exhaustively verified an authentic **IPZ $3\text{-CNF}$ flower/sunflower sparsification branching algorithm** on dense SAT/UNSAT formulas ($n=8..10$), confirming 100% exact solution-set equality and exact leaf-density bounds ($|C_2| \le 2n_{\text{act}}$, $|C_3| \le 4n_{\text{act}}$).
  2. Proved and verified the **IPZ–ETH Propagation Law** ($\beta_k = \frac{\alpha}{1 + \gamma_k} \implies s_k = 0$ for all fixed $k$, collapsing SETH), while uncovering both the **doubly-exponential galactic crossover** $\log_2 n_{\text{cross}}(k) = (c_0 k)^{\Theta(k)}$ and the **unbounded-width breakdown** at $k(n) = \omega(\log\log n / \log\log\log n)$ that preserves **CNF-SAT-SETH**.
  3. Audited every major fine-grained and complexity-theoretic hypothesis, establishing the exact exponential survival gap separating $\exp(n/\sqrt{\log n})$ from $\text{SP-ETH}(\epsilon)$, $\text{QETH}$, $\text{P}$, and Natural Proofs PRFs.

### Concrete Handoffs for Downstream Batons
1. **To `baton-003-direct-tc0-sat` (Structured Circuit-SAT Beyond Tseitin/IPZ)**: Because black-box IPZ breaks down at clause width $k = \omega(\log\log n / \log\log\log n)$ and Tseitin fails beyond size $\Theta(n\sqrt{\log n})$, future algorithmic attacks **must** open the black box and directly exploit circuit structure ($\text{TC}^0$, $\text{AC}^0[m]$, or unbounded-width CNF-SAT) without auxiliary variable blowup.
2. **To `baton-004-nonlocal-magnification`**: Since Natural Proofs and CHOPRS Locality survive completely intact, meta-complexity lower-bound routes must target non-local / non-black-box reductions rather than hoping ETH refutation weakens PRF barriers.
3. **New Replacement-Hypothesis Frontier (Fine-Grained Complexity)**: Rebuild fine-grained hardness foundations cleanly on **surviving hypotheses** — specifically **CNF-SAT-SETH** (unbounded width), **Circuit-SAT-SETH**, **OVH**, **3SUM**, **APSP**, and **$\text{SP-ETH}(\epsilon)$ / $\text{QETH}$** — instead of the refuted ETH/SETH pair.
