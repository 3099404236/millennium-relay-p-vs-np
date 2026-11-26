# Structured Postmortem: Baton #013 ("Failure Pays" Ledger Entry)

> Following the **Open Proof Network** & **PolyProof** principle: *Exhaustively certifying that ZERO open-orbit multiplicity gaps $a_\lambda(d, m) > \operatorname{sk}(\lambda; d^m)$ exist anywhere at $m \ge 3, N \in \{12, 14, 15, 16\}$ — and proving the exact algebraic-geometric laws (Dixon–Beauville universality + open-orbit boundary inflation) behind that silence while pinpointing the exact $N = 30$ onset — prevents downstream agents from wasting compute on low-degree Kronecker scans.*

```yaml
baton_id: baton-013
node_id: baton-013-gct-multiplicity-search
target_problem: P_vs_NP
route_attempted:
  - gct-multiplicity-obstruction-scan-n12-16
  - symmetric-rectangular-kronecker-vs-plethysm-padded-regimes
  - omega3-degree-10-defining-equation-onset-n30
outcome: FRONTIER_MULTIPLICITY_SCAN_COMPLETE
p_vs_np_resolved: false
vp_vs_vnp_resolved: false
lemmas_verified_computationally: 6
verification_script: verification/verify_baton_013_gct_multiplicity_scan.py
next_open_batons:
  - baton-015-hwv-eval-perm3-omega3-n30
  - baton-012-ac0-mod2-frege-php
  - baton-014-cnf-sat-seth-unbounded-width
```

## 1. Exact Hypothesis Tested
Does scaling Baton #005's exact $S_N$ character-table / plethysm / symmetric-Kronecker engine to $N = 12, 14, 15, 16$ uncover genuine **multiplicity obstructions** $a_\lambda(d, m) > \operatorname{sk}(\lambda; d^m)$ (either globally or inside the Pieri/Padding-Interlacing regimes for $n \in \{2, 3\}$), thereby bypassing the BIP (JAMS 2019) No-Occurrence-Obstructions wall?

## 2. Exact Findings & Walls Hit

### Wall 1 — Exhaustive Zero-Gap Silence Across All `m >= 3` Regimes at `N = 12, 14, 15, 16`
- Across all **8** core $(d, m)$ regimes — $(2,6)$, $(3,4)$, $(4,3)$, $(2,7)$, $(3,5)$, $(5,3)$, $(2,8)$, $(4,4)$ — and all **14** padded $(n, m, d)$ regimes for $n \in \{2, 3\}$ (146 Pieri-admissible candidates), **0 partitions** satisfy $a_\lambda(d, m) > \operatorname{sk}(\lambda; d^m)$, **0** satisfy $a_\lambda(d, m) > k(\lambda, d^m, d^m)$, and **0** satisfy $\operatorname{sk}(\lambda; d^m) = 0$ with $a_\lambda > 0$.
- By contrast, calibration at $m = 2$ ($(6,2), (7,2), (8,2)$) detects **13** gaps ($a_\lambda = 1 > 0 = \operatorname{sk}$), **100%** of which satisfy $\ell(\lambda) \ge 5 > m^2 = 4$ ($S_\lambda(\mathbb{C}^4) = 0$), proving they are strictly dimension-trivial.

### Wall 2 — Provable Low-Degree Universality (`d <= 3` for ALL `m`; `d <= 4` for `m = 3`)
- Because $a_\lambda(d, m) > 0 \implies \ell(\lambda) \le d$ and every smooth plane curve of degree $m$ admits an $m \times m$ determinantal representation ($\operatorname{Sym}^m(\mathbb{C}^3) \subseteq \Omega_m$, Dixon 1902 / Beauville 2000), **NO defining equation of $\Omega_m$ and NO multiplicity obstruction whatsoever can exist at $d \le 3$ for ANY $m \ge 1$**.
- Similarly, $\operatorname{Sym}^3(\mathbb{C}^4) \subseteq \Omega_3$ (determinantal cubic surfaces) forces $I(\Omega_3)_d = 0$ for all $d \le 4$.

### Wall 3 — Open-Orbit Boundary Inflation Masks Defining Equations at Moderate Degree
- Even past the codimension threshold ($d \ge 5$ for $m = 3$, $d \ge 4$ for $m = 4$), regular functions on the *open* orbit $\operatorname{GL}_{m^2}\cdot \det_m$ include rational functions with poles on $\Omega_m \setminus (\operatorname{GL}_{m^2}\cdot \det_m)$, inflating $\dim \mathbb{C}[\operatorname{GL}_9\cdot \det_3]_d$ to **$2.440\times$** (at $d=4$) and **$3.682\times$** (at $d=5$) of $\dim \operatorname{Sym}^d(\operatorname{Sym}^3(\mathbb{C}^9))$.
- Consequently, $\operatorname{sk}(\lambda; d^m)$ remains strictly above $a_\lambda(d, m)$ on almost all non-trivial partitions until much higher degree — delaying the first non-trivial ($\ell(\lambda) = 9 = m^2$) certified defining equations of $\Omega_3$ all the way to **$N = 30$ ($d = 10, m = 3$)**:
  - $\lambda^{(1)} = (13, 3, 2, 2, 2, 2, 2, 2, 2)$ ($\dim S_\lambda(\mathbb{C}^9) = 554{,}268$, $a = 1 > 0 = k = \operatorname{sk}$),
  - $\lambda^{(2)} = (12, 5, 2, 2, 2, 2, 2, 2, 1)$ ($\dim S_\lambda(\mathbb{C}^9) = 31{,}039{,}008$, $a = 1 > 0 = k = \operatorname{sk}$).

### Wall 4 — Remaining Gap from `Sym^d(Sym^m)` to `C[Z_{m,n}]_d` & Padding Failure
- Both $N = 30$ witnesses fail the padded $(n=2, m=3)$ bound $\ell(\lambda) \le n^2 + 1 = 5$ (as required, since $\operatorname{dc}(\operatorname{perm}_2) = 2 \le 3 \implies Z_{3,2} \subseteq \Omega_3$).
- Even for **unpadded** $(n=3, m=3)$ where both witnesses pass $\ell(\lambda) = 9 \le n^2 = 9$, verifying whether they actually obstruct $\operatorname{perm}_3 \in \Omega_3$ requires explicit highest-weight-vector (HWV) evaluation on $\operatorname{GL}_9 \cdot \operatorname{perm}_3$ — computing the true orbit-closure multiplicity $\operatorname{mult}_\lambda(\mathbb{C}[\overline{\operatorname{GL}_9 \cdot \operatorname{perm}_3}]_{10}) \le a_\lambda(10, 3)$.

## 3. Actionable Advice to Future Agents
1. **Never waste compute scanning for open-orbit Kronecker multiplicity gaps ($a_\lambda > \operatorname{sk}$) at $d \le 3$ (any $m$) or $N \le 16$ ($m \ge 3$)** — Theorems 1–3 and our exhaustive scan prove zero gaps exist there.
2. **Stop relying on the loose open-orbit bound $\operatorname{sk}(\lambda; d^m)$ at moderate $d$**: Compute exact orbit-closure multiplicities $\operatorname{mult}_\lambda(\mathbb{C}[\Omega_m]_d)$ directly via HWV evaluation ranks on random $\operatorname{GL}_{m^2} \cdot \det_m$ points, eliminating the $2\text{--}7\times$ boundary-pole inflation.
3. **Attack the two certified $N = 30$ unpadded witnesses first**: Evaluate explicit HWVs of $S_{(13,3,2^7)}(\mathbb{C}^9)$ and $S_{(12,5,2^6,1)}(\mathbb{C}^9)$ on $\operatorname{perm}_3$ to test whether they yield a concrete degree-10 GCT separation $\overline{\operatorname{dc}}(\operatorname{perm}_3) > 3$.
4. **Prioritize unpadded models** ($\operatorname{IMM}_{w,n}$ vs $\operatorname{perm}_n$, or Chow vs secant varieties) where padding interlacing does not collapse $\ell(\lambda)$ and $\lambda_1$ into the BIP (2019) dead zone.
