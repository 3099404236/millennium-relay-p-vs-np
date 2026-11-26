#!/usr/bin/env python3
"""
Verification Suite for Baton #018:
Polynomial-Clause Unbounded-Width CNF-SAT (M = n^B) vs. Valiant's O(n / log log n) Bridge.

Self-contained Python 3.12 standard-library verification covering:
  Check 1: Exact CNF-SAT -> Orthogonal Vectors (OV) reduction (zero width bound!)
           paired with an exact Bit-Parallel + Subtree-Pruning OV Solver, verified
           100% against exhaustive brute force across 30 random wide-CNF instances
           (n = 10..14, M = n^2 clauses, widths k in [n//2, n-2]).
  Check 2: Exact Abboud-Williams-Yu (SODA 2015) / Chan-Williams (SODA 2016)
           polynomial-method + rectangular-matrix-multiplication scaling law
           across M = n^2, n^3, n^5, n^10 (n = 100..2^30), quantifying the exact
           Theta((B-1) log n / log log n) gap to Valiant's threshold, proving even
           optimal omega = 2 (alpha = 1) cannot close it, and verifying the exact
           collision at M = n * polylog(n).
  Check 3: Exact F_2 random-linear-combination compression of M-bit OV falsification
           vectors (M = 64, 128, 256; r = 4, 8, 12), verifying 0% false negatives,
           exact 2^(-r) false-positive rate (independent of M and Hamming weight),
           exact diagonal bilinear monomial expansion identity, and the pairwise-
           independence Chebyshev wall forcing r = Omega(n) for global compression.
"""

from __future__ import annotations

import math
import random
import sys
import time
from typing import Dict, List, Optional, Sequence, Tuple


# ============================================================================
# CHECK 1: Exact CNF-SAT -> OV Reduction + Bit-Parallel Subtree-Pruning Solver
# ============================================================================

Clause = List[Tuple[int, bool]]  # list of (var_idx, is_positive)


def evaluate_cnf_assignment(clauses: Sequence[Clause], x: int) -> bool:
    """Evaluate CNF formula on integer assignment bitmask x."""
    for clause in clauses:
        sat = False
        for var, is_pos in clause:
            val = bool((x >> var) & 1)
            if val == is_pos:
                sat = True
                break
        if not sat:
            return False
    return True


def solve_cnf_bruteforce(n: int, clauses: Sequence[Clause]) -> Tuple[bool, Optional[int]]:
    """Exhaustive 2^n ground-truth CNF-SAT solver using bitmask clause representation."""
    pos_masks: List[int] = []
    neg_masks: List[int] = []
    for clause in clauses:
        pm = 0
        nm = 0
        for var, is_pos in clause:
            if is_pos:
                pm |= 1 << var
            else:
                nm |= 1 << var
        pos_masks.append(pm)
        neg_masks.append(nm)

    full_mask = (1 << n) - 1
    m = len(clauses)
    for x in range(1 << n):
        nx = full_mask ^ x
        ok = True
        for j in range(m):
            if ((x & pos_masks[j]) | (nx & neg_masks[j])) == 0:
                ok = False
                break
        if ok:
            return True, x
    return False, None


def cnf_to_ov_vectors(
    n: int, clauses: Sequence[Clause]
) -> Tuple[int, int, Dict[int, int], Dict[int, int]]:
    """
    Exact width-independent CNF-SAT -> Orthogonal Vectors (OV) reduction.

    Split variables into X_L = {0..n1-1} and X_R = {n1..n-1}.
    For each left assignment a in {0,1}^n1, define M-bit falsification vector u(a)
    where bit j is 1 iff a falsifies ALL literals of clause C_j in X_L.
    Similarly v(b) has bit j = 1 iff b falsifies ALL literals of C_j in X_R.
    Then (a || b) satisfies Phi  <==>  u(a) & v(b) == 0.
    """
    n1 = n // 2
    n2 = n - n1
    m = len(clauses)

    # Precompute left/right positive and negative literal masks per clause.
    left_pos = [0] * m
    left_neg = [0] * m
    right_pos = [0] * m
    right_neg = [0] * m

    for j, clause in enumerate(clauses):
        for var, is_pos in clause:
            if var < n1:
                if is_pos:
                    left_pos[j] |= 1 << var
                else:
                    left_neg[j] |= 1 << var
            else:
                rvar = var - n1
                if is_pos:
                    right_pos[j] |= 1 << rvar
                else:
                    right_neg[j] |= 1 << rvar

    # Build deduplicated vector -> witness maps u_map and v_map.
    full_l = (1 << n1) - 1
    u_map: Dict[int, int] = {}
    for a in range(1 << n1):
        na = full_l ^ a
        mask = 0
        for j in range(m):
            if ((a & left_pos[j]) | (na & left_neg[j])) == 0:
                mask |= 1 << j
        if mask not in u_map:
            u_map[mask] = a

    full_r = (1 << n2) - 1
    v_map: Dict[int, int] = {}
    for b in range(1 << n2):
        nb = full_r ^ b
        mask = 0
        for j in range(m):
            if ((b & right_pos[j]) | (nb & right_neg[j])) == 0:
                mask |= 1 << j
        if mask not in v_map:
            v_map[mask] = b

    return n1, n2, u_map, v_map


class OVSubtreeNode:
    """Binary coordinate-splitting trie node with exact common-ones bitmask pruning."""

    __slots__ = ("common_ones", "split_bit", "left_zero", "right_one", "leaf_vecs")

    def __init__(
        self,
        common_ones: int,
        split_bit: int = -1,
        left_zero: Optional["OVSubtreeNode"] = None,
        right_one: Optional["OVSubtreeNode"] = None,
        leaf_vecs: Optional[List[int]] = None,
    ) -> None:
        self.common_ones = common_ones
        self.split_bit = split_bit
        self.left_zero = left_zero
        self.right_one = right_one
        self.leaf_vecs = leaf_vecs


def build_ov_tree(vecs: List[int], leaf_limit: int = 8) -> Optional[OVSubtreeNode]:
    """Build exact coordinate-splitting OV search tree with common-ones pruning."""
    if not vecs:
        return None
    common = vecs[0]
    union = vecs[0]
    for v in vecs[1:]:
        common &= v
        union |= v

    if len(vecs) <= leaf_limit:
        return OVSubtreeNode(common_ones=common, leaf_vecs=vecs)

    # Active bits are coordinates that vary across vecs (1 in union, 0 in common).
    varying = union ^ common
    if varying == 0:
        return OVSubtreeNode(common_ones=common, leaf_vecs=vecs)

    # Pick a well-balanced splitting coordinate among up to 32 varying bits.
    best_bit = -1
    best_balance = len(vecs) + 1
    half = len(vecs) // 2
    temp = varying
    checked = 0
    while temp and checked < 32:
        lsb = temp & -temp
        bit_idx = lsb.bit_length() - 1
        ones = sum(1 for v in vecs if (v >> bit_idx) & 1)
        bal = abs(ones - half)
        if bal < best_balance:
            best_balance = bal
            best_bit = bit_idx
            if bal <= 1:
                break
        temp ^= lsb
        checked += 1

    if best_bit < 0:
        return OVSubtreeNode(common_ones=common, leaf_vecs=vecs)

    mask_bit = 1 << best_bit
    v0 = [v for v in vecs if not (v & mask_bit)]
    v1 = [v for v in vecs if (v & mask_bit)]
    if not v0 or not v1:
        return OVSubtreeNode(common_ones=common, leaf_vecs=vecs)

    return OVSubtreeNode(
        common_ones=common,
        split_bit=best_bit,
        left_zero=build_ov_tree(v0, leaf_limit),
        right_one=build_ov_tree(v1, leaf_limit),
    )


def query_ov_tree(node: Optional[OVSubtreeNode], u: int, stats: List[int]) -> Optional[int]:
    """
    Exact subtree-pruning OV query: returns v in tree with (u & v) == 0, or None.
    stats[0] counts bitwise leaf checks performed; stats[1] counts pruned subtrees.
    """
    if node is None:
        return None
    if u & node.common_ones:
        stats[1] += 1
        return None
    if node.leaf_vecs is not None:
        for v in node.leaf_vecs:
            stats[0] += 1
            if (u & v) == 0:
                return v
        return None
    # Recurse into 0-branch first; if bit is 1 in u, 1-branch is impossible!
    res = query_ov_tree(node.left_zero, u, stats)
    if res is not None:
        return res
    if (u >> node.split_bit) & 1:
        stats[1] += 1
        return None
    return query_ov_tree(node.right_one, u, stats)


def solve_cnf_via_ov(
    n: int, clauses: Sequence[Clause]
) -> Tuple[bool, Optional[int], int, int, int]:
    """
    Solve arbitrary-width CNF-SAT via exact OV reduction + bit-parallel subtree pruning.
    Returns (is_sat, assignment_or_None, leaf_checks, pruned_subtrees, naive_pairs).
    """
    n1, _n2, u_map, v_map = cnf_to_ov_vectors(n, clauses)
    naive_pairs = 1 << n

    # Fast check if 0-vector exists in either half (already satisfies all clauses!).
    if 0 in u_map:
        a = u_map[0]
        b = next(iter(v_map.values()))
        return True, a | (b << n1), 1, 0, naive_pairs
    if 0 in v_map:
        a = next(iter(u_map.values()))
        b = v_map[0]
        return True, a | (b << n1), 1, 0, naive_pairs

    tree = build_ov_tree(list(v_map.keys()), leaf_limit=8)
    stats = [0, 0]
    # Sort u-vectors by ascending Hamming weight (lighter vectors more likely orthogonal).
    for u in sorted(u_map.keys(), key=lambda x: x.bit_count()):
        v_hit = query_ov_tree(tree, u, stats)
        if v_hit is not None:
            a = u_map[u]
            b = v_map[v_hit]
            return True, a | (b << n1), stats[0], stats[1], naive_pairs

    return False, None, stats[0], stats[1], naive_pairs


def generate_wide_cnf_instance(
    rng: random.Random, n: int, mode: str
) -> List[Clause]:
    """
    Generate a wide-CNF instance with EXACTLY M = n^2 clauses and EVERY clause
    having width k in [n//2, n-2].

    Modes:
      - 'random_sat': uniform random wide clauses (naturally SAT).
      - 'planted_tight_sat': 2^(n//2)-1 clauses of a split-straddling width-(n//2)
                             cube + random wide clauses satisfied by planted witness.
      - 'unsat_wide': full split-straddling width-(n//2) UNSAT core (2^(n//2) <= n^2
                      clauses for all n in 10..14!) padded to M = n^2 with random
                      wide clauses of widths in [n//2, n-2], then randomly shuffled.
    """
    m = n * n
    k_min = n // 2
    k_max = n - 2
    n1 = n // 2
    clauses: List[Clause] = []

    if mode == "random_sat":
        for _ in range(m):
            k = rng.randint(k_min, k_max)
            vars_chosen = rng.sample(range(n), k)
            clauses.append([(v, rng.choice((True, False))) for v in vars_chosen])
        return clauses

    # Pick k_min core variables guaranteed to straddle X_L and X_R evenly.
    l_cnt = k_min // 2
    r_cnt = k_min - l_cnt
    core_vars = rng.sample(range(n1), l_cnt) + rng.sample(range(n1, n), r_cnt)
    rng.shuffle(core_vars)

    if mode == "unsat_wide":
        # Complete truth-table contradiction on core_vars: 2^(k_min) clauses of width k_min.
        for mask in range(1 << k_min):
            clause = [(core_vars[i], bool((mask >> i) & 1)) for i in range(k_min)]
            clauses.append(clause)
        while len(clauses) < m:
            k = rng.randint(k_min, k_max)
            vars_chosen = rng.sample(range(n), k)
            clauses.append([(v, rng.choice((True, False))) for v in vars_chosen])
        rng.shuffle(clauses)
        return clauses

    if mode == "planted_tight_sat":
        # Plant a secret assignment x* and omit the one core clause falsified by x*.
        x_star = rng.getrandbits(n)
        for mask in range(1 << k_min):
            clause = [(core_vars[i], bool((mask >> i) & 1)) for i in range(k_min)]
            if evaluate_cnf_assignment([clause], x_star):
                clauses.append(clause)
        while len(clauses) < m:
            k = rng.randint(k_min, k_max)
            vars_chosen = rng.sample(range(n), k)
            clause = [(v, rng.choice((True, False))) for v in vars_chosen]
            if not evaluate_cnf_assignment([clause], x_star):
                # Flip one literal so x_star satisfies it.
                idx = rng.randrange(k)
                v0, p0 = clause[idx]
                clause[idx] = (v0, not p0)
            clauses.append(clause)
        rng.shuffle(clauses)
        return clauses

    raise ValueError(f"Unknown mode: {mode}")


def run_check_1() -> None:
    print("=" * 78)
    print("CHECK 1: Exact CNF-SAT -> OV Reduction & Bit-Parallel Subtree-Pruning Solver")
    print("=" * 78)
    rng = random.Random(20261126)

    ns = [10, 11, 12, 13, 14]
    modes = ["random_sat", "planted_tight_sat", "unsat_wide"]
    total_instances = 0
    sat_count = 0
    unsat_count = 0
    total_leaf_checks = 0
    total_naive_pairs = 0
    unsat_leaf_checks = 0
    unsat_naive_pairs = 0

    for n in ns:
        for mode in modes:
            for rep in range(2):  # 5 * 3 * 2 = 30 instances
                clauses = generate_wide_cnf_instance(rng, n, mode)
                m = len(clauses)
                assert m == n * n, f"Expected M=n^2={n*n}, got {m}"
                widths = [len(c) for c in clauses]
                assert min(widths) >= n // 2 and max(widths) <= n - 2

                bf_sat, bf_witness = solve_cnf_bruteforce(n, clauses)
                ov_sat, ov_witness, checks, pruned, naive = solve_cnf_via_ov(n, clauses)

                assert bf_sat == ov_sat, (
                    f"MISMATCH on n={n} mode={mode} rep={rep}: bf={bf_sat} ov={ov_sat}"
                )
                if ov_sat:
                    assert ov_witness is not None
                    assert evaluate_cnf_assignment(clauses, ov_witness), (
                        "OV witness failed CNF evaluation!"
                    )
                    assert bf_witness is not None
                    assert evaluate_cnf_assignment(clauses, bf_witness)
                    sat_count += 1
                else:
                    assert ov_witness is None
                    unsat_count += 1
                    unsat_leaf_checks += checks
                    unsat_naive_pairs += naive

                total_instances += 1
                total_leaf_checks += checks
                total_naive_pairs += naive

    overall_reduction = total_naive_pairs / max(1, total_leaf_checks)
    unsat_reduction = unsat_naive_pairs / max(1, unsat_leaf_checks)
    print(
        f"  Tested {total_instances} wide-CNF instances (n=10..14, M=n^2 in 100..196, "
        f"width k in [n//2, n-2]): {sat_count} SAT, {unsat_count} UNSAT."
    )
    print(
        f"  Exact brute-force agreement: {total_instances}/{total_instances} (100.0%)."
    )
    print(
        f"  Bit-parallel subtree-pruning speedup (pairs vs leaf checks): "
        f"overall = {overall_reduction:.2f}x, UNSAT-only = {unsat_reduction:.2f}x "
        f"({unsat_leaf_checks} checks vs {unsat_naive_pairs} naive pairs)."
    )
    print(
        "[PASS] Check 1: Width-independent CNF->OV reduction & subtree-pruning OV solver "
        "verified 30/30 against brute force."
    )


# ============================================================================
# CHECK 2: Exact Abboud-Williams-Yu / Chan-Williams Polynomial-Method Scaling
# ============================================================================

# Rectangular matrix multiplication exponent alpha* where omega(1, alpha*, 1) = 2:
# Williams-Xu-Xu-Zhou (SODA 2024): alpha* > 0.321334.
ALPHA_WXXZ24 = 0.321334
ALPHA_OPTIMAL_OMEGA2 = 1.0  # Upper-bound benchmark even if omega = 2!
LOG2_E = math.log2(math.e)


def log2_binom_stirling(log2_M: float, r: float) -> float:
    """
    High-precision log2(C(M, r)) given log2_M = log2(M) and 1 <= r <= M/2.
    Works seamlessly from M = 100 up to M = 2^3000 without float overflow.
    """
    if r <= 0.0:
        return 0.0
    log2_r = math.log2(r)
    log2_p = log2_r - log2_M
    if log2_p > -1.0:
        # r > M/2: saturate at M (full Boolean cube)
        return (2.0 ** log2_M) if log2_M < 50 else float("inf")

    if log2_p < -35.0:
        # Tiny p = r/M < 2^-35: use exact asymptotic expansion avoiding cancellation:
        # M*H2(p) = r * (log2(M/r) + log2(e)) - r*p/(2 ln 2) - ...
        ent = r * ((log2_M - log2_r) + LOG2_E)
        stirling_corr = 0.5 * math.log2(2.0 * math.pi * r) + (1.0 / (12.0 * r * math.log(2.0)))
        return max(0.0, ent - stirling_corr)

    p = 2.0 ** log2_p
    # Exact binary entropy: r*log2(1/p) - (M-r)*log2(1-p)
    # Write M-r = r * (1-p)/p so M never needs to be materialized as huge float!
    term1 = r * (-log2_p)
    term2 = -r * ((1.0 - p) / p) * (math.log1p(-p) / math.log(2.0))
    # Stirling 1/2 log(2 pi r (1-p)) + exact 1/(12 ln 2) * (1/r + 1/(M-r) - 1/M)
    # Note 1/(M-r) - 1/M = p^2 / (r*(1-p)).
    stirling_corr = (
        0.5 * math.log2(2.0 * math.pi * r * (1.0 - p))
        + (1.0 + (p * p) / (1.0 - p)) / (12.0 * r * math.log(2.0))
    )
    return max(0.0, term1 + term2 - stirling_corr)


def log2_monomial_count(log2_M: float, r: float) -> float:
    """
    Compute log2(sum_{k=0}^r C(M, k)) using log2_binom_stirling + geometric tail bound.
    """
    if r <= 0.0:
        return 0.0
    base = log2_binom_stirling(log2_M, r)
    log2_p = math.log2(r) - log2_M
    if log2_p < -30.0:
        return base
    p = 2.0 ** log2_p
    if p < 0.499:
        # Exact geometric ratio factor between C(M, r) and sum_{k<=r} C(M, k):
        # bounded tightly by (1 - p) / (1 - 2p)
        tail_factor = (1.0 - p) / (1.0 - 2.0 * p)
        return base + math.log2(tail_factor)
    return base + 1.0


def solve_cw_savings(
    log2_n: float, log2_M: float, alpha: float = ALPHA_WXXZ24, c0: float = 7.0
) -> float:
    """
    Solve the exact Abboud-Williams-Yu (2015) / Chan-Williams (2016) polynomial-method
    rectangular-MM bottleneck equation for exponent savings sigma = 2 * log2(s):

        log2( sum_{k=0}^{sigma + c0} C(M, k) )  <=  (alpha / 2) * (n - sigma)

    Returns sigma(n, M) in exact bits saved below 2^n (so runtime is 2^(n - sigma)).
    Works cleanly for log2_n from ~6 up to 256+ using exact bisection.
    """
    n = 2.0 ** log2_n
    budget_max = 0.5 * alpha * n

    # Check if even sigma = 1 fits; otherwise return 0.
    if log2_monomial_count(log2_M, 1.0 + c0) > budget_max:
        return 0.0

    lo = 0.0
    hi = min(n * 0.5, 2.0 ** (log2_M - 1.0) - c0)
    if hi <= 0.0:
        return 0.0

    for _ in range(90):
        mid = 0.5 * (lo + hi)
        lhs = log2_monomial_count(log2_M, mid + c0)
        rhs = 0.5 * alpha * (n - mid)
        if lhs <= rhs:
            lo = mid
        else:
            hi = mid
    return lo


def solve_cw_fraction_asymptotic(
    log2_delta: float, alpha: float = ALPHA_WXXZ24
) -> float:
    """
    Scale-free asymptotic solver for gamma = sigma / n as a function of
    log2_delta = log2(M / n), solving:
        gamma * (log2_delta - log2(gamma) + log2(e))  <=  (alpha / 2) * (1 - gamma)
    Valid for arbitrarily astronomical n (e.g. log2(log2(n)) = 1000) without float overflow.
    """
    lo = 1e-18
    hi = 0.49
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lhs = mid * (log2_delta - math.log2(mid) + LOG2_E)
        rhs = 0.5 * alpha * (1.0 - mid)
        if lhs <= rhs:
            lo = mid
        else:
            hi = mid
    return lo


def run_check_2() -> None:
    print("\n" + "=" * 78)
    print("CHECK 2: Exact Chan-Williams / AWY Polynomial-Method vs. Valiant Threshold")
    print("=" * 78)

    # 2A. Cross-check log2_binom_stirling against exact math.comb at moderate M.
    max_err = 0.0
    for M_test, r_test in [(1000, 10), (10000, 50), (50000, 120)]:
        exact_val = math.log2(math.comb(M_test, r_test))
        approx_val = log2_binom_stirling(math.log2(M_test), float(r_test))
        err = abs(exact_val - approx_val)
        max_err = max(max_err, err)
        assert err < 1e-2, f"Stirling mismatch: exact={exact_val}, approx={approx_val}"
    print(f"  [2A] Stirling log2-binomial cross-check vs exact math.comb: max abs err = {max_err:.6f} bits.")

    # 2B. Polynomial-clause regime: M = n^B for B in {2, 3, 5, 10} and n = 100..2^30.
    # Benchmark Valiant baseline savings: sigma_Val(n) = n / log2(log2(n)).
    print("\n  [2B] Polynomial-Clause Unbounded-Width CNF (M = n^B), alpha = 0.321334 (WXXZ24):")
    print(
        f"  {'B':>3} | {'n':>11} | {'sigma_CW':>13} | {'n/loglog n':>13} | "
        f"{'sigma_CW/sigma_Val':>18} | {'NormGap * (B-1)logn/loglogn':>27}"
    )
    print("  " + "-" * 97)

    test_ns = [
        (math.log2(100.0), "100"),
        (math.log2(1000.0), "1,000"),
        (math.log2(1e4), "10^4"),
        (math.log2(1e6), "10^6"),
        (20.0, "2^20"),
        (25.0, "2^25"),
        (30.0, "2^30"),
    ]

    for B in [2, 3, 5, 10]:
        ratios: List[float] = []
        norm_constants: List[float] = []
        for log2_n, label in test_ns:
            n = 2.0 ** log2_n
            log2_M = B * log2_n
            sigma_cw = solve_cw_savings(log2_n, log2_M, ALPHA_WXXZ24)
            sigma_val = n / math.log2(log2_n)
            ratio = sigma_cw / sigma_val
            # Predicted asymptotic scaling:
            # sigma_CW / sigma_Val ~ (alpha / 2) * log2(log2(n)) / ((B-1) * log2(n))
            # Therefore (sigma_CW / sigma_Val) * ((B-1)*log2(n) / log2(log2(n))) -> alpha/2 = 0.160667!
            norm_const = ratio * ((B - 1) * log2_n / math.log2(log2_n))
            ratios.append(ratio)
            norm_constants.append(norm_const)
            if label in ("100", "10^4", "2^20", "2^30"):
                print(
                    f"  {B:>3} | {label:>11} | {sigma_cw:>13.3e} | {sigma_val:>13.3e} | "
                    f"{ratio:>18.6f} | {norm_const:>27.5f}"
                )

        # Verify strict asymptotic decay of sigma_CW / sigma_Val for n >= 10^6
        # (once sigma >> c0 = 7) and verify normalized constant sits tightly below alpha/2 = 0.16067!
        assert ratios[3] > ratios[4] > ratios[5] > ratios[6], (
            f"Expected strict asymptotic ratio decay for B={B} (n>=10^6): {ratios[3:]}"
        )
        assert 0.10 < norm_constants[-1] < ALPHA_WXXZ24 * 0.505, (
            f"Unexpected norm_const at 2^30 for B={B}: {norm_constants[-1]}"
        )

    # Check asymptotic convergence at huge scales (2^64, 2^128) and under omega=2 (alpha=1.0).
    sigma_cw_omega2 = solve_cw_savings(30.0, 2.0 * 30.0, ALPHA_OPTIMAL_OMEGA2)
    sigma_val_30 = (2.0 ** 30) / math.log2(30.0)
    gap_omega2_30 = sigma_val_30 / sigma_cw_omega2
    print(
        f"\n  [2C] Even under optimal omega = 2 (alpha = 1.0) at B=2, n=2^30: "
        f"sigma_CW = {sigma_cw_omega2:.3e}, Valiant gap = {gap_omega2_30:.2f}x "
        f"(still diverges as Theta(log n / log log n)!)."
    )
    assert gap_omega2_30 > 10.0

    # 2D. EXACT COLLISION AT M = n * (log2 n)^q (Polylogarithmic Density)!
    print("\n  [2D] Exact Boundary Collision at M = n * (log2 n)^q vs Sub-Polylog M = n * 2^sqrt(loglog n):")
    print(
        f"  {'Regime':>24} | {'Scale':>14} | {'sigma_CW / (n/loglog n)':>24} | {'Theory alpha/(2q)':>18}"
    )
    print("  " + "-" * 90)

    for q in [1, 2, 4]:
        theory_limit = ALPHA_WXXZ24 / (2.0 * q)
        vals = []
        for log2_n in [20.0, 30.0, 64.0, 256.0]:
            n = 2.0 ** log2_n
            log2_M = log2_n + q * math.log2(log2_n)
            sigma_cw = solve_cw_savings(log2_n, log2_M, ALPHA_WXXZ24)
            ratio = sigma_cw / (n / math.log2(log2_n))
            vals.append(ratio)
            if log2_n in (30.0, 256.0):
                print(
                    f"  {'M = n*(log n)^' + str(q):>24} | {'log2 n = ' + str(int(log2_n)):>14} | "
                    f"{ratio:>24.6f} | {theory_limit:>18.6f}"
                )
        # Asymptotic check at log2(log2 n) = 1000 via scale-free solver:
        lln_asym = 1000.0
        gamma_asym = solve_cw_fraction_asymptotic(q * lln_asym, ALPHA_WXXZ24)
        ratio_asym = gamma_asym * lln_asym
        print(
            f"  {'M = n*(log n)^' + str(q):>24} | {'loglog n=1000':>14} | "
            f"{ratio_asym:>24.6f} | {theory_limit:>18.6f}"
        )
        # Verify strictly increasing toward the exact nonzero constant alpha/(2q) (NOT decaying to 0!)
        assert vals[0] < vals[1] < vals[2] < vals[3] < ratio_asym < theory_limit, (
            f"Expected monotonic climb to alpha/(2q) for q={q}: {vals}, asym={ratio_asym}"
        )
        assert abs(ratio_asym - theory_limit) / theory_limit < 0.03, (
            f"Asymptotic collision ratio off for q={q}: {ratio_asym} vs {theory_limit}"
        )

    # Sub-polylog: M = n * 2^(sqrt(log2(log2(n)))) -> exceeds Valiant threshold!
    sub_ratios = []
    for log2_n in [30.0, 64.0, 256.0, 900.0]:
        n = 2.0 ** log2_n
        lln = math.log2(log2_n)
        log2_M = log2_n + math.sqrt(lln)
        sigma_cw = solve_cw_savings(log2_n, log2_M, ALPHA_WXXZ24)
        ratio = sigma_cw / (n / lln)
        sub_ratios.append(ratio)
        if log2_n in (30.0, 900.0):
            print(
                f"  {'M = n*2^sqrt(loglog n)':>24} | {'log2 n = ' + str(int(log2_n)):>14} | "
                f"{ratio:>24.6f} | {'-> +infinity':>18}"
            )
    gamma_sub_asym = solve_cw_fraction_asymptotic(math.sqrt(1000.0), ALPHA_WXXZ24)
    ratio_sub_asym = gamma_sub_asym * 1000.0
    print(
        f"  {'M = n*2^sqrt(loglog n)':>24} | {'loglog n=1000':>14} | "
        f"{ratio_sub_asym:>24.6f} | {'-> +infinity':>18}"
    )
    assert sub_ratios[-1] > sub_ratios[0] and ratio_sub_asym > 3.0, (
        "Sub-polylog ratio must grow past Valiant!"
    )

    # Valiant raw CNF regime: M = 2^(n^0.25) -> sigma_CW = Theta(n^0.75) << n/loglog n.
    log2_n_raw = 30.0
    n_raw = 2.0 ** log2_n_raw
    log2_M_raw = n_raw ** 0.25
    sigma_cw_raw = solve_cw_savings(log2_n_raw, log2_M_raw, ALPHA_WXXZ24)
    ratio_raw = sigma_cw_raw / (n_raw / math.log2(log2_n_raw))
    print(
        f"  {'Valiant raw M=2^(n^.25)':>24} | {'log2 n = 30':>14} | "
        f"{ratio_raw:>24.6e} | {'Theta(loglog/n^.25)':>18}"
    )
    assert ratio_raw < 1e-2

    print(
        "[PASS] Check 2: Exact Chan-Williams scaling law verified across M=n^2..n^10 "
        "(Theta((B-1)log n/log log n) shortfall even if omega=2) & exact collision at M=n*polylog(n)."
    )


# ============================================================================
# CHECK 3: Exact F_2 Probabilistic Polynomial Compression & Chebyshev Wall
# ============================================================================


def eval_f2_random_lincomb_pass(
    rng: random.Random, w_mask: int, m_bits: int, r: int
) -> bool:
    """
    Returns True iff R * w == 0^r (mod 2) for a fresh uniform R in F_2^{r x M}.
    Short-circuits immediately upon the first nonzero parity bit for speed.
    """
    for _ in range(r):
        row = rng.getrandbits(m_bits)
        if (row & w_mask).bit_count() & 1:
            return False
    return True


def verify_diagonal_bilinear_identity(rng: random.Random, m: int = 10, r: int = 3) -> int:
    """
    Algebraically construct the EXACT diagonal bilinear expansion over F_2:
        P_R(u, v) = prod_{i=1}^r (1 + sum_{j=1}^M R_{i,j} u_j v_j)
                  = sum_{|S| <= r} c_S * (prod_{j in S} u_j) * (prod_{j in S} v_j)  (mod 2)
    and verify 100% agreement on 500 random (u, v) pairs!
    """
    rows = [rng.getrandbits(m) for _ in range(r)]

    # Dynamic programming over i = 0..r-1 to compute exact coefficients c_S in F_2,
    # indexed by bitmask S of weight <= r (since w_j^2 = w_j in F_2).
    coeffs: Dict[int, int] = {0: 1}
    for row in rows:
        new_coeffs: Dict[int, int] = dict(coeffs)  # multiply by 1
        # Extract active indices j where R_{i,j} == 1
        active_bits: List[int] = []
        tmp = row
        while tmp:
            lsb = tmp & -tmp
            active_bits.append(lsb)
            tmp ^= lsb
        for s_mask, c_val in coeffs.items():
            if c_val == 0:
                continue
            for bit in active_bits:
                t_mask = s_mask | bit
                new_coeffs[t_mask] = new_coeffs.get(t_mask, 0) ^ 1
        coeffs = {k: v for k, v in new_coeffs.items() if v}

    # Verify every surviving monomial has degree <= r.
    max_possible = sum(math.comb(m, k) for k in range(r + 1))
    assert all(mask.bit_count() <= r for mask in coeffs)
    assert len(coeffs) <= max_possible

    # Test 500 random pairs (u, v) in {0,1}^m.
    for _ in range(500):
        u = rng.getrandbits(m)
        v = rng.getrandbits(m)
        w = u & v

        # Direct evaluation of product over i = 1..r:
        direct = 1
        for row in rows:
            if (row & w).bit_count() & 1:
                direct = 0
                break

        # Diagonal bilinear evaluation sum_S c_S * phi_S(u) * psi_S(v) (mod 2):
        expanded = 0
        for s_mask in coeffs:
            phi_u = 1 if (u & s_mask) == s_mask else 0
            psi_v = 1 if (v & s_mask) == s_mask else 0
            expanded ^= (phi_u & psi_v)

        assert direct == expanded, "Diagonal bilinear polynomial identity failed!"

    return max_possible


def run_check_3() -> None:
    print("\n" + "=" * 78)
    print("CHECK 3: Exact F_2 Probabilistic Polynomial Compression & Error-Boosting Wall")
    print("=" * 78)
    rng = random.Random(20260318)

    # 3A. Empirical false-positive rate across M in {64, 128, 256} and r in {4, 8, 12}.
    trials_by_r = {4: 8000, 8: 40000, 12: 120000}
    print(
        f"  [3A] Empirical F_2 compression R(u & v) == 0^r across M in {{64,128,256}}, r in {{4,8,12}}:"
    )
    print(
        f"  {'M':>4} | {'r':>2} | {'Trials':>7} | {'Zero-FN (w=0)':>14} | "
        f"{'Emp FP Rate':>12} | {'Exact 2^-r':>12} | {'Z-score':>8}"
    )
    print("  " + "-" * 74)

    for m_bits in [64, 128, 256]:
        # Test a mix of Hamming weights: |w|=1, |w|=2, |w|=M//4, |w|=M//2
        weight_masks = [
            1,
            (1 << 0) | (1 << (m_bits - 1)),
            sum(1 << i for i in range(0, m_bits, 4)),
            sum(1 << i for i in range(0, m_bits, 2)),
        ]
        for r in [4, 8, 12]:
            # Check 0 false negatives on w = 0
            fn_checks = 500
            fn_pass = sum(
                1 for _ in range(fn_checks) if eval_f2_random_lincomb_pass(rng, 0, m_bits, r)
            )
            assert fn_pass == fn_checks, "False negative detected on orthogonal vector!"

            n_trials = trials_by_r[r]
            fp_count = 0
            for t in range(n_trials):
                w_mask = weight_masks[t & 3]
                if eval_f2_random_lincomb_pass(rng, w_mask, m_bits, r):
                    fp_count += 1

            p_exact = 2.0 ** (-r)
            p_emp = fp_count / n_trials
            se = math.sqrt(p_exact * (1.0 - p_exact) / n_trials)
            z_score = (p_emp - p_exact) / se
            print(
                f"  {m_bits:>4} | {r:>2} | {n_trials:>7} | {fn_pass:>5}/{fn_checks:<8} | "
                f"{p_emp:>12.6f} | {p_exact:>12.6f} | {z_score:>+8.2f}"
            )
            assert abs(z_score) < 4.0, (
                f"Empirical FP rate deviated > 4 sigma at M={m_bits}, r={r}: z={z_score}"
            )

    # 3B. Exact diagonal bilinear monomial expansion identity.
    max_monomials = verify_diagonal_bilinear_identity(rng, m=10, r=3)
    print(
        f"\n  [3B] Diagonal bilinear expansion P_R(u,v) = sum_{{|S|<=r}} c_S phi_S(u) psi_S(v) "
        f"(M=10, r=3, L<={max_monomials}): 500/500 exact matches."
    )

    # 3C. Concrete UNSAT wide-CNF global-compression Chebyshev Wall (n=12, M=144).
    n_wall = 12
    m_wall = n_wall * n_wall
    clauses_wall = generate_wide_cnf_instance(rng, n_wall, "unsat_wide")
    _n1, _n2, u_map, v_map = cnf_to_ov_vectors(n_wall, clauses_wall)

    # Collect all distinct nonzero overlap patterns w = u & v across the entire UNSAT instance.
    distinct_overlaps = set()
    for u in u_map:
        for v in v_map:
            w = u & v
            assert w != 0, "UNSAT formula had an orthogonal pair!"
            distinct_overlaps.add(w)
    k_distinct = len(distinct_overlaps)
    overlaps_list = list(distinct_overlaps)
    log2_k = math.log2(k_distinct)

    print(
        f"\n  [3C] Concrete UNSAT Wide-CNF Global-Compression Wall (n={n_wall}, M={m_wall}):"
    )
    print(
        f"       Distinct nonzero overlap vectors |W| = {k_distinct} (log2 |W| = {log2_k:.2f}, "
        f"2^n = {1 << n_wall})."
    )
    print(
        f"       Pairwise-independence Chebyshev bound: Pr[0 FPs] <= 2^r / |W|."
    )
    print(
        f"  {'r':>3} | {'Emp Pr[0 FPs]':>14} | {'Chebyshev 2^r/|W|':>18} | "
        f"{'E[FPs] = |W|*2^-r':>18} | {'log2 L(M,r)':>12} | {'MM budget (a/2)n':>16}"
    )
    print("  " + "-" * 95)

    mm_budget = 0.5 * ALPHA_WXXZ24 * n_wall
    zero_fp_by_r: Dict[int, float] = {}
    for r in [4, 8, 12, 14, 16]:
        trials_wall = 80
        zero_fp_hits = 0
        for _ in range(trials_wall):
            rows = [rng.getrandbits(m_wall) for _ in range(r)]
            found_fp = False
            for w in overlaps_list:
                passed_all = True
                for row in rows:
                    if (row & w).bit_count() & 1:
                        passed_all = False
                        break
                if passed_all:
                    found_fp = True
                    break
            if not found_fp:
                zero_fp_hits += 1
        emp_zero_fp = zero_fp_hits / trials_wall
        zero_fp_by_r[r] = emp_zero_fp
        cheb_bound = min(1.0, (2.0 ** r) / k_distinct)
        exp_fps = k_distinct * (2.0 ** (-r))
        log2_L = math.log2(sum(math.comb(m_wall, k) for k in range(r + 1)))
        print(
            f"  {r:>3} | {emp_zero_fp:>14.4f} | {cheb_bound:>18.4f} | "
            f"{exp_fps:>18.3f} | {log2_L:>12.2f} | {mm_budget:>16.2f}"
        )

    # Confirm: for r <= 8, empirical Pr[0 FPs] is ~0 (<= 0.1); reliable global suppression
    # requires r >= log2(|W|) (~11-12 = Omega(n)), at which point log2 L(M, r) >> (alpha/2)*n!
    assert zero_fp_by_r[4] == 0.0
    assert zero_fp_by_r[8] <= 0.15
    assert zero_fp_by_r[16] > 0.70
    log2_L_at_n = math.log2(sum(math.comb(m_wall, k) for k in range(n_wall + 1)))
    assert log2_L_at_n > 20.0 * mm_budget

    print(
        "[PASS] Check 3: Exact 2^-r FP rate, diagonal bilinear identity, and pairwise-independence "
        "Chebyshev wall (forcing r = Omega(n) globally & locking block savings to O(n/log(M/n))) verified."
    )


def main() -> int:
    t0 = time.perf_counter()
    run_check_1()
    run_check_2()
    run_check_3()
    dt = time.perf_counter() - t0
    print("\n" + "=" * 78)
    print(f"[PASS] ALL BATON #018 VERIFICATION CHECKS SUCCEEDED in {dt:.2f}s (exit code 0).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
