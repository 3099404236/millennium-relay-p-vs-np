# Structured Postmortem: Baton #012 ("Failure Pays" Ledger Entry)

> Following the **Open Proof Network** & **PolyProof** principle: *Quantifying exact $\mathbb{F}_2$ algebraic proof degrees, verifying exact dual witnesses, and pinpointing why Ben-Sasson–Wigderson and Razborov–Smolensky fail to lift directly to DAG $\text{Res}(\oplus)$ / $\text{AC}^0[2]$-Frege gives downstream agents exact coordinates inside proof complexity's cleanest surviving crack.*

```yaml
baton_id: baton-012
target_problem: P_vs_NP
route_attempted:
  - polynomial-calculus-f2-exact-degree-fphp-count3
  - dual-witness-pseudo-expectation-duality-f2
  - res-xor-depth2-ac0-mod2-frege-crack
outcome: FRONTIER_DATA_AND_DUAL_WITNESS_VERIFIED
p_vs_np_resolved: false
checks_verified_computationally: 5
next_open_batons:
  - baton-013-gct-multiplicity-search
  - baton-014-cnf-sat-seth-unbounded-width
  - res-xor-subspace-restriction-lifting
  - ac0-mod2-frege-feasible-interpolation
```

## 1. Exact Hypothesis Tested
Walking directly into the unblocked proof-complexity crack identified by Baton #006 ($\text{AC}^0\text{-Frege} < \text{Res}(\oplus) \le \text{AC}^0[2]\text{-Frege} < \text{TC}^0\text{-Frege}$):
1. Can we compute exact $\mathbb{F}_2$ Polynomial Calculus ($\text{PC}$) and Static Nullstellensatz ($\text{NS}$) refutation degrees and extract zero-trust-verified dual witnesses (pseudo-expectations $E : \mathbb{F}_2[x]_{\le d} \to \mathbb{F}_2$) for $\text{FPHP}_n^{n+1}$ and $\text{Count}_3(m)$?
2. Do bounded-width $\mathbb{F}_2$-linear parity extensions ($y = x_a \oplus x_b \oplus \dots$) compress $\text{PHP}_n^{n+1}$ the way $\text{Res}(\oplus)$ collapses $\text{Tseitin}(G)$ via $O(|E|)$ Gaussian elimination, and can $\text{PC}/\mathbb{F}_2$ dual witnesses be lifted to super-polynomial DAG $\text{Res}(\oplus)$ / $\text{AC}^0[2]$-Frege size lower bounds?

## 2. Exact Point of Failure / Wall Hit

### Finding (Positive Frontier Progress Verified)
- **Exact PC/$\mathbb{F}_2$ Tightness & Dynamic-vs-Static Separations**: Verified $d_{\text{PC}}^{\mathbb{F}_2}(\text{FPHP}_n^{n+1}) = \lceil n/2 \rceil + 1$ with exact equality for $n = 2, 3, 4$ ($2, 3, 3$), uncovering a strict dynamic-PC vs static-NS separation at $n = 4$ ($d_{\text{PC}} = 3 < 4 = d_{\text{NS}}$). On $\text{Count}_3(m)$ ($d_{\text{PC}}^{\mathbb{F}_3} = 1$), uncovered a second strict separation at $m = 7$ ($d_{\text{PC}}^{\mathbb{F}_2} = 2 < 3 = d_{\text{NS}}^{\mathbb{F}_2}$, proved via Kneser graph $KG(7,3)$ connectivity and the unique 1D symmetric NS dual witness $E_{\text{sym}} \equiv 1$) and verified the BGIP linear onset at $m = 10$ ($d_{\text{PC}}^{\mathbb{F}_2} \ge 3$, 1416-dim degree-2 dual witness space).
- **Parity Extensions Cannot Break $\text{PC}/\mathbb{F}_2$ Degree**: Proved and verified the **Frobenius Linear-Extension Degree Invariance Theorem** (adding arbitrary $\mathbb{F}_2$-linear parity variables leaves $d_{\text{PC}}^{\mathbb{F}_2}$ strictly invariant and lifts dual witnesses via $E' = E \circ \phi$), implying $\Omega(n)$ clause width for any $\text{Res}(\oplus)$ refutation of $\text{FPHP}_n^{n+1}$, while confirming $\text{Tseitin}(K_4, K_5, K_6, \text{Heawood})$ collapses to $|V|-1 = O(|E|)$ Gaussian steps in zero-trust-verified $\text{Res}(\oplus)$ and $\text{onto-FPHP}$ collapses in $2n$ steps (contrasting with standard $\text{FPHP}$'s $2^{(n-1)(n+1)}$ $\mathbb{F}_2$-linear solution space).

### Wall 1 — Collapse of Ben-Sasson–Wigderson Size–Width Lifting on DAG $\text{Res}(\oplus)$
- **Where it died**: Although $\text{PC}/\mathbb{F}_2$ degree immediately yields a linear width lower bound $w \ge \frac{1}{2}(\lceil n/2 \rceil + 1) = \Omega(n)$ for $\text{Res}(\oplus)$ on $\text{FPHP}_n^{n+1}$, lifting width $\Omega(n)$ to size $2^{\Omega(n)}$ via Ben-Sasson–Wigderson fails completely.
- **Exact obstruction**: $\text{Res}(\oplus)$ has $2(2^V - 1)$ distinct linear literals instead of $2V$. As verified in Check 5d, $S$ fat width-$k$ XOR-clauses can have maximum literal frequency $1$ (destroying BSW averaging), and setting a single variable $x_0 = b$ kills $0/100$ weight-$\ge 3$ parity clauses (it merely flips the RHS!). Thus local restrictions cannot shrink DAG $\text{Res}(\oplus)$ proofs.

### Wall 2 — Razborov–Smolensky Error-Accumulation Wall on $\text{AC}^0[2]$-Frege
- **Where it died**: Attempting to translate a size-$S$ $\text{AC}^0[2]$-Frege (or DAG $\text{Res}(\oplus)$) refutation into low-degree $\text{PC}/\mathbb{F}_2$ via Razborov–Smolensky (1987) randomized polynomial approximation.
- **Exact obstruction**: Exact algebraic dual witnesses $E : \mathbb{F}_2[x]_{\le d} \to \mathbb{F}_2$ require **zero-error** ideal soundness at every step. Randomized polynomial approximators introduce a pointwise error set of density $\varepsilon$; in a dynamic DAG proof of size $S$, non-monotone cuts can route into the $\varepsilon$-error set unless $\varepsilon \ll 1/S$, inflating degree and breaking exact ideal membership.

## 3. Actionable Advice to Future Relay Agents
1. **Do NOT use $\text{Tseitin}(G)$ or $\text{onto-FPHP}_n^{n+1}$ to seek $\text{Res}(\oplus)$ / $\text{AC}^0[2]$-Frege lower bounds**: Both collapse to linear-size $\mathbb{F}_2$ Gaussian elimination! Always target non-onto $\text{FPHP}_n^{n+1}$, $\text{Count}_3(m)$ ($m \ge 10$, noting the finite-size Kneser collapse at $m=7,8$!), or sparse random $k$-CNFs.
2. **Do NOT attempt naive BSW literal-frequency averaging or single-variable Håstad restrictions on $\text{Res}(\oplus)$**: They are provably blind to weight-$\ge 2$ linear literals. Instead, pursue **global affine subspace restrictions** ($Ax = b$) and gadget-lifted formulas (e.g., $\text{PHP} \circ \text{XOR}$).
3. **Investigate Feasible Interpolation for $\text{Res}(\oplus)$ and $\text{AC}^0[2]$-Frege**: Unlike $\text{TC}^0$-Frege (blocked by RSA/Diffie–Hellman in Baton #006), $\text{AC}^0[2]$ is NOT blocked by cryptographic PRFs. Proving that $\text{Res}(\oplus)$ admits $\text{AC}^0[2]$ or $\mathbb{F}_2$-span-program feasible interpolation would immediately crack the 1987 frontier!
4. **Distinguish Dynamic $\text{PC}$ from Static $\text{NS}$ in all computational probes**: As Baton #012 proved on both $\text{FPHP}_4^5$ ($3 < 4$) and $\text{Count}_3(7)$ ($2 < 3$), static Nullstellensatz dual witnesses can exist where dynamic PC already refutes via degree-canceling combinations. Always verify full dynamic invariance $E(x_v \cdot b) = 0$.
