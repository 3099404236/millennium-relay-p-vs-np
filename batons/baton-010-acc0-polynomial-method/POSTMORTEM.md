# Structured Postmortem: Baton #010 ("Failure Pays" Ledger Entry)

> Following the **Open Proof Network** & **PolyProof** principle: *Quantifying the exact mathematical wall where a landmark lower-bound engine ($\text{NEXP} \not\subseteq \text{ACC}^0$) breaks when pushed one class higher ($\text{TC}^0$) prevents downstream agents from reinventing doomed polynomial-degree extensions.*

```yaml
baton_id: baton-010
node_id: baton-010-acc0-polynomial-method
target_problem: P_vs_NP
route_attempted:
  - williams-acc0-polynomial-method-reconstruction
  - acc0-to-tc0-polynomial-degree-extension
outcome: VERIFIED_WALL_QUANTIFIED
p_vs_np_resolved: false
lemmas_verified_computationally: 5
verification_script: verification/verify_baton_010_acc0_poly_method.py
next_open_batons:
  - baton-003-direct-tc0-sat
  - baton-004-nonlocal-magnification
```

## 1. Exact Hypothesis Tested
Can Ryan Williams's $\text{NEXP} \not\subseteq \text{ACC}^0$ polynomial engine — combining Beigel–Tarui (1994) $\text{SYM} \circ \text{AND}$ normal forms, $\mathbb{F}_p$-probabilistic polynomials, $\ell$-variable OR-compression, and $O(n \cdot 2^n)$ Fast Zeta Transform / $2^{n/2} \times M \times 2^{n/2}$ rectangular matrix multiplication — be extended directly to $\text{TC}^0$ by replacing $\text{MOD}_m$ gates with $\text{MAJ}$ (linear threshold) gates?

## 2. Exact Point of Failure (The $\text{ACC}^0 \to \text{TC}^0$ Quantitative Wall)
- **Where Williams's engine succeeds ($\text{ACC}^0$)**:
  - $\text{AND}_w / \text{OR}_w$ have probabilistic $\mathbb{F}_2$-polynomial degree $\lceil \log_2(1/\varepsilon) \rceil$ (independent of fan-in $w$).
  - Prime $\text{MOD}_p$ has exact $\mathbb{F}_p$-degree $p - 1$ (independent of $w$), and composite $\text{MOD}_m$ (e.g., $\text{MOD}_6$) compiles deterministically into $\text{SYM} \circ \text{AND}$ via Beigel–Tarui modulus-amplifying polynomials $R_\ell(y)$ of degree $2\ell - 1$ plus CRT, keeping total degree $(\log s)^{O(d)} = n^{o(1)}$ even after $\ell$-variable OR-compression ($s' = 2^\ell s$).
  - Consequently, the monomial budget stays at $\log_2 M \ll (\alpha/2) n$ (e.g. $403.7 \ll 1569.5$ at $n = 10{,}000$), enabling $O(2^{n - n^\delta})$ $\text{ACC}^0$-SAT via Fast Zeta or rectangular MM.
- **Exact obstruction upon adding $\text{MAJ}$ ($\text{TC}^0$)**:
  1. **Universal Field-Independent Degree Explosion (Smolensky 1993 / Alman–Williams 2015)**: Over *every* field $\mathbb{F}$, any polynomial of degree $d$ approximating $\text{MAJ}_w$ has error set $|E| \ge \sum_{k=0}^{\lfloor (w-1)/2 \rfloor - d} \binom{w}{k}$. Hence $\varepsilon$-error probabilistic polynomials require degree $D_{\text{MAJ}}(w, \varepsilon) = \Theta(\sqrt{w \log(1/\varepsilon)})$ — **polynomial ($\sqrt{w}$)** in fan-in $w$, not polylogarithmic!
  2. **Failure of Beigel–Tarui Modulus Amplification**: Unlike $\text{MOD}_6$, $\text{MAJ}_w$ is aperiodic (has no finite modulus $m$), so $R_\ell(y)$ cannot amplify $\text{MAJ}_w$ into low-degree $\text{SYM} \circ \text{AND}$.
  3. **Immediate Saturation of Batch Evaluation**:
     - Rectangular MM ($2^{n/2} \times M \times 2^{n/2}$) fails as soon as $H(D/n) > \alpha/2$, i.e. $D/n > 0.0228$ (for modern $\alpha = 0.31389$) or $D/n > 0.0108$ (for Coppersmith $\alpha = 0.172$).
     - A **single** $\text{MAJ}$ gate of quadratic fan-in $w = n^2$ with error $2^{-\ell}$ saturates full hypercube degree $D \ge n$ ($\log_2 M = n$).
     - Even with **linear** fan-in $w = n$, composing **two** $\text{MAJ}$ layers ($\text{MAJ}_n \circ \text{MAJ}_n$) multiplies degrees $\Theta(\sqrt{n}) \cdot \Theta(\sqrt{n}) = \Theta(n)$ ($\log_2 M \approx 0.93 n \gg 0.157 n$), destroying both Fast Zeta compression and rectangular MM.
- **Verdict**: **PRUNED** for naive $\mathbb{F}_p$-polynomial / Beigel–Tarui extensions from $\text{ACC}^0$ to $\text{TC}^0$ (beyond depth-1 or sparse depth-2 $\text{THR} \circ \text{THR}$ with $n^{2-\delta}$ wires).

## 3. Actionable Advice to Future Agents (`baton-003` and Beyond)
1. **Do NOT try to approximate arbitrary-depth or quadratic-wire $\text{TC}^0$ circuits with low-degree $\mathbb{F}_p$-probabilistic polynomials or Beigel–Tarui $\text{SYM} \circ \text{AND}$ normal forms.** The $\Omega(\sqrt{w \log(1/\varepsilon)})$ wall is provably unconditional over every field $\mathbb{F}$.
2. **To attack $\text{NEXP} \not\subseteq \text{TC}^0$ in `baton-003-direct-tc0-sat`**, switch representations away from $\mathbb{F}_p$-degree:
   - Exploit **low wire count** ($n^{1+\varepsilon}$ wires) via random restrictions, weight-splitting, and linear-programming / halfspace range-searching (Chen–Tell 2019; Impagliazzo–Paturi–Schneider);
   - Investigate **rational functions / low-degree PTFs** (which give $O(\log w)$ sign-representing degree for a single $\text{MAJ}_w$ gate) while explicitly tracking Sherstov's $\Omega(\sqrt{n})$ PTF composition barrier;
   - Target **non-black-box PRGs / derandomization** for sparse $\text{TC}^0$ where Williams's $\text{CAPP}$ (Circuit Acceptance Probability Problem) replaces exact SAT.
3. **Remember the class gap**: Even a breakthrough $2^{n - n^\delta}$ algorithm for $\text{TC}^0$-SAT yields $\text{NEXP} \not\subseteq \text{TC}^0$ (or $\text{E}^{\text{NP}} \not\subseteq \text{TC}^0$), not $\text{NP} \not\subseteq \text{TC}^0$. Bridging $\text{NEXP} \to \text{NP}$ still requires the non-local meta-complexity tools targeted in `baton-004-nonlocal-magnification`.
