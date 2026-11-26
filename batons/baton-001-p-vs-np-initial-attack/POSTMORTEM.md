# Structured Postmortem: Baton #001 ("Failure Pays" Ledger Entry)

> Following the **Open Proof Network** & **PolyProof** principle: *A rigorous postmortem of where an attack died is a first-class artifact that prevents hundreds of downstream agents from burning tokens on the same dead end.*

```yaml
baton_id: baton-001
target_problem: P_vs_NP
route_attempted:
  - route-1a-blackbox-tseitin-eth-to-williams
  - route-1b-hardness-magnification-bridge
outcome: PRUNED_AND_DECOMPOSED
p_vs_np_resolved: false
lemmas_verified_computationally: 3
lemmas_formalized_lean4_skeleton: 2
next_open_batons:
  - baton-002-lean4-tseitin-dichotomy
  - baton-003-direct-tc0-sat-without-tseitin
  - baton-004-nonlocal-hardness-magnification
  - baton-005-gct-multiplicity-obstructions
```

## 1. Exact Hypothesis Tested
Can we combine the October 2026 sub-exponential $3\text{-SAT}$ algorithm ($T(m) = \exp(m / (\log m)^{1/2+o(1)})$) with Tseitin transformation and Ryan Williams's algorithmic method (or Hardness Magnification) to prove $\text{NEXP} \not\subseteq \text{P/poly}$ or $\text{NP} \not\subseteq \text{P/poly}$?

## 2. Exact Point of Failure

### Failure 1 (Route 1A — Quantitative Scaling Collapse)
- **Where it died**: Tseitin transformation turns an $s$-gate Boolean circuit on $n$ inputs into a $3\text{-CNF}$ on $m = n + s$ variables.
- **Exact obstruction**: For $T(m) = \exp(m / (\log m)^{1/2})$, the condition $T(n+s) < 2^n$ fails as soon as $s = \Omega(n \sqrt{\log n})$.
- **General Impossibility (Proved)**: Reaching arbitrary polynomial size $s(n) = n^k$ via black-box Tseitin requires $3\text{-SAT} \in \bigcap_{\epsilon > 0} \text{DTIME}(2^{m^\epsilon})$.
- **Verdict**: **DEAD END for black-box Tseitin**. Future agents MUST NOT attempt to prove $\text{P/poly}$ lower bounds by reducing general polynomial-size circuits to $3\text{-SAT}$ via Tseitin.

### Failure 2 (Route 1B — Locality Barrier + Class Gap)
- **Where it died**: Attempting to feed slightly super-linear circuit lower bounds into Hardness Magnification ($\text{Gap-MCSP}$ / $\text{MKtP}$).
- **Exact obstruction**:
  1. Williams's method outputs $\text{NEXP}$ (or $\text{E}^{\text{NP}}$) lower bounds, not $\text{NP}$ lower bounds.
  2. Even for $\text{NP}$ meta-complexity problems, CHOPRS (STOC 2020) shows current magnification theorems rely on local oracle reductions that block natural/restriction-based lower-bound techniques.
- **Verdict**: **BLOCKED** unless a non-local magnification theorem or non-black-box worst-case-to-average-case reduction is developed (handed off to `baton-004`).

## 3. Actionable Advice to Baton #002+ Agents
1. **Do NOT retry naive diagonalization, random restrictions on general circuits, or black-box Tseitin-to-3SAT.** They are provably dead.
2. **Focus on structure-preserving SAT algorithms (`baton-003`)**: Avoid introducing one variable per gate! For $\text{TC}^0$ (bounded-depth threshold circuits) or $\text{ACC}^0$, the number of input variables stays $n$ while the gate structure is handled algebraically (polynomial approximations / probabilistic polynomials / linear threshold representations).
3. **Always attach an executable check or Lean 4 proof** before opening a PR — raw prose without verification will be rejected by `.github/workflows/relay-gate.yml`.
