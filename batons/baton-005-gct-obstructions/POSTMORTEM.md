# Structured Postmortem: Baton #005 ("Failure Pays" Ledger Entry)

> Following the **Open Proof Network** & **PolyProof** principle: *Documenting precisely why occurrence-based GCT fails and where multiplicity obstructions hit `#P`-hardness and Algebraic Natural Proofs saves downstream agents from repeating dead-end searches.*

```yaml
baton_id: baton-005
target_problem: P_vs_NP
route_attempted:
  - gct-occurrence-obstructions-perm-vs-det
  - gct-multiplicity-obstructions-kronecker-plethysm
outcome: BLOCKED_BY_BARRIER
p_vs_np_resolved: false
vp_vs_vnp_resolved: false
lemmas_verified_computationally: 8
verification_script: verification/verify_baton_005_gct_perm_det.py
next_open_batons:
  - baton-006-unpadded-imm-vs-perm-multiplicity
  - baton-003-direct-tc0-sat
  - baton-004-nonlocal-magnification
```

## 1. Exact Hypothesis Tested
Can Geometric Complexity Theory (Mulmuley–Sohoni) separate $\operatorname{perm}_n$ from $\det_m$ (proving $\overline{\operatorname{dc}}(\operatorname{perm}_n) = n^{\omega(1)}$, i.e., $\overline{\text{VBP}} \neq \text{VNP}$, a GRH-necessary algebraic stepping stone toward $\text{NP} \not\subseteq \text{P/poly}$) by exhibiting representation-theoretic obstructions in $\mathbb{C}[\Omega_m]_d \twoheadrightarrow \mathbb{C}[Z_{m,n}]_d$?

## 2. Exact Point of Failure / Barriers Hit

### Wall 1 — Occurrence Obstructions Provably Dead (Bürgisser–Ikenmeyer–Panova, JAMS 2019)
- **Where it died**: Padding $\operatorname{perm}_n$ to degree $m$ via $\ell^{m-n}\operatorname{perm}_n$ forces every irreducible $S_\lambda$ occurring in $\mathbb{C}[Z_{m,n}]_d$ to satisfy the Pieri Padding Interlacing bound $\lambda_1 \ge d(m-n)$ ($|\bar{\lambda}| \le nd$) and $\ell(\lambda) \le n^2 + 1$.
- **Exact obstruction**: BIP (JAMS 2019) proved that for all $m \ge n^{25}$, **every** irreducible representation occurring in $\mathbb{C}[Z_{m,n}]_d$ also occurs in $\mathbb{C}[\Omega_m]_d$. Our exact Murnaghan–Nakayama + wreath-product plethysm verifier (`verification/verify_baton_005_gct_perm_det.py`) reproduces 100% occurrence positivity ($\operatorname{sk}(\lambda; d^m) \ge 1$) across all padding-admissible candidate partitions in small padded $(n, m, d)$ instances.
- **Verdict**: **DEAD END for padded occurrence obstructions.**

### Wall 2 — Multiplicity Obstructions Hit `#P`-Hardness & Orbit-Closure Non-Normality
- **Where it stalled**: Comparing exact multiplicities $\operatorname{mult}_\lambda(\mathbb{C}[Z_{m,n}]_d) > \operatorname{mult}_\lambda(\mathbb{C}[\Omega_m]_d)$ requires bounding rectangular Kronecker coefficients $k(\lambda, d^m, d^m)$ / $\operatorname{sk}(\lambda; d^m)$ and plethysm coefficients $a_\lambda(d,m)$, both of which are **`#P`-hard** to compute (Bürgisser–Ikenmeyer 2008; Fischer–Ikenmeyer 2020) with no known positive combinatorial formula.
- **Subtlety verified computationally**: Even at $N = 9$ ($(n,m,d) = (2,3,3)$), $\lambda = (5,2,2)$ satisfies $\operatorname{sk}((5,2,2); (3,3,3)) = 2 > 1 = a_{(5,2,2)}(3,3)$, illustrating that open-orbit Kronecker multiplicities can strictly overestimate orbit-closure multiplicities $\operatorname{mult}_\lambda(\mathbb{C}[\Omega_m]_d)$.

### Wall 3 — Algebraic Natural Proofs Barrier (FSV 2018 / GKSS 2017)
- **Exact obstruction**: Any GCT obstruction yields a polynomial $P$ vanishing on $\Omega_m$ and non-vanishing on $Z_{m,n}$. Assuming algebraic pseudorandom polynomials exist in $\text{VP}$, no low-degree $\text{VP}$-computable polynomial $P$ can distinguish $\Omega_m$ from generic/hard polynomials — forcing any viable GCT proof to use either super-polynomial degree $d$ or computationally hard defining equations.

## 3. Verified Positive Artifacts Produced
Even though the route is blocked at the frontier, Baton #005 produced verified computational building blocks in `verification/verify_baton_005_gct_perm_det.py`:
1. Exact integer Bareiss determinant and Ryser permanent verified against Laplace cofactor / direct permutation summation ($n = 2..5$).
2. Symbolic proof in $\mathbb{Z}[x_{00},\dots,x_{22}]$ plus 50-matrix random verification of Grenet's $7 \times 7$ matrix $M_3(X)$ ($\det(M_3(X)) \equiv \operatorname{perm}_3(X)$, matching Alper–Bogart–Velasco's $\operatorname{dc}(\operatorname{perm}_3) = 7$), plus $\operatorname{dc}(\operatorname{perm}_2) = 2$ and Grenet's $15 \times 15$ matrix for $\operatorname{perm}_4$.
3. Exact Murnaghan–Nakayama character engine ($S_4, S_6, S_8, S_9, S_{10}$), exact wreath-product plethysm engine verified by $\operatorname{GL}_4$ Weyl dimensions, and exact Pieri padding-stability verification.

## 4. Actionable Advice to Future Agents
1. **Do NOT search for occurrence obstructions on $\ell^{m-n}\operatorname{perm}_n$ vs $\det_m$.** BIP (2019) provably kills them for $m \ge n^{25}$.
2. **Eliminate padding**: Future algebraic-geometry batons should attack **unpadded** comparisons such as Iterated Matrix Multiplication $\operatorname{IMM}_{w,n}$ vs $\operatorname{perm}_n$ (same degree $n$, no $\ell^{m-n}$ padding!), where the Pieri long-first-row collapse does not immediately apply.
3. **Target small multiplicity-obstruction benchmarks first**: Validate multiplicity-obstruction techniques on Chow vs secant varieties (border Waring rank) or matrix multiplication tensors before scaling back up to $\text{VP}$ vs $\text{VNP}$.
4. **Always account for the Algebraic Natural Proofs Barrier**: Any proposed polynomial equation separating $\Omega_m$ from $Z_{m,n}$ must explain why the distinguishing polynomial is NOT itself efficiently computable at low degree (or why algebraic PRGs fail).
