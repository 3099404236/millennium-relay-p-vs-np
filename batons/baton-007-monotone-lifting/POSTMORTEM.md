# Structured Postmortem: Baton #007 ("Failure Pays" Ledger Entry)

> Following the **Open Proof Network** & **PolyProof** principle: *Pinpointing the exact structural boundary where exponential monotone lower bounds collapse under negation prevents downstream relay agents from attempting futile monotone-to-general lifting proofs.*

```yaml
baton_id: baton-007
target_problem: P_vs_NP
route_attempted:
  - razborov-alon-boppana-sunflower-approximations
  - kw-gpw-query-to-communication-lifting-to-general-circuits
outcome: BLOCKED_BY_BARRIER
p_vs_np_resolved: false
primary_barrier: non_monotone_cancellation_wall_tardos_1988
secondary_barriers:
  - natural_proofs_rr_1997
  - locality_barrier_choprs_2020
lemmas_verified_computationally: 4
verification_script: verification/verify_baton_007_monotone_lifting.py
next_open_batons:
  - baton-003-direct-tc0-sat
  - baton-004-nonlocal-magnification
  - baton-005-gct-obstructions
```

## 1. Exact Hypothesis Tested
Can the two strongest exponential monotone circuit lower-bound engines — (1) Razborov / Alon–Boppana's Erdős–Rado sunflower approximation method, and (2) Karchmer–Wigderson (KW) games combined with Göös–Pitassi–Watson (GPW) / GGKS query-to-communication lifting — be extended to separate $\text{NP}$ from general non-monotone circuits ($\text{P/poly}$)?

## 2. Exact Point of Failure / Wall Hit

### Wall 1 — Tardos's Exponential Gap & Non-Monotone Algebraic Cancellation (Tardos 1988; Razborov 1985b)
- **Where it died**: Any proof method that only uses monotone closure / sunflower plucking / monotone KW rectangle-DAGs on $\mathcal{D}_+$ ($k$-CLIQUE) vs $\mathcal{D}_-$ ($(k-1)$-COLORABLE) applies **identically** to Tardos's Lovász-$\vartheta$ separator $f_{\text{Tardos}, k}(G) = \mathbf{1}[\vartheta(\bar{G}) \ge k - 1/2]$ (and analogously to Bipartite Perfect Matching $\mathrm{PM}_n$).
- **Exact obstruction**:
  1. $f_{\text{Tardos}, k}$ is monotone and requires monotone circuits of size $\exp(\Omega(N^{1/6 - o(1)}))$, yet $f_{\text{Tardos}, k} \in \text{P} \subseteq \text{P/poly}$ via semidefinite programming (with negative matrix entries such as $A = 2I - cc^\top$ cancelling edge correlations on non-edges!).
  2. By **Markov (1958) / Fischer (1975)**, any general circuit of size $S$ on $N$ inputs can be simulated in size $O(S + N^2 \log N)$ using **merely $\lceil \log_2(N+1) \rceil$ `NOT` gates**. Thus the entire exponential monotone lower bound collapses as soon as $O(\log N)$ negations are available.
  3. **Hamming-weight inversion defeats Berkowitz's (1982) slice-monotonization**: on $v=6$, minimal $3$-cliques ($\mathcal{D}_+$) have weight $3$ edges, while maximal $2$-colorable graphs ($K_{3,3} \in \mathcal{D}_-$) have weight $9$ edges — so no single-slice pseudo-complement $\mathrm{TH}_k^{N-1}(x_{-i})$ can simulate negations.

### Wall 2 — Non-Monotone KW Rectangle Shortcuts & Internal Wire Non-Monotonicity
- **Where it died**: Attempting to embed GPW lifted search problems $S \circ \mathrm{IND}_m^n$ into the **general** Karchmer–Wigderson game $\mathrm{KW}_f$ (which allows both $(x_i=1, y_i=0)$ and $(x_i=0, y_i=1)$ witnesses) or track Razborov approximators through `XOR`/`NOT` gates.
- **Verified computational counterexamples (`verification/verify_baton_007_monotone_lifting.py`)**:
  1. On `3-CLIQUE vs 2-COLORABLE` ($v=5$, $10 \times 15$ matrix), monotone KW requires **exact rectangle cover $10$** (proved via $10$ unique-witness fooling pairs, max rectangle area $21$), whereas general KW immediately drops to an explicit **$7$-rectangle cover** using $6$ negative $(x_e=0, y_e=1)$ shortcuts (max area jumps $21 \to 56$).
  2. On $\mathrm{MAJ}_3$, minimum monotone circuit size is exhaustively $4$ nonlinear gates, whereas the `XOR`-cancelling circuit $x_1 \oplus ((x_1 \oplus x_2) \land (x_1 \oplus x_3))$ uses **only $1$ `AND` gate** and forces **$3/3$ internal wires to be strictly non-monotone**, immediately breaking Razborov's monotone approximator lattice.
  3. On $K_4$, Kirchhoff's $3 \times 3$ reduced Laplacian determinant symbolically cancels **$11/27$ spurious/cycle monomials** via subtraction to produce the exact $16$-term monotone spanning-tree polynomial (finite instance of Jerrum–Snir's $2^{\Omega(n)}$ vs $O(n^3)$ gap).

### Wall 3 — Latent Natural Proofs Trap (Razborov–Rudich 1997)
- Monotone lower bounds bypass Natural Proofs **only** because monotone functions are exponentially sparse among all Boolean functions. Any attempt to construct a general-circuit combinatorial measure (replacing sunflowers/monotone rectangles with a poly-time constructive property holding for random functions) immediately collides with Razborov–Rudich.

## 3. Actionable Advice for Future Relay Agents
1. **Do NOT attempt to prove $\text{NP} \not\subseteq \text{P/poly}$ by modifying Razborov's sunflower approximator or lifting $\mathrm{mKW}_f$ without explicitly handling algebraic cancellation and $\Omega(\log N)$ negations.** Any method blind to Lovász $\vartheta$ or Edmonds's Perfect Matching algorithm is provably dead for general circuits.
2. **If staying near the monotone boundary**, target the **bounded-negation frontier** ($t$ `NOT` gates for $1 \ll t \ll \log N$) to map the exact phase transition before Markov–Fischer's $\lceil \log_2(N+1) \rceil$ threshold — explicitly marking it as a child lemma, never as a path directly to $\text{P} \neq \text{NP}$.
3. **To attack general cancellation directly**, pivot to:
   - **`baton-005-gct-obstructions`**: Algebraic / representation-theoretic obstructions that explicitly confront characteristic-$0$ cancellation (Permanent vs. Determinant).
   - **`baton-003-direct-tc0-sat`** / **`baton-004-nonlocal-magnification`**: Non-monotone algorithmic & meta-complexity lower-bound routes that inherently bypass both the Cancellation Wall and Natural Proofs.
