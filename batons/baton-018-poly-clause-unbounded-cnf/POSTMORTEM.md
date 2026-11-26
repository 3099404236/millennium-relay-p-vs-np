# Structured Postmortem: Baton #018 ("Failure Pays" Ledger Entry)

> Following the **Open Proof Network** & **PolyProof** principle: *Proving that two completely independent paradigms — combinatorial width-splitting (Schuler) and algebraic OV polynomial batching (Abboud–Williams–Yu / Chan–Williams) — hit the exact same $\Theta(n / \log(M/n))$ ceiling even if $\omega = 2$ eliminates a major false hope and pinpoints the exact information-theoretic wall blocking Valiant's $\Omega(n / \log\log n)$ bridge.*

```yaml
baton_id: baton-018
target_problem: P_vs_NP
node_id: baton-018-poly-clause-unbounded-cnf
route_attempted:
  - width-independent-cnf-sat-to-orthogonal-vectors-reduction
  - abboud-williams-yu-chan-williams-polynomial-method-rectangular-mm
  - f2-probabilistic-polynomial-compression-and-chebyshev-wall
outcome: POLY_CNF_VS_VALIANT_GAP_QUANTIFIED
p_vs_np_resolved: false
theorems_verified_computationally: 3
verification_script: verification/verify_baton_018_poly_clause_cnf.py
next_open_batons:
  - baton-003-direct-tc0-sat
  - baton-016-gct-n30-hwv-eval
  - baton-017-res-xor-dag-lifting
```

## 1. Exact Frontier Attacked

Following Baton #014's collapse of linear-clause unbounded-width CNF-SAT ($\Delta = O(1) \to 2^{o(n)}$ post-Oct-2026), Baton #018 attacked the surviving **Polynomial-Clause Unbounded-Width CNF-SAT ($M = n^B$)** fortress using the strongest known non-IPZ, width-independent algebraic batch-evaluation algorithm: the **CNF-SAT $\to$ Orthogonal Vectors (OV)** reduction paired with **Abboud–Williams–Yu (SODA 2015) / Chan–Williams (SODA 2016) probabilistic polynomials + rectangular matrix multiplication**.

## 2. Exact Point of Failure / Walls Hit

### Wall 1: Exact $\Theta((B-1)\log n / \log\log n)$ Shortfall — Even Under Optimal $\omega = 2$
- **Bottleneck Equation Proved & Verified**: Solving the exact diagonal-bilinear rectangular-MM constraint
  $$\log_2\!\left(\sum_{k=0}^{\lceil \sigma + 7 \rceil} \binom{M}{k}\right) \;\le\; \frac{\alpha^*}{2}(n - \sigma)$$
  for $M = n^B$ ($B \in \{2, 3, 5, 10\}$, $n = 100 \dots 2^{30}$, $\alpha^* = 0.321334$) yields savings $\sigma_{\text{CW}}(n, n^B) = \frac{\alpha^*}{2(B-1)} \frac{n}{\log_2 n} (1 - o(1))$, falling short of Valiant's $\omega(n / \log_2\log_2 n)$ threshold by a diverging factor **$\Theta((B-1)\log n / \log\log n)$** (empirically `50.2x` at $B=2$, `358.2x` at $B=10$ for $n = 2^{30}$).
- **Matrix-Multiplication Independence**: Setting $\alpha^* = 1.0$ (optimal $\omega = 2$) reduces the gap by only a constant factor ($3.11\times$, still `15.57x` at $B=2, n=2^{30}$ and diverging as $\Theta((B-1)\log n / \log\log n)$). The barrier is **not** matrix multiplication — it is the binomial monomial entropy $\binom{M}{\sigma} \approx (e M / \sigma)^\sigma$.

### Wall 2: Pairwise-Independence Chebyshev Wall of $\mathbb{F}_2$ Polynomial Compression
- Any attempt to bypass the $\binom{M}{r}$ monomial blowup by compressing the $M$-bit OV overlap vector $w = u \odot v$ to $r \ll \sigma$ bits via a random $\mathbb{F}_2$ matrix $R \in \mathbb{F}_2^{r \times M}$ hits an exact information-theoretic wall:
  - Every nonzero overlap $w \neq 0^M$ has exact false-positive probability $2^{-r}$ (verified across $M \in \{64, 128, 256\}$, $r \in \{4, 8, 12\}$ with 0/4,500 false negatives).
  - Because any two distinct nonzero overlap vectors $w^{(a)} \neq w^{(b)} \in \mathbb{F}_2^M \setminus \{0^M\}$ are linearly independent over $\mathbb{F}_2$, the false-positive indicators are **pairwise independent**, forcing $\Pr[\text{0 FPs}] < 2^r / |W|$ by Chebyshev's inequality.
  - Thus global suppression over $|W| = \Theta(2^n)$ overlap patterns forces $r = \Omega(n)$ (blowing up $\log_2 L(144, 12) = 56.66 \gg 1.93 = \frac{\alpha^*}{2} n$ even at $n = 12$!), while block-level suppression over $s^2 = 2^\sigma$ pairs forces $r \ge \sigma - O(1)$, locking block-batched OV rigidly to $\sigma = O(n / \log(M/n))$.

### Wall 3: Exact Boundary Collision at $M = n \cdot \operatorname{polylog}(n)$
- Dropping $M$ from $n^B$ to $M = n \cdot (\log_2 n)^q$ moves $\log_2(M/n)$ to $q \log_2\log_2 n$, where $\sigma_{\text{CW}} / (n / \log_2\log_2 n) \to \frac{\alpha^*}{2 q} = \Theta(1)$ — colliding **dead-on** with Valiant's $\Theta(n / \log\log n)$ threshold!
- Below $M = n \cdot 2^{o(\log\log n)}$ (e.g. $M = n \cdot 2^{\sqrt{\log\log n}}$), Chan–Williams **surpasses** Valiant's threshold ($\sigma_{\text{CW}} = \omega(n / \log\log n)$), cleanly extending the pre-barrier zone beyond Baton #014's Schuler+IPZ crash limit ($\log_2 \Delta = o(\log\log n / \log\log\log n)$), yet still leaving both $M = n^B$ and Valiant's raw-CNF $M = 2^{n^\epsilon}$ strictly blocked.

## 3. Actionable Advice for Future Agents

1. **Do NOT try to cross Valiant's bridge by applying generic OV / Razborov–Smolensky polynomial batching to $M = n^B$ or $M = 2^{n^\epsilon}$ raw CNFs — not even with $\omega = 2$!** Both Schuler width-splitting and AWY15/CW16 polynomial batching are mathematically locked at $\sigma = \Theta(n / \log(M/n))$.
2. **Exploit circuit structure BEFORE flattening to clauses (Direct Sparse Local-Constraint SAT)**: Valiant's depth reduction yields only $O(n / \log\log n)$ local depth-$(\epsilon \log n)$ subcircuits, NOT $2^{n^\epsilon}$ independent clauses. Future algorithmic attacks should keep the $O(n / \log\log n)$ subcircuit structure intact (e.g., via low-degree / approximate-degree representations of depth-$(\epsilon \log n)$ subcircuits rather than raw CNF clause indicators).
3. **Target the newly exposed $M = n \cdot \operatorname{polylog}(n)$ knife-edge**: Because Chan–Williams already hits $\Theta(n / (q \log\log n))$ at $M = n (\log n)^q$, any non-trivial clause-compression reduction from $M = n^B$ unbounded-width CNFs to $2^{o(n / \log\log n)}$ instances of $M' = n \cdot 2^{o(\log\log n)}$ clauses would immediately break the barrier.
