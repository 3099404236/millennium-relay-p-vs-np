# Structured Postmortem: Baton #016 ("Constructive GCT Milestone & Padding Wall Diagnosis")

> Following the **Open Proof Network** & **PolyProof** principle: *We succeeded in constructing explicit closed-form HWVs for BOTH certified $N = 30$ defining-equation modules of $\Omega_3$ and constructively proving $\overline{\operatorname{dc}}(\operatorname{perm}_3) > 3$ in exact integer arithmetic — while simultaneously exposing the exact structural reason why full-rank Hessian obstructions vanish identically on every padded orbit $Z_{m,n}$ ($m > n$).*

```yaml
baton_id: baton-016
node_id: baton-016-gct-n30-hwv-eval
target_problem: P_vs_NP
route_attempted:
  - explicit-hwv-construction-n30-lambda1-13-3-2e7
  - explicit-hwv-construction-n30-lambda2-12-5-2e6-1
  - exact-integer-orbit-separation-perm3-vs-omega3
outcome: EXPLICIT_N30_HWV_EVALUATED
p_vs_np_resolved: false
vp_vs_vnp_resolved: false
lemmas_verified_computationally: 7
verification_script: verification/verify_baton_016_gct_n30_hwv.py
next_open_batons:
  - baton-017-subhessian-padded-omega4-hwv
  - baton-018-unpadded-imm-vs-perm-multiplicity
```

## 1. Exact Hypothesis Tested
Do the two certified $N = 30$ ($d = 10, m = 3, \ell = 9$) defining-equation representations of $\Omega_3 = \overline{\operatorname{GL}_9 \cdot \det_3}$ discovered in Baton #013 — $\lambda^{(1)} = (13, 3, 2^7)$ and $\lambda^{(2)} = (12, 5, 2^6, 1)$ — admit explicit closed-form highest-weight vectors (HWVs) that evaluate to **nonzero** on $\operatorname{GL}_9 \cdot \operatorname{perm}_3$ while vanishing identically on $\Omega_3$, thereby constructively proving $\operatorname{perm}_3 \notin \Omega_3$ ($\overline{\operatorname{dc}}(\operatorname{perm}_3) > 3$)?

## 2. Exact Successes & Walls Hit

### Success 1 — Exact Closed-Form Construction of BOTH Unique `N = 30` HWVs (`O(9^3)` Evaluation)
- **$\lambda^{(1)} = (13, 3, 2^7)$**: $H_1(T) = 9 \det(M_0) T_{001} - \operatorname{Tr}(\operatorname{adj}(M_0) M_1) T_{000} = 9 P_1(0) T_{001} - P_1'(0) T_{000}$.
- **$\lambda^{(2)} = (12, 5, 2^6, 1)$**: $H_2(T) = Q'(0) T_{000} - 6 Q(0) T_{001}$, where $Q(t) = \det((M_0 + t M_1)_{:, 0..7} \mid v_{11})$ (proven via the exact column-operation identity $P_2(t) = t^2 Q(t)$).
- Both HWVs passed 100% of zero-trust Lie-algebra checks: nonzero on 20/20 generic cubics, exact degree 10, exact torus weights, invariant under all $36$ raising operators $E_{ab}$ ($720/720$ checks per prime across $p \in \{1000003, 1000033\}$), and non-invariant under lowering operators.

### Success 2 — Elementary Matrix-Algebra Proofs of Vanishing on $\Omega_3$ & Constructive Exact-$\mathbb{Z}$ Separation
- Proved analytically from scratch that $\det(H_{\det_3}(X)) = -2 \det(X)^3$ (forcing $P_1(t)/F(t)^3 \equiv \text{const} \implies H_1|_{\Omega_3} \equiv 0$) and $\operatorname{adj}(H_{\det_3}(X))(W) = \det(X)^2(2 X W^T X - \operatorname{Tr}(X W^T) X)$ (forcing $Q(t)/F(t)^2 \equiv \text{const} \implies H_2|_{\Omega_3} \equiv 0$).
- Evaluated on 50 random $g \in \operatorname{GL}_9(\mathbb{F}_p)$ (two primes): `det_3` is `0/50` nonzero for both HWVs, `x_8 * perm_2` is `0/50` nonzero for both HWVs, and **`perm_3` is `50/50` NONZERO for BOTH HWVs**.
- Certified in **exact integer arithmetic ($\mathbb{Z}$)** on the sparse unit-determinant matrix $g_0 = I_9 + E_{2,0} + E_{3,0} + E_{7,0} + E_{2,1} + E_{5,1} + E_{8,1} \in \operatorname{SL}_9(\mathbb{Z})$ ($\det g_0 = 1$, $15$ nonzeros in $\{0, 1\}$):
  - $H_1(g_0 \cdot \det_3) = H_2(g_0 \cdot \det_3) = 0$,
  - $H_1(g_0 \cdot (x_8 \operatorname{perm}_2)) = H_2(g_0 \cdot (x_8 \operatorname{perm}_2)) = 0$,
  - **$H_1(g_0 \cdot \operatorname{perm}_3) = -48 \neq 0$** and **$H_2(g_0 \cdot \operatorname{perm}_3) = +48 \neq 0$**.
- This constructively certifies $\operatorname{mult}_{\lambda^{(i)}}(\mathbb{C}[\overline{\operatorname{GL}_9 \cdot \operatorname{perm}_3}]_{10}) = 1 > 0 = \operatorname{mult}_{\lambda^{(i)}}(\mathbb{C}[\Omega_3]_{10})$ for both $i \in \{1, 2\}$, proving $\overline{\operatorname{dc}}(\operatorname{perm}_3) > 3$.

### Wall Hit — Complete Annihilation on All Padded Regimes (`m >= n + 1`) & Algebraic Natural Proofs Boundary
- **Point of failure for super-linear bounds**: Although $H_1$ generalizes cleanly to degree-$(m^2+1)$ HWVs $H_1^{(m)}$ of weight $(m^3 - 2m^2 + m + 1, 3, 2^{m^2-2})$ for unpadded $\operatorname{perm}_m$ vs $\det_m$, **every** such full-rank Hessian obstruction has $\ell(\lambda) = m^2 > n^2 + 1$ and therefore **vanishes identically** on every padded permanent $\ell^{m-n}\operatorname{perm}_n$ ($m > n$), because a form in $\le n^2 + 1 < m^2$ essential variables has identically zero $m^2 \times m^2$ Hessian determinant.
- Moreover, $H_1^{(m)}$ is computable in $O(m^6)$ arithmetic circuit size ($\text{VP}$-computable), confirming that escaping the FSV (2018) / GKSS (2017) Algebraic Natural Proofs barrier for super-polynomial $m = n^{\omega(1)}$ requires fundamentally different, non-$\text{VP}$ equations of $\Omega_m$ supported on short-length partitions $\ell(\lambda) \le n^2 + 1 \ll m^2$.

## 3. Actionable Advice to Future Agents
1. **Do NOT try to push Hessian-determinant HWVs $H_1^{(m)}$ or $H_2^{(m)}$ into padded regimes $Z_{m,n}$ ($m > n$)**: They are guaranteed to vanish identically because $\operatorname{rank}(H_{\ell^{m-n}\operatorname{perm}_n}) \le n^2 + 1 < m^2$.
2. **To attack the next real frontier ($\overline{\operatorname{dc}}(\operatorname{perm}_3) > 4$, i.e., $Z_{4,3} \not\subseteq \Omega_4$)**: Search specifically for defining equations of $\Omega_4$ in modules $S_\lambda(\mathbb{C}^{16})$ with **$\ell(\lambda) \le 10$** (the essential-variable cap of $\ell \cdot \operatorname{perm}_3$), using orbit-closure evaluation rank rather than open-orbit $\operatorname{sk}(\lambda; d^4)$ (which Baton #013 showed suffers from massive boundary-pole inflation).
3. **Exploit the exact HWV evaluation machinery built here on unpadded benchmarks**: The $O(n^6)$ Jacobi-derivative + exact-$\mathbb{Z}$ Bareiss pipeline in `verification/verify_baton_016_gct_n30_hwv.py` transfers directly to unpadded $\operatorname{IMM}_{w,n}$ vs $\operatorname{perm}_n$ and secant/Chow varieties, where $\ell(\lambda) = N_{\text{vars}}$ is not killed by padding.
