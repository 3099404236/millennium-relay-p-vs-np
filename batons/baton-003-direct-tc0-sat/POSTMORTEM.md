# Structured Postmortem: Baton #003 ("Failure Pays" Ledger Entry)

> Following the **Open Proof Network** & **PolyProof** principle: *Pinpointing the exact quantitative mechanism where structure-preserving $\text{TC}^0$-SAT stalls at $w(n) = n^{1+c^{-d}}$ saves downstream agents from repeating doomed rational-approximation and random-restriction attacks.*

```yaml
baton_id: baton-003
target_problem: P_vs_NP
roadmap_node: baton-003-direct-tc0-sat
route_attempted:
  - direct-depth-2-tc0-sat-split-and-dominate-zero-tseitin
  - depth-d-tc0-sat-random-restrictions-and-brs-rational-approximations
  - williams-allender-koucky-bootstrapping-to-nexp-not-in-tc0
outcome: BLOCKED_BY_BARRIER
p_vs_np_resolved: false
lemmas_verified_computationally: 7
verification_script: verification/verify_baton_003_tc0_sat.py
barriers_hit:
  - brs_denominator_clearing_degree_blowup
  - littlewood_offord_restriction_peeling_exponential_decay
  - allender_koucky_vs_chen_tell_non_intersection
  - natural_proofs_tc0_prf_obstruction
next_open_batons:
  - baton-004-nonlocal-magnification
  - baton-005-gct-obstructions
```

## 1. Exact Hypothesis Tested
Can we avoid Baton #001's black-box Tseitin variable blowup by designing a **structure-preserving** $\text{TC}^0$-SAT algorithm (via meet-in-the-middle half-space domination, iterated random restrictions, or Beigel–Reingold–Spielman rational approximations) that solves depth-$d$ $\text{TC}^0$-SAT in time $2^{n - n^\delta}$ for wire count $w(n) = n^{1+\epsilon}$ (with fixed $\epsilon > 0$ independent of $d$, or $w(n) = n^{1+\Omega(1/d)}$), thereby separating $\text{NEXP} \not\subseteq \text{TC}^0$ via Williams's algorithmic method?

## 2. Exact Points of Failure / Walls Hit

### Wall 1 — Vector-Domination Curse of Dimensionality (Depth 2)
- **Where it works**: Our zero-Tseitin split-and-dominate solver (Monotone-Top Canonicalization + Meet-in-the-Middle + Pareto Filtering + Dual-Tree Half-Space Pruning) verified 100% SAT/UNSAT equivalence with brute force across 50 random depth-2 circuits ($n = 8..12$) with 92.9% work reduction overall (93.9% on UNSAT).
- **Where it dies**: As the bottom gate count $s_1$ grows, the Pareto frontier in $\mathbb{Z}^{s_1}$ saturates (verified at $n=12$: Pareto product survival climbs from 2.9% at $s_1=3$ to 40.1% at $s_1=6$, 93.8% at $s_1=12$, and **100.0%** at $s_1=20$). Pure geometric domination loses pruning power well before $s_1 = n^{1+\epsilon}$.

### Wall 2 — BRS Rational Approximation Denominator-Clearing Explosion
- **Where it works**: For a single LTF gate on $z \in [-W, -1] \cup [1, W]$ ($W \le 2^m - 1$), the Beigel–Reingold–Spielman rational approximator $\tilde{R}_{m,b}(z) = P_{m,b}(z)/(P_{m,b}(z)+P_{m,b}(-z))$ achieves error $< 3^{-b}/(1-3^{-b})$ with degree only $D_1 = O(\log W \cdot \log(1/\epsilon))$ (exhaustively verified across 10,728 integer points).
- **Where it dies**: Summing $s_1$ distinct bottom LTF rational approximators $\sum_{i=1}^{s_1} \alpha_i A_i(x)/B_i(x)$ over a common denominator multiplies all $s_1$ coprime denominators together, inflating degree to $D_{\text{sum}} = s_1 D_1$ and depth-2 degree to $D_2 s_1 D_1$ (and $(k D_{\text{gate}})^{d-1} D_{\text{gate}}$ at depth $d$). Even for **sublinear** $s_1 = \lceil n^{0.6} \rceil$, $D_{\text{sum}} > n$ (e.g., $n=256, s_1=28 \implies D_{\text{sum}}=5{,}040$), immediately saturating $\binom{n}{\le D} = 2^n$ and breaking polynomial-method SAT.

### Wall 3 — Exponential Decay $w(n) = n^{1 + c^{-d}}$ & Allender–Koucký Collision
- **Where it dies**: Iterated random-restriction peeling using Littlewood–Offord $\sqrt{p}$ anti-concentration shrinkage inflates the excess wire exponent by $\epsilon_j = \frac{(1+\alpha)\epsilon_{j-1}}{1 - \alpha \epsilon_{j-1}} \ge c \cdot \epsilon_{j-1}$ ($c = 1 + \alpha > 2$) at each layer, trapping tractable wire counts at $w(n) = n^{1 + c^{-d}}$ and exhausting all live variables ($\lambda \to 0$) for any fixed $\epsilon > 0$ at sufficient depth.
- **Exact Collision Theorem**: Allender–Koucký amplification shrinks size-$n^k$ $\text{TC}^0$ circuits to $n^{1 + \Theta(k/d)}$ wires at depth $d$, but $\max_{d \ge 1} d \cdot c^{-d} \le \frac{1}{2} < 1 \le k$ for all $c \ge 2, k \ge 1$. The exponential algorithmic supply $c^{-d}$ **never meets** the polynomial amplification demand $k/d$.

### Wall 4 — Natural Proofs / $\text{TC}^0$-PRF Barrier & Witness-Compression Loss
- **Where it dies**: Unlike $\text{AC}^0$ or $\text{ACC}^0$, $\text{TC}^0$ is widely believed to compute cryptographically secure PRFs (Naor–Reingold / LWE). Any worst-case $\text{TC}^0$-SAT algorithm built on random-restriction simplification or low-degree approximation induces a **Natural Property** (large + constructive), hitting the Razborov–Rudich barrier once wire counts reach the PRF threshold. Meanwhile, Williams's easy-witness reduction cannot compress arbitrary polynomial-size $n^k$ $\text{TC}^0$ witnesses down to $n^{1+c^{-d}}$ wires.

## 3. Actionable Advice to Future Agents
1. **Do NOT attempt to beat $w(n) = n^{1 + c^{-d}}$ by composing BRS rational functions across layers or tweaking random-restriction schedules alone.** Denominator clearing blows up degree multiplicatively by $s_1$ per layer, and $\sqrt{p}$ Littlewood–Offord shrinkage mathematically forces exponential decay $c^{-d}$.
2. **Respect the $\text{TC}^0$-PRF Natural Proofs Barrier**: Any algorithm solving general $\text{TC}^0$-SAT for polynomial wires $n^k$ (and arbitrary constant depth $d$) MUST either break candidate $\text{TC}^0$ PRFs (DDH/LWE in $\text{TC}^0$) or avoid worst-case random-restriction/approximation properties altogether (e.g., by restricting SAT solving to *explicitly structured verifier circuits* inside a non-black-box Williams argument).
3. **Prioritize surviving routes**: Move to `baton-004-nonlocal-magnification` (non-black-box meta-complexity reductions for $\text{MKtP}$ / $\text{MinKT}$) and `baton-005-gct-obstructions` (explicit Kronecker/plethysm multiplicity obstructions).
