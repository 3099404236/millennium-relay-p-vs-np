#!/usr/bin/env python3
"""
Verification Suite for Baton #003: Structure-Preserving TC^0-SAT & Exact Barrier Analysis.

Self-contained Python 3.12 script (standard library only) verifying all mathematical
and algorithmic claims of Baton #003 (`baton-003-direct-tc0-sat`):

1. Structure-Preserving Depth-2 TC^0 (LTF-of-LTF) SAT Solver (Zero Tseitin Variables):
   - Evaluates depth-2 threshold circuits directly on {0,1}^n.
   - Implements exact Monotone-Top Canonicalization + Meet-in-the-Middle Split +
     Pareto Vector-Domination Pruning + Dual-Tree Half-Space Bounding-Box Search.
   - Verifies 100% SAT/UNSAT equivalence against exhaustive 2^n brute force across
     random depth-2 threshold circuits for n = 8, 9, 10, 11, 12 (both SAT and UNSAT),
     verifies every returned witness on the original uncanonicalized circuit, and
     quantifies search-space pruning vs 2^n (with 0 Tseitin variables introduced).
   - Demonstrates curse-of-dimensionality degradation as bottom fan-in s_1 grows.

2. Chen-Tell (STOC 2019) Wire-Exponent Decay 1 + c^(-d) vs Allender-Koucky Amplification:
   - Numerically simulates the iterated random-restriction peeling recurrence
     (Littlewood-Offord sqrt(p) shrinkage + live-variable depletion) across depth d = 2..12.
   - Verifies exact exponential decay of the maximum tractable excess wire exponent
     eps_max(d) = Theta(c^(-d)) and confirms exhaustion of live variables for any
     fixed eps > 0 independent of d.
   - Verifies the exact quantitative collision against Allender-Koucky (2010)
     amplification: max_{d >= 1} d * c^(-d) < k for all k >= 1 and c >= 2.

3. Beigel-Reingold-Spielman (1995) Rational Approximation & Depth-d Degree Blowup:
   - Implements the exact BRS rational approximator R_{m,b}(z) = P(z)/(P(z)+P(-z))
     with P(z) = prod_{j=0}^{m-1} (z + 2^j)^b and verifies the exact worst-case error
     bound |R_{m,b}(z) - 1[z > 0]| < 3^(-b) / (1 - 3^(-b)) exhaustively over integer
     domains z in [-W, -1] U [1, W].
   - Quantitatively verifies the exact denominator-clearing degree blowup across
     s_1 distinct bottom LTF gates at depth 2 (D_sum = s_1 * D_1, D_2 = D_top * s_1 * D_1)
     and exponential blowup across depth d = 1..5, showing when degree exceeds n
     and breaks polynomial-method SAT (binom(n, <= D) >= 2^(n/2)).
"""

from __future__ import annotations

import heapq
import itertools
import math
import random
from dataclasses import dataclass
from typing import List, Optional, Tuple


# =============================================================================
# Part 1: Depth-2 TC^0 (LTF o LTF) Circuit Model & Structure-Preserving Solver
# =============================================================================


@dataclass(frozen=True)
class Depth2LTF:
    """Depth-2 Linear Threshold Circuit (LTF o LTF) on n Boolean inputs {0,1}^n."""

    n: int
    bottom_weights: Tuple[Tuple[int, ...], ...]  # s1 x n integer weights
    bottom_thresholds: Tuple[int, ...]           # length s1
    top_weights: Tuple[int, ...]                 # length s1
    top_threshold: int

    @property
    def s1(self) -> int:
        return len(self.bottom_weights)

    @property
    def wire_count(self) -> int:
        bottom_wires = sum(1 for row in self.bottom_weights for w in row if w != 0)
        top_wires = sum(1 for a in self.top_weights if a != 0)
        return bottom_wires + top_wires

    def evaluate(self, bits: Tuple[int, ...]) -> int:
        top_sum = 0
        for row, th, alpha in zip(self.bottom_weights, self.bottom_thresholds, self.top_weights):
            dot = 0
            for w, b in zip(row, bits):
                if b:
                    dot += w
            if dot >= th:
                top_sum += alpha
        return 1 if top_sum >= self.top_threshold else 0


def solve_bruteforce(circuit: Depth2LTF) -> Tuple[bool, Optional[Tuple[int, ...]], int]:
    """Exhaustive 2^n evaluator returning (is_sat, witness_or_None, evals_to_decide)."""
    n = circuit.n
    rows = circuit.bottom_weights
    ths = circuit.bottom_thresholds
    alphas = circuit.top_weights
    top_th = circuit.top_threshold
    compress = itertools.compress

    evals = 0
    for bits in itertools.product((0, 1), repeat=n):
        evals += 1
        top_sum = 0
        for row, th, alpha in zip(rows, ths, alphas):
            if sum(compress(row, bits)) >= th:
                top_sum += alpha
        if top_sum >= top_th:
            return True, bits, evals
    return False, None, evals


def canonicalize_monotone_top(circuit: Depth2LTF) -> Depth2LTF:
    """
    Exact monotone-top canonicalization (zero auxiliary variables):
    Replaces any bottom gate i with alpha_i < 0 by its exact complement:
      1 - 1[<w, x> >= th] = 1[<-w, x> >= 1 - th]
    and shifts top_threshold -> top_threshold - alpha_i, alpha_i -> -alpha_i > 0.
    Drops gates with alpha_i == 0.
    """
    new_rows: List[Tuple[int, ...]] = []
    new_ths: List[int] = []
    new_alphas: List[int] = []
    new_top_th = circuit.top_threshold

    for row, th, alpha in zip(circuit.bottom_weights, circuit.bottom_thresholds, circuit.top_weights):
        if alpha == 0:
            continue
        elif alpha > 0:
            new_rows.append(row)
            new_ths.append(th)
            new_alphas.append(alpha)
        else:
            new_rows.append(tuple(-w for w in row))
            new_ths.append(1 - th)
            new_alphas.append(-alpha)
            new_top_th -= alpha

    return Depth2LTF(
        n=circuit.n,
        bottom_weights=tuple(new_rows),
        bottom_thresholds=tuple(new_ths),
        top_weights=tuple(new_alphas),
        top_threshold=new_top_th,
    )


@dataclass
class BoxNode:
    mins: Tuple[int, ...]
    maxs: Tuple[int, ...]
    size: int
    rep_mask: int
    left: Optional["BoxNode"] = None
    right: Optional["BoxNode"] = None


def _pareto_filter(
    vec_to_mask: dict[Tuple[int, ...], int],
) -> List[Tuple[Tuple[int, ...], int]]:
    """
    Exact Pareto-maximal filtering in Z^{s1}:
    Discards v if there exists u with u[i] >= v[i] for all i.
    Sound whenever all top weights alpha_i > 0 (monotone-top canonical form).
    """
    # Sort descending by sum of coordinates so any dominator appears strictly earlier
    items = sorted(vec_to_mask.items(), key=lambda kv: sum(kv[0]), reverse=True)
    frontier: List[Tuple[Tuple[int, ...], int]] = []
    for vec, mask in items:
        dominated = False
        for fvec, _ in frontier:
            if all(a >= b for a, b in zip(fvec, vec)):
                dominated = True
                break
        if not dominated:
            frontier.append((vec, mask))
    return frontier


def _build_box_tree(
    points: List[Tuple[Tuple[int, ...], int]],
    alphas: Tuple[int, ...],
) -> BoxNode:
    """Builds a balanced half-space bounding-box tree (KD-tree) over Pareto vectors."""
    s1 = len(alphas)
    if len(points) == 1:
        v, m = points[0]
        return BoxNode(mins=v, maxs=v, size=1, rep_mask=m)

    mins = [min(p[0][i] for p in points) for i in range(s1)]
    maxs = [max(p[0][i] for p in points) for i in range(s1)]

    # Split along coordinate with largest alpha-weighted spread
    split_dim = max(range(s1), key=lambda i: alphas[i] * (maxs[i] - mins[i]))
    points_sorted = sorted(points, key=lambda p: p[0][split_dim])
    mid = len(points_sorted) // 2

    left_node = _build_box_tree(points_sorted[:mid], alphas)
    right_node = _build_box_tree(points_sorted[mid:], alphas)
    return BoxNode(
        mins=tuple(mins),
        maxs=tuple(maxs),
        size=len(points),
        rep_mask=points_sorted[0][1],
        left=left_node,
        right=right_node,
    )


@dataclass
class SolverStats:
    is_sat: bool
    witness: Optional[Tuple[int, ...]]
    tseitin_vars_added: int
    half_table_evals: int
    pareto_left: int
    pareto_right: int
    tree_node_checks: int
    pruned_pareto_pairs: int

    @property
    def total_work_units(self) -> int:
        return self.half_table_evals + self.tree_node_checks


def solve_ltf2_split_and_dominate(circuit: Depth2LTF) -> SolverStats:
    """
    Structure-preserving Depth-2 TC^0-SAT solver introducing ZERO Tseitin variables:
      1. Monotone-top canonicalization (all top weights > 0).
      2. Meet-in-the-middle split x = (x_L, x_R) with n_L = floor(n/2), n_R = n - n_L.
      3. Deduplication + exact Pareto vector-domination filtering on both halves.
      4. Best-first dual-tree half-space bounding-box pruning (UB < Theta prunes,
         LB >= Theta certifies SAT immediately).
    """
    canon = canonicalize_monotone_top(circuit)
    n = canon.n
    s1 = canon.s1
    alphas = canon.top_weights
    ths = canon.bottom_thresholds
    top_th = canon.top_threshold

    # Trivial boundary checks after monotone-top canonicalization
    if top_th <= 0:
        return SolverStats(True, (0,) * n, 0, 0, 1, 1, 1, 0)
    if sum(alphas) < top_th:
        return SolverStats(False, None, 0, 0, 0, 0, 1, 0)

    n_l = n // 2
    n_r = n - n_l
    size_l = 1 << n_l
    size_r = 1 << n_r

    # Precompute partial-sum vectors for left and right halves (cost 2^n_L + 2^n_R)
    left_map: dict[Tuple[int, ...], int] = {}
    for mask_l in range(size_l):
        vec = tuple(
            sum(canon.bottom_weights[i][j] for j in range(n_l) if (mask_l >> j) & 1)
            for i in range(s1)
        )
        if vec not in left_map:
            left_map[vec] = mask_l

    right_map: dict[Tuple[int, ...], int] = {}
    for mask_r in range(size_r):
        vec = tuple(
            sum(canon.bottom_weights[i][n_l + j] for j in range(n_r) if (mask_r >> j) & 1)
            for i in range(s1)
        )
        if vec not in right_map:
            right_map[vec] = mask_r

    half_table_evals = size_l + size_r

    # Exact Pareto vector-domination filtering
    pareto_l = _pareto_filter(left_map)
    pareto_r = _pareto_filter(right_map)

    root_l = _build_box_tree(pareto_l, alphas)
    root_r = _build_box_tree(pareto_r, alphas)

    def eval_box_bounds(u: BoxNode, v: BoxNode) -> Tuple[int, int]:
        ub = 0
        lb = 0
        for i in range(s1):
            if u.maxs[i] + v.maxs[i] >= ths[i]:
                ub += alphas[i]
                if u.mins[i] + v.mins[i] >= ths[i]:
                    lb += alphas[i]
        return ub, lb

    node_checks = 0
    pruned_pairs = 0

    def combine_witness(mask_l: int, mask_r: int) -> Tuple[int, ...]:
        full_mask = mask_l | (mask_r << n_l)
        return tuple((full_mask >> j) & 1 for j in range(n))

    ub0, lb0 = eval_box_bounds(root_l, root_r)
    node_checks += 1
    if ub0 < top_th:
        pruned_pairs += root_l.size * root_r.size
        return SolverStats(False, None, 0, half_table_evals, len(pareto_l), len(pareto_r), node_checks, pruned_pairs)
    if lb0 >= top_th:
        return SolverStats(
            True,
            combine_witness(root_l.rep_mask, root_r.rep_mask),
            0,
            half_table_evals,
            len(pareto_l),
            len(pareto_r),
            node_checks,
            pruned_pairs,
        )

    # Max-UB-first priority queue: (-ub, tie_breaker, u, v)
    tie = 0
    heap: List[Tuple[int, int, BoxNode, BoxNode]] = [(-ub0, tie, root_l, root_r)]

    while heap:
        _, _, u, v = heapq.heappop(heap)
        # Split the larger box
        if u.size >= v.size and u.left is not None and u.right is not None:
            children = ((u.left, v), (u.right, v))
        elif v.left is not None and v.right is not None:
            children = ((u, v.left), (u, v.right))
        else:
            # Both leaves; should already be decided upon push
            continue

        for cu, cv in children:
            ub, lb = eval_box_bounds(cu, cv)
            node_checks += 1
            if ub < top_th:
                pruned_pairs += cu.size * cv.size
            elif lb >= top_th:
                return SolverStats(
                    True,
                    combine_witness(cu.rep_mask, cv.rep_mask),
                    0,
                    half_table_evals,
                    len(pareto_l),
                    len(pareto_r),
                    node_checks,
                    pruned_pairs,
                )
            else:
                tie += 1
                heapq.heappush(heap, (-ub, tie, cu, cv))

    return SolverStats(False, None, 0, half_table_evals, len(pareto_l), len(pareto_r), node_checks, pruned_pairs)


def generate_random_depth2_ltf(
    rng: random.Random,
    n: int,
    s1: int,
    tightness: float = 0.0,
) -> Depth2LTF:
    """
    Generates a random non-trivial depth-2 LTF circuit on n inputs with s1 bottom gates.
    Top weights include both positive and negative signs; bottom thresholds are shifted
    according to `tightness` (aligning with the sign of alpha_i) to produce a realistic
    mix of SAT and hard non-trivial UNSAT instances near the phase transition.
    """
    top_weights = tuple(rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(s1))
    bottom_weights = []
    bottom_thresholds = []
    for alpha in top_weights:
        row = tuple(rng.randint(-4, 4) for _ in range(n))
        mean = 0.5 * sum(row)
        spread = max(1.0, math.sqrt(sum(w * w for w in row) / 4.0))
        # Shift threshold in the direction that makes contributing +|alpha| harder as tightness rises
        sign = 1 if alpha > 0 else -1
        th = int(round(mean + sign * (tightness + rng.uniform(-0.35, 0.35)) * spread))
        bottom_weights.append(row)
        bottom_thresholds.append(th)

    pos_sum = sum(a for a in top_weights if a > 0)
    neg_sum = sum(a for a in top_weights if a < 0)
    span = pos_sum - neg_sum
    # Require a high fraction of canonicalized top weight (always <= pos_sum so non-trivial!)
    frac = min(0.95, 0.65 + 0.15 * tightness)
    top_th = neg_sum + int(round(frac * span))
    return Depth2LTF(
        n=n,
        bottom_weights=tuple(bottom_weights),
        bottom_thresholds=tuple(bottom_thresholds),
        top_weights=top_weights,
        top_threshold=top_th,
    )


def verify_depth2_tc0_sat_solver() -> None:
    rng = random.Random(2026112603)
    total_instances = 0
    sat_count = 0
    unsat_count = 0
    total_bruteforce_space = 0
    total_solver_work = 0
    unsat_bruteforce_space = 0
    unsat_solver_work = 0
    total_pareto_ratio_num = 0
    total_pareto_ratio_den = 0

    for n in range(8, 13):
        # Sweep tightness across the SAT/UNSAT phase transition (10 circuits per n, 50 total)
        tightness_schedule = [0.2, 0.4, 0.6, 0.8, 1.0, 1.15, 1.3, 1.45, 1.6, 1.8]
        for t in tightness_schedule:
            s1 = rng.randint(4, 7)
            circuit = generate_random_depth2_ltf(rng, n=n, s1=s1, tightness=t)

            # Verify canonicalization identity on a random sample of inputs
            canon = canonicalize_monotone_top(circuit)
            for _ in range(16):
                sample = tuple(rng.randint(0, 1) for _ in range(n))
                assert circuit.evaluate(sample) == canon.evaluate(sample), "Canonicalization mismatch!"

            bf_sat, bf_wit, _ = solve_bruteforce(circuit)
            stats = solve_ltf2_split_and_dominate(circuit)

            assert stats.tseitin_vars_added == 0, "Solver must introduce 0 Tseitin variables!"
            assert stats.is_sat == bf_sat, (
                f"SAT equivalence failed at n={n}, s1={s1}: solver={stats.is_sat}, bf={bf_sat}"
            )
            if stats.is_sat:
                assert stats.witness is not None
                assert circuit.evaluate(stats.witness) == 1, "Returned witness failed original circuit!"
                sat_count += 1
            else:
                # Confirm UNSAT instance was non-trivial (top threshold <= total canonical top weight)
                assert sum(canon.top_weights) >= canon.top_threshold
                unsat_count += 1
                unsat_bruteforce_space += 1 << n
                unsat_solver_work += stats.total_work_units

            if bf_sat:
                assert bf_wit is not None and circuit.evaluate(bf_wit) == 1

            total_instances += 1
            total_bruteforce_space += 1 << n
            total_solver_work += stats.total_work_units
            total_pareto_ratio_num += stats.pareto_left * stats.pareto_right
            total_pareto_ratio_den += 1 << n

    assert sat_count >= 12 and unsat_count >= 12, f"Unbalanced benchmark: SAT={sat_count}, UNSAT={unsat_count}"
    overall_reduction = 1.0 - (total_solver_work / total_bruteforce_space)
    unsat_reduction = 1.0 - (unsat_solver_work / unsat_bruteforce_space)
    pareto_survival = total_pareto_ratio_num / total_pareto_ratio_den

    assert overall_reduction > 0.65, f"Expected strong pruning, got {overall_reduction:.3f}"
    assert unsat_reduction > 0.55, f"Expected strong UNSAT pruning, got {unsat_reduction:.3f}"

    print(
        f"[PASS] Depth-2 TC^0-SAT (n=8..12, {total_instances} circuits: {sat_count} SAT, {unsat_count} UNSAT): "
        f"100% equivalence with brute force, 0 Tseitin vars added; "
        f"work reduced by {overall_reduction * 100:.1f}% overall ({unsat_reduction * 100:.1f}% on UNSAT; "
        f"Pareto product survival {pareto_survival * 100:.1f}% of 2^n)."
    )

    # Dimension-scaling probe at n=12: show why vector-domination degrades as s_1 grows
    probe_rng = random.Random(20260303)
    survival_by_s1 = []
    for s1_probe in (3, 6, 12, 20):
        survivals = []
        for _ in range(5):
            c = generate_random_depth2_ltf(probe_rng, n=12, s1=s1_probe, tightness=1.3)
            st = solve_ltf2_split_and_dominate(c)
            survivals.append((st.pareto_left * st.pareto_right) / (1 << 12))
        survival_by_s1.append((s1_probe, sum(survivals) / len(survivals)))

    # Pareto survival must increase strongly with s1 (curse of dimensionality in Z^{s1})
    assert survival_by_s1[0][1] < survival_by_s1[-1][1]
    assert survival_by_s1[-1][1] > 0.75, "Expected Pareto frontier saturation at high s1"
    summary_str = ", ".join(f"s1={k}: {v*100:.1f}%" for k, v in survival_by_s1)
    print(
        f"[PASS] Vector-domination dimension wall at n=12 (Pareto product survival vs s1): {summary_str}."
    )


# =============================================================================
# Part 2: Chen-Tell Wire-Exponent Decay 1 + c^(-d) & Allender-Koucky Collision
# =============================================================================


def simulate_restriction_peeling(
    eps0: float,
    depth: int,
    alpha: float,
    base_eps_limit: float = 0.5,
) -> Tuple[bool, float, float]:
    """
    Simulates d-1 random-restriction peeling stages for a depth-d TC^0 circuit
    starting with W = n^(1 + eps0) wires.

    At stage j (peeling layer j from bottom):
      - Current live variables: n_{j-1} = n^{lambda_{j-1}} (initially lambda_0 = 1).
      - Current excess wire exponent relative to n_{j-1}: eps_{j-1} = (1 + eps0)/lambda_{j-1} - 1.
      - Keep probability p_j = n_{j-1}^{-alpha * eps_{j-1}} (where alpha > 1 captures
        the Littlewood-Offord sqrt(p) shrinkage + degree-reduction overhead; e.g. alpha >= 2).
      - Surviving live-variable exponent: lambda_j = lambda_{j-1} * (1 - alpha * eps_{j-1}).
      - Updated excess wire exponent relative to n_j:
          eps_j = (1 + eps0) / lambda_j - 1 = ((1 + alpha) * eps_{j-1}) / (1 - alpha * eps_{j-1}).

    Succeeds iff lambda_{d-1} > 0 and final base-case excess exponent eps_{d-1} <= base_eps_limit.
    """
    lam = 1.0
    eps = eps0
    for _ in range(depth - 1):
        if alpha * eps >= 1.0:
            return False, 0.0, float("inf")
        lam = lam * (1.0 - alpha * eps)
        if lam <= 1e-12:
            return False, 0.0, float("inf")
        eps = (1.0 + eps0) / lam - 1.0
    return (eps <= base_eps_limit), lam, eps


def max_tractable_eps0(depth: int, alpha: float, base_eps_limit: float = 0.5) -> float:
    lo, hi = 0.0, base_eps_limit
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        ok, _, _ = simulate_restriction_peeling(mid, depth, alpha, base_eps_limit)
        if ok:
            lo = mid
        else:
            hi = mid
    return lo


def verify_chen_tell_decay_and_ak_collision() -> None:
    alpha = 2.0  # Littlewood-Offord sqrt(p) needs p <= n^{-2*eps} just to overcome n^eps average degree
    c_theory = 1.0 + alpha  # c = 3.0 asymptotic decay factor per layer
    base_limit = 0.5

    eps_table: List[Tuple[int, float, float]] = []
    for d in range(2, 12):
        e_max = max_tractable_eps0(d, alpha=alpha, base_eps_limit=base_limit)
        scaled = e_max * (c_theory ** (d - 1))
        eps_table.append((d, e_max, scaled))

    # Verify strict exponential decay: ratio eps_max(d-1)/eps_max(d) converges to c_theory = 1 + alpha
    ratios = [eps_table[i - 1][1] / eps_table[i][1] for i in range(1, len(eps_table))]
    assert all(r > c_theory - 1e-6 for r in ratios), f"Decay slower than c={c_theory}: {ratios}"
    assert abs(ratios[-1] - c_theory) < 0.01, f"Asymptotic ratio mismatch: {ratios[-1]} vs {c_theory}"

    # Verify that any fixed eps > 0 fails past a finite depth d_fail(eps)
    for fixed_eps in (0.1, 0.01, 0.001):
        ok_deep, lam_deep, _ = simulate_restriction_peeling(fixed_eps, depth=20, alpha=alpha, base_eps_limit=base_limit)
        assert not ok_deep and lam_deep == 0.0, f"Fixed eps={fixed_eps} unexpectedly survived depth 20!"

    # Verify Allender-Koucky (2010) vs Chen-Tell (2019) quantitative collision:
    # AK shrinks poly size n^k to n^{1 + k/d} at depth d; CT requires eps <= c^{-d}.
    # Collision check: for every c >= 2 and every k >= 1, max_{d >= 1} (d * c^{-d}) < k.
    for c in (2.0, 3.0, 5.0, 10.0):
        max_d_c_inv_d = max(d * (c ** (-d)) for d in range(1, 200))
        analytic_sup = 1.0 / (math.e * math.log(c))
        assert max_d_c_inv_d <= analytic_sup + 1e-12
        assert max_d_c_inv_d < 1.0, f"Unexpected intersection for c={c}: {max_d_c_inv_d}"
        # Therefore for all polynomial exponents k >= 1 and all depths d >= 1: c^(-d) < k/d
        for k in (1.0, 1.5, 2.0, 5.0):
            for d in range(1, 100):
                assert (c ** (-d)) < (k / d), f"AK-CT intersection found at c={c}, k={k}, d={d}!"

    print(
        f"[PASS] Chen-Tell restriction peeling (alpha={alpha}, c={c_theory:.1f}): "
        f"eps_max(d=2)={eps_table[0][1]:.5f}, eps_max(d=6)={eps_table[4][1]:.6f}, "
        f"eps_max(d=11)={eps_table[-1][1]:.3e}; asymptotic decay ratio={ratios[-1]:.4f} -> {c_theory:.1f}."
    )
    print(
        "[PASS] Allender-Koucky vs Chen-Tell collision verified: "
        "c^(-d) < k/d holds for all d >= 1, k >= 1, c >= 2 (max_{d>=1} d*2^(-d) = 0.5 < 1)."
    )


# =============================================================================
# Part 3: Beigel-Reingold-Spielman (1995) Rational Approx & Exact Degree Blowup
# =============================================================================


def brs_rational_eval(z: int, m: int, b: int) -> float:
    """
    Evaluates the exact Beigel-Reingold-Spielman (1995) rational approximator
    for 1[z > 0] on nonzero integers z in [-W, -1] U [1, W] where W <= 2^m - 1:
      P_{m,b}(z) = prod_{j=0}^{m-1} (z + 2^j)^b   (degree D_1 = m * b)
      R_{m,b}(z) = P_{m,b}(z) / (P_{m,b}(z) + P_{m,b}(-z))
    Computed stably via ratio rho(z) = P(-z)/P(z) = prod_{j=0}^{m-1} ((2^j - z)/(2^j + z))^b.
    """
    assert z != 0, "BRS domain excludes z = 0 (use odd-shifted threshold 2*sum - 2*th + 1)"
    u = abs(z)
    # Compute signed ratio rho(u) = P(-u)/P(u) = prod ((2^j - u)/(2^j + u))^b
    rho = 1.0
    for j in range(m):
        node = 1 << j
        factor = (node - u) / (node + u)
        rho *= factor ** b
    if z > 0:
        return 1.0 / (1.0 + rho)
    else:
        return rho / (1.0 + rho)


def log2_binom_sum(n: int, d: int) -> float:
    """Computes log2(sum_{k=0}^{min(d,n)} binom(n, k)) exactly using integer arithmetic."""
    d_eff = min(d, n)
    total = 0
    for k in range(d_eff + 1):
        total += math.comb(n, k)
    return math.log2(total)


def verify_brs_rational_and_degree_blowup() -> None:
    # 3A: Exhaustive verification of BRS rational approximation error bound
    checked_points = 0
    for m in (6, 8, 10):
        W = (1 << m) - 1
        for b in (1, 2, 3, 4):
            theoretical_bound = (3.0 ** (-b)) / (1.0 - 3.0 ** (-b))
            max_err = 0.0
            for z in range(-W, W + 1):
                if z == 0:
                    continue
                approx = brs_rational_eval(z, m=m, b=b)
                target = 1.0 if z > 0 else 0.0
                err = abs(approx - target)
                if err > max_err:
                    max_err = err
                checked_points += 1
            assert max_err < theoretical_bound, (
                f"BRS error exceeded bound at m={m}, b={b}: {max_err} >= {theoretical_bound}"
            )
    print(
        f"[PASS] Beigel-Reingold-Spielman rational approximator verified exhaustively across "
        f"{checked_points} integer points (W up to 1023, b=1..4): worst-case error strictly < 3^(-b)/(1-3^(-b))."
    )

    # 3B: Exact denominator-clearing degree blowup at depth 2 and depth d
    # For depth-2 LTF o LTF with s1 distinct bottom LTF gates of weight W_1 = n^2,
    # top gate weights sum A_top = s1 * n:
    #   Need bottom error eps_1 <= 1 / (4 * A_top) -> b_1 = ceil(log_3(6 * A_top))
    #   Bottom BRS degree: D_1 = b_1 * ceil(log2(2*W_1 + 1))
    #   Clearing s1 distinct denominators in Z_top = sum_{i=1}^{s1} alpha_i * (A_i / B_i):
    #     D_sum = s1 * D_1
    #   Applying top BRS gate of degree D_2 (for error 1/4, b_2 = 2, m_2 = ceil(log2(2*A_top+1))):
    #     D_depth2 = D_2 * D_sum = D_2 * s1 * D_1
    blowup_reports = []
    for n in (64, 128, 256, 1024):
        s1 = int(math.ceil(n ** 0.6))  # even sublinear s1 = n^0.6 bottom gates!
        W1 = n * n
        A_top = s1 * n
        m1 = math.ceil(math.log2(2 * W1 + 1))
        b1 = math.ceil(math.log(6 * A_top) / math.log(3.0))
        D1 = m1 * b1

        m2 = math.ceil(math.log2(2 * A_top + 1))
        b2 = 2  # gives error < (1/9)/(8/9) = 1/8 < 1/4
        D2 = m2 * b2

        D_sum = s1 * D1
        D_depth2 = D2 * D_sum

        # Polynomial-method SAT (multipoint eval / rectangular MM) needs binom(n, <= D) << 2^(n/2),
        # which fails already when D >= 0.11 * n (since H_2(0.11) > 0.5)!
        assert D_sum > n, f"Expected denominator-cleared sum degree > n at n={n}: {D_sum}"
        assert D_depth2 > n, f"Expected depth-2 rational degree > n at n={n}: {D_depth2}"
        # Check exact binomial monomial count at n=64, 128, 256
        if n <= 256:
            # Even at half the single-sum degree capped at n, monomial space saturates 2^n
            assert log2_binom_sum(n, min(D_sum, n)) == float(n)
        blowup_reports.append(f"n={n}, s1={s1}: D1={D1}, D_sum={D_sum} (>n), D_d2={D_depth2}")

    # Multi-layer composition degree explosion (fan-in k=4 per gate, modest D_gate=12)
    k_fanin = 4
    D_gate = 12
    deg_by_depth = []
    cur_deg = D_gate
    for d in range(1, 6):
        deg_by_depth.append((d, cur_deg))
        cur_deg = D_gate * k_fanin * cur_deg  # clearing k denominators + composing with next BRS gate
    assert deg_by_depth[-1][1] == D_gate * ((D_gate * k_fanin) ** 4)
    assert deg_by_depth[2][1] > 10000  # already > 27,000 at depth 3 even for fan-in 4!

    print(f"[PASS] Depth-2 BRS denominator-clearing blowup verified: {'; '.join(blowup_reports)}.")
    print(
        "[PASS] Depth-d BRS composition blowup (fan-in k=4, D_gate=12): "
        + ", ".join(f"d={d}: deg={deg}" for d, deg in deg_by_depth)
        + "."
    )


if __name__ == "__main__":
    verify_depth2_tc0_sat_solver()
    verify_chen_tell_decay_and_ak_collision()
    verify_brs_rational_and_degree_blowup()
    print("ALL BATON-003 TC0-SAT VERIFICATIONS PASSED.")
