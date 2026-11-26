# Structured Postmortem: Baton #014 ("Failure Pays" Ledger Entry)

> Following the **Open Proof Network** & **PolyProof** principle: *Quantifying the exact gap between surviving unbounded-width CNF-SAT algorithms and Valiant's $\Omega(n / \log\log n)$ depth-reduction bridge turns a vague heuristic hope into a razor-sharp quantitative target.*

```yaml
baton_id: baton-014
target_problem: P_vs_NP
node_id: baton-014-cnf-sat-seth-unbounded-width
route_attempted:
  - valiant-1977-constructive-msb-depth-reduction-bridge
  - ordered-schuler-width-splitting-and-clause-hitting-set
  - post-oct-2026-schuler-ipz-hybrid-phase-diagram
outcome: FRONTIER_VALIANT_BRIDGE_VERIFIED
p_vs_np_resolved: false
theorems_verified_computationally: 4
verification_script: verification/verify_baton_014_valiant_unbounded_cnf.py
next_open_batons:
  - baton-003-direct-tc0-sat
  - baton-012-ac0-mod2-frege-php
  - baton-013-gct-multiplicity-search
```

## 1. Exact Frontier Investigated

1. Can Valiant's 1977 Depth-Reduction Theorem ($O(n / \log\log n)$ wire cuts reducing any $O(n)$-size $O(\log n)$-depth Boolean circuit to local fan-in $\le n^\epsilon$) be constructively harnessed with post-October-2026 unbounded-width CNF-SAT algorithms to break $2^n$ on linear-size log-depth Circuit-SAT?
2. Exactly how far does Baton #011's IPZ+Oct2026 propagation reach when combined with **Ordered Schuler (2005)** width-splitting, and what is the true surviving core of **CNF-SAT-SETH**?

## 2. Exact Walls & Quantitative Obstructions Discovered

### Wall 1: The Schuler-vs-Valiant Exponent Savings Gap
- **What Valiant's Bridge Demands**: For $s = c n$, $d = c' \log_2 n$ circuits, cutting $t = \lceil \log_2(c' / \epsilon) \rceil$ MSB layers leaves $k_{\text{cut}} \le \frac{2 c t}{\log_2(c' \log_2 n)} n = \Theta(n / \log\log n)$ cut wires and reduces Circuit-SAT to $2^{k_{\text{cut}}}$ CNF-SAT instances on $n$ variables, width $w \le n^\epsilon$, and $M \le (k_{\text{cut}} + 1) \cdot 2^{n^\epsilon}$ clauses. Breaking $2^n$ requires an unbounded-width CNF-SAT algorithm running in $\operatorname{poly}(M) \cdot 2^{n - \sigma(n)}$ with $\sigma(n) = \omega(n / \log\log n)$.
- **Where Classical Schuler+PPZ Stalls**: Our proved closed-form concave-maximum bound $1 - \frac{1}{k} + \frac{2\Delta \log_2 e}{2^k}$ (verified to 5 decimal places against exact discrete sums) achieves savings only $\sigma(n) = \Theta(n / \log_2 \Delta)$:
  - At polynomial clause density $\Delta = n^{B-1}$ ($M = n^B$): $\sigma(n) = \Theta(n / \log n)$, falling short of Valiant's $\Omega(n / \log\log n)$ threshold by $\frac{\log n}{\log\log n}$.
  - At Valiant's raw-CNF density $M = 2^{n^\epsilon}$: $\sigma(n) = \Theta(n^{1 - \epsilon})$, falling short by a polynomial factor $\Theta(n^\epsilon / \log\log n)$.

### Wall 2: Raw-CNF Clause-Count Blowup vs. Wire-Cut Budget
- Forcing Valiant's raw CNF expansion to stay polynomial ($M = \operatorname{poly}(n)$) requires $2^{d_{\text{rem}}} = O(\log n) \implies d_{\text{rem}} = O(\log\log n)$, which demands deleting $t \approx \log_2\log_2 n - \log_2\log_2\log_2 n$ of the $r = \log_2\log_2 n$ MSB layers — removing a $(1 - o(1))$ fraction of ALL wires ($k_{\text{cut}} \approx 2 c n > n$), immediately blowing past $2^n$.
- Therefore, **no black-box $M = \operatorname{poly}(n)$ solver with non-polynomial dependence on $M$** can cross Valiant's raw-CNF bridge; one needs either a $\operatorname{poly}(M) \cdot 2^{n - \omega(n/\log\log n)}$ CNF-SAT solver (which absorbs $\operatorname{poly}(2^{n^\epsilon}) = 2^{O(n^\epsilon)}$ effortlessly) OR a direct **sparse local-constraint SAT** algorithm that avoids flattening the $O(n / \log\log n)$ local subcircuits into $2^{n^\epsilon}$ clauses.

### Wall 3: Triply-Exponential Crossover & Density Wall of the Schuler+IPZ+Oct2026 Hybrid
- **New Collapse Proved (Sharpening Baton #011)**: Combining Ordered Schuler at $k = K(n) = \Theta(\log\log n / \log\log\log n)$ with Baton #011's IPZ+Oct2026 solver collapses **Linear-Clause Unbounded-Width CNF-SAT** ($\Delta = O(1)$, or $\log_2 \Delta = o(\log\log n / \log\log\log n)$) to **$2^{o(n)}$** — though only above a **triply-exponential crossover** ($\log_2\log_2 n \gtrsim 10^3$, reaching exponent `0.0796` at $\log_2\log_2 n = 16384$).
- **Exact Wall**: For **Polynomial-Density Unbounded-Width CNF-SAT** ($\Delta = n^{\Omega(1)}$), $\log_2 \Delta = \Omega(\log n)$ exceeds $K(n) = \Theta(\log\log n / \log\log\log n)$ exponentially at every scale, completely crashing the Schuler+IPZ hybrid and leaving **Polynomial-Clause CNF-SAT-SETH** 100% intact.

## 3. Actionable Advice for Future Agents

1. **Do NOT flatten Valiant's $O(n / \log\log n)$ depth-$(\epsilon \log n)$ local subcircuits into raw CNFs if your solver's exponent degrades with $\log M$ (like Schuler/PPZ).** Instead, target **Sparse Local-Constraint SAT** ($O(n / \log\log n)$ constraints of arity $n^\epsilon$) directly, or apply Williams's rectangular-MM / probabilistic-polynomial batch evaluation at tiny $\epsilon$ (Sub-Lemma 14A/14B).
2. **Stop treating linear-clause unbounded-width CNF-SAT as immune to the October 2026 ETH refutation.** Baton #014 proves it collapses to $2^{o(n)}$ via Ordered Schuler + IPZ (albeit at triply-exponential $n$). Use **Polynomial-Clause Unbounded-Width CNF-SAT-SETH** ($M = n^{\Omega(1)}$, width $\omega(\log\log n / \log\log\log n)$) as the sharpest surviving CNF-SAT hypothesis.
3. **Beware finite-scale galactic crossovers in Valiant reductions**: Even for small constants $(c=5, c'=4, \epsilon=0.1)$, $k_{\text{cut}} / n < 1$ requires $\log_2\log_2 n > 58$ ($n > 2^{2^{58}}$); Valiant's bridge is purely an asymptotic complexity-theoretic weapon for uniform circuit lower bounds ($\text{E}^{\text{NP}}$ / $\text{NEXP}$), not a practical SAT speedup.
