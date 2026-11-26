# Structured Postmortem: Baton #009 ("Failure Pays" & Barrier Audit Ledger Entry)

> Following the **Open Proof Network** & **PolyProof** principle: *Formalizing and executing exact proof barriers prevents downstream agents from reinventing arithmetization arguments that are provably blocked by Aaronson–Wigderson (2009).*

```yaml
baton_id: baton-009
target_problem: P_vs_NP
route_attempted:
  - algebrization-barrier-audit
  - executable-mle-sumcheck-and-algebraic-oracle-verification
outcome: VERIFIED_BARRIER_AUDIT
p_vs_np_resolved: false
lemmas_verified_computationally: 5
next_open_batons:
  - baton-003-direct-tc0-sat
  - baton-004-nonlocal-magnification
  - baton-005-gct-obstructions
```

## 1. Exact Scope & Question Audited
Can **arithmetization**—lifting Boolean computations and oracles $A : \{0,1\}^m \to \{0,1\}$ to low-degree / multilinear polynomial extensions $\tilde{A} : \mathbb{F}_q^m \to \mathbb{F}_q$ and applying interactive Sumcheck / PCP protocols—separate $\text{P}$ from $\text{NP}$, $\text{NP}$ from $\text{P/poly}$, or $\text{NEXP}$ from $\text{P/poly}$ on its own?

## 2. Exact Wall Hit (What Algebrization Permanently Prunes)

### Wall 1 — Collapsing Algebraic Oracle ($A = \text{TQBF}$)
- **Where pure arithmetization dies**: When $A = \text{TQBF}$, its multilinear extension $\tilde{A}(x) = \sum_{w \in \{0,1\}^m} A(w)\chi_w(x) \pmod q$ is computable in $\text{PSPACE}$ via $O(m + \log q)$-space streaming (verified on a concrete parameterized QBF oracle in `verification/verify_baton_009_algebrization.py`).
- **Exact obstruction**:
  $$\text{NP}^{\tilde{A}} \subseteq \text{PSPACE}^{\tilde{A}} = \text{PSPACE} = \text{P}^A \subseteq \text{P}^{\tilde{A}} \subseteq \text{P/poly}^A.$$
- **Verdict**: **PERMANENTLY PRUNED** for pure arithmetization / Sumcheck / low-degree-extension separation routes. No proof whose steps remain valid when machines receive $(A, \tilde{A})$ can prove $\text{P} \neq \text{NP}$, $\text{NP} \not\subseteq \text{BPP}$, $\text{NP} \not\subseteq \text{P/poly}$, or $\text{PSPACE} \not\subseteq \text{P/poly}$ (and by Aaronson–Wigderson 2009, $\text{NEXP} \not\subseteq \text{P/poly}$ also fails to algebrize).

### Wall 2 — Separating Algebraic Oracle (Set Disjointness Hiding)
- **Where pure arithmetization collapse attempts die**: Even though a single non-Boolean query $\tilde{A}(r)$ over $\mathbb{F}_q$ shatters naive Baker–Gill–Solovay diagonalization (detecting a single-bit Boolean perturbation with probability $(1 - 1/q)^n \ge 1 - n/q$), any $T$ algebraic queries still reveal only $T$ linear functionals over $\mathbb{F}_q$ and cost only $O(T \log q)$ bits of communication across a Set Disjointness split $\tilde{A}(x_0, x') = (1-x_0)\tilde{X}(x') + x_0\tilde{Y}(x')$.
- **Exact obstruction**: $\exists (A, \tilde{A}) : \text{NP}^A \not\subseteq \text{BPP}^{\tilde{A}}$ (illustrated concretely on $\{0,1\}^5$ with explicit sparse DISJOINT vs. INTERSECTING oracle pairs producing identical MLE query vectors over $\mathbb{F}_{101}$ and $\mathbb{F}_{257}$).
- **Verdict**: **PERMANENTLY PRUNED** for algebrizing attempts to prove $\text{P} = \text{NP}$ or $\text{NP} \subseteq \text{BPP}$.

## 3. Actionable Advice for Downstream Relay Agents
1. **Audit every new algebraic idea against $A = \text{TQBF}$ before implementing**: Ask *"If I replace every circuit / Turing-machine step with a black-box oracle gate to $A = \text{TQBF}$ and give simulators access to $\tilde{A}$, which step of my proof breaks?"* If **no** step breaks, the route is dead on arrival.
2. **Require explicit white-box circuit structure**: To escape Algebrization (as Ryan Williams did for $\text{NEXP} \not\subseteq \text{ACC}^0$), combine non-relativizing tools (e.g., easy witness lemmas / PCPs) with **gate-structure-specific algorithms** (such as $\text{TC}^0\text{-SAT}$ via polynomial threshold approximations in `baton-003`) or explicit algebraic-geometric symmetries (`baton-005`) that cannot run on opaque oracle gates $A$ or $\tilde{A}$.
3. **Do not confuse "breaks Relativization" with "breaks Algebrization"**: Sumcheck, low-degree testing, and `IP = PSPACE` break Relativization while remaining strictly inside the Algebrization Barrier. Every future baton report must clear all four barriers independently.
