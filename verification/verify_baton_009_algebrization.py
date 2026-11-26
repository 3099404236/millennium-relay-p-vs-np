#!/usr/bin/env python3
"""
Verification Suite for Baton #009:
Aaronson-Wigderson (2009) Algebrization Barrier & Executable Arithmetization / Sumcheck Audit.

Pure Python 3.12 standard library verification covering three core pillars:
1. Exact Multilinear Low-Degree Extension (MLE / LDE) over prime fields F_q (q = 101, 257):
   - Lagrange basis evaluation vs. exact Mobius-inverted monomial expansion.
   - Exact Boolean hypercube agreement on {0,1}^n.
   - Exhaustive verification of individual degree <= 1 (vanishing second finite difference).
2. Full Interactive Sumcheck Protocol (Verifier + Honest Prover + Naive & Optimal Cheating Provers):
   - Tested for n = 4, 5 variables over F_101 and F_257 with degrees d = 1, 2, 3
     (including d = 2 arithmetized witness-intersection polynomials g(x) = A~(x) * B~(x)).
   - Verifies 100% completeness for the honest prover.
   - Verifies Schwartz-Zippel soundness both deterministically (exact root counting over all
     q challenges per round, proving optimal catch probability (1 - d/q)^n >= 1 - n*d/q)
     and empirically via Monte Carlo interactive runs.
3. Finite-Field Algebraic-Oracle Consistency & Aaronson-Wigderson Barrier Mechanics:
   - Part A: Demonstrates why naive Baker-Gill-Solovay diagonalization breaks against A~
     (a single random F_q query catches a weight-1 Boolean perturbation with prob >= 1 - n/q).
   - Part B: Demonstrates AW09's separating mechanism (NP^A not in BPP^{A~}) via Set Disjointness:
     verifies exact bilinear Alice-Bob split A~(x_0, x') = (1 - x_0)*X~(x') + x_0*Y~(x')
     and explicitly constructs sparse Boolean oracle pairs (A^(0) disjoint, A^(1) intersecting)
     whose MLEs agree identically on all T non-Boolean field queries over F_101 (T=3) and F_257 (T=2).
   - Part C: Demonstrates AW09's collapsing mechanism (NP^{A~} <= P^A <= P^{A~} for A = TQBF):
     verifies streaming O(n + log q)-space evaluation of the MLE of a parameterized QBF oracle
     matches the full-table MLE identically over F_101 and F_257.
"""

from __future__ import annotations

import itertools
import random
from typing import Callable, List, Sequence, Tuple


# ---------------------------------------------------------------------------
# Finite Field F_q Utilities (q prime)
# ---------------------------------------------------------------------------

def mod_inv(a: int, q: int) -> int:
    a %= q
    if a == 0:
        raise ZeroDivisionError(f"Zero has no inverse mod {q}")
    return pow(a, q - 2, q)


def poly_eval(coeffs: Sequence[int], x: int, q: int) -> int:
    """Evaluate sum_k coeffs[k] * x^k mod q via Horner's method."""
    acc = 0
    for c in reversed(coeffs):
        acc = (acc * x + c) % q
    return acc


def lagrange_interpolate_univariate(points: Sequence[Tuple[int, int]], q: int) -> List[int]:
    """
    Given d+1 points (x_k, y_k) with distinct x_k in F_q, return the exact
    monomial coefficients [a_0, a_1, ..., a_d] of the unique degree <= d
    interpolating polynomial over F_q.
    """
    m = len(points)
    result = [0] * m
    for i in range(m):
        xi, yi = points[i]
        # Build numerator polynomial prod_{j != i} (X - x_j) and denominator prod_{j != i} (x_i - x_j)
        basis = [1]
        denom = 1
        for j in range(m):
            if i == j:
                continue
            xj = points[j][0]
            denom = (denom * (xi - xj)) % q
            # Multiply basis by (X - x_j)
            new_basis = [0] * (len(basis) + 1)
            for k, coeff in enumerate(basis):
                new_basis[k] = (new_basis[k] - coeff * xj) % q
                new_basis[k + 1] = (new_basis[k + 1] + coeff) % q
            basis = new_basis
        scale = (yi * mod_inv(denom, q)) % q
        for k, coeff in enumerate(basis):
            result[k] = (result[k] + coeff * scale) % q
    return result


# ---------------------------------------------------------------------------
# Pillar 1: Exact Multilinear Extension (MLE / LDE) over F_q
# ---------------------------------------------------------------------------

def int_to_bits(idx: int, n: int) -> Tuple[int, ...]:
    return tuple((idx >> (n - 1 - i)) & 1 for i in range(n))


def bits_to_int(bits: Sequence[int]) -> int:
    val = 0
    for b in bits:
        val = (val << 1) | (b & 1)
    return val


def chi_basis(w_bits: Sequence[int], x: Sequence[int], q: int) -> int:
    """Lagrange multilinear indicator chi_w(x) = prod_i (w_i*x_i + (1-w_i)*(1-x_i)) mod q."""
    prod = 1
    for wi, xi in zip(w_bits, x):
        term = xi if wi == 1 else (1 - xi)
        prod = (prod * term) % q
    return prod


def mle_eval_lagrange(table: Sequence[int], x: Sequence[int], q: int) -> int:
    """
    Exact multilinear extension evaluated via Lagrange interpolation over {0,1}^n:
      A~(x) = sum_{w in {0,1}^n} A(w) * chi_w(x) mod q.
    Also serves as an O(n + log q)-space streaming evaluator when A(w) is computed on the fly.
    """
    n = len(x)
    assert len(table) == (1 << n)
    # Precompute 1D factor pairs [(1 - x_i) mod q, x_i mod q] for fast evaluation
    factors = [((1 - xi) % q, xi % q) for xi in x]

    # Iterative folding computes the exact sum sum_w A(w) chi_w(x) mod q in O(2^n) field ops
    layer = [val % q for val in table]
    for i in range(n - 1, -1, -1):
        f0, f1 = factors[i]
        next_layer = []
        for j in range(0, len(layer), 2):
            next_layer.append((layer[j] * f0 + layer[j + 1] * f1) % q)
        layer = next_layer
    return layer[0]


def mle_eval_direct_sum(oracle_fn: Callable[[Tuple[int, ...]], int], n: int, x: Sequence[int], q: int) -> int:
    """
    Streaming O(n + log q)-space evaluator of A~(x) that never materializes the 2^n table:
    loops over w in {0,1}^n, queries oracle_fn(w), multiplies by chi_w(x), and accumulates mod q.
    """
    total = 0
    for idx in range(1 << n):
        w = int_to_bits(idx, n)
        aw = oracle_fn(w) % q
        if aw:
            total = (total + aw * chi_basis(w, x, q)) % q
    return total


def mle_monomial_coeffs(table: Sequence[int], n: int, q: int) -> List[int]:
    """
    Compute exact multilinear monomial coefficients c_S over F_q such that
      A~(x_0, ..., x_{n-1}) = sum_{S subseteq [n]} c_S * prod_{i in S} x_i mod q
    using Mobius inversion on the Boolean lattice.
    Note: bit (n - 1 - i) of mask S corresponds to variable x_i.
    """
    assert len(table) == (1 << n)
    coeffs = [val % q for val in table]
    for bit in range(n):
        step = 1 << bit
        for mask in range(1 << n):
            if mask & step:
                coeffs[mask] = (coeffs[mask] - coeffs[mask ^ step]) % q
    return coeffs


def mle_eval_monomials(coeffs: Sequence[int], x: Sequence[int], q: int) -> int:
    """Evaluate sum_S c_S * prod_{i in S} x_i mod q directly from monomial coefficients."""
    n = len(x)
    # Build product of x_i for every subset mask S in O(2^n)
    monomial_vals = [1] * (1 << n)
    for bit in range(n):
        xi = x[n - 1 - bit] % q
        step = 1 << bit
        for mask in range(step):
            monomial_vals[mask | step] = (monomial_vals[mask] * xi) % q
    total = 0
    for c, mv in zip(coeffs, monomial_vals):
        if c:
            total = (total + c * mv) % q
    return total


def test_multilinear_extension() -> None:
    rng = random.Random(2026009)
    primes = (101, 257)
    checks_total = 0

    for q in primes:
        for n in (3, 4, 5):
            N = 1 << n
            # Test a diverse suite of Boolean oracle tables: random, parity, majority, point, all-ones
            oracles = [
                [rng.randint(0, 1) for _ in range(N)],
                [bin(i).count("1") & 1 for i in range(N)],
                [1 if bin(i).count("1") > n // 2 else 0 for i in range(N)],
                [1 if i == (N // 3) else 0 for i in range(N)],
                [1] * N,
            ]
            for table in oracles:
                coeffs = mle_monomial_coeffs(table, n, q)

                # 1. Exact agreement on the entire Boolean hypercube {0,1}^n
                for idx in range(N):
                    w = int_to_bits(idx, n)
                    val_lag = mle_eval_lagrange(table, w, q)
                    val_mon = mle_eval_monomials(coeffs, w, q)
                    assert val_lag == table[idx], f"Lagrange MLE mismatch on Boolean input {w}"
                    assert val_mon == table[idx], f"Monomial MLE mismatch on Boolean input {w}"

                # 2. Exact identity between Lagrange form, Monomial form, and streaming sum on F_q^n
                for _ in range(40):
                    pt = [rng.randrange(q) for _ in range(n)]
                    v_lag = mle_eval_lagrange(table, pt, q)
                    v_mon = mle_eval_monomials(coeffs, pt, q)
                    assert v_lag == v_mon, f"Lagrange != Monomial at {pt} mod {q}"
                # Also check streaming sum on 5 random points
                for _ in range(5):
                    pt = [rng.randrange(q) for _ in range(n)]
                    v_stream = mle_eval_direct_sum(lambda w, t=table: t[bits_to_int(w)], n, pt, q)
                    assert v_stream == mle_eval_lagrange(table, pt, q)

                # 3. Individual degree <= 1 verification:
                # Over prime field F_q (q > 2), f(t) has degree <= 1 iff f(t+2) - 2f(t+1) + f(t) == 0 for all t in F_q.
                base_pt = [rng.randrange(q) for _ in range(n)]
                for var in range(n):
                    line_vals = []
                    for t in range(q):
                        pt = list(base_pt)
                        pt[var] = t
                        line_vals.append(mle_eval_lagrange(table, pt, q))
                    for t in range(q):
                        second_diff = (line_vals[(t + 2) % q] - 2 * line_vals[(t + 1) % q] + line_vals[t]) % q
                        assert second_diff == 0, f"Individual degree > 1 detected in var {var} mod {q}"
                checks_total += 1

    print(
        f"[PASS] Exact Multilinear Low-Degree Extension verified across {checks_total} Boolean oracles "
        f"(n in {{3,4,5}}, q in {{101,257}}): 100% agreement on {{0,1}}^n, Lagrange==Monomial==Streaming, "
        f"and exact individual degree <= 1 (vanishing 2nd finite difference over all F_q)."
    )


# ---------------------------------------------------------------------------
# Pillar 2: Full Interactive Sumcheck Protocol (Honest + Cheating Provers)
# ---------------------------------------------------------------------------

class ProductOfMLEs:
    """
    Arithmetized multivariate polynomial g(x) = prod_{k=1}^d A_k~(x) mod q
    of individual degree <= d in each of n variables.
    Notice: For d = 2, sum_{w in {0,1}^n} g(w) counts the exact Boolean witness intersection
    |{w in {0,1}^n : A_1(w) = 1 and A_2(w) = 1}| mod q!
    """

    def __init__(self, tables: Sequence[Sequence[int]], n: int, q: int) -> None:
        self.tables = [list(t) for t in tables]
        self.n = n
        self.q = q
        self.d = len(tables)
        assert all(len(t) == (1 << n) for t in self.tables)

    def eval(self, x: Sequence[int]) -> int:
        prod = 1
        for table in self.tables:
            prod = (prod * mle_eval_lagrange(table, x, self.q)) % self.q
        return prod

    def true_hypercube_sum(self) -> int:
        total = 0
        for idx in range(1 << self.n):
            p = 1
            for table in self.tables:
                p *= table[idx]
            total = (total + p) % self.q
        return total

    def round_poly_from_folded(self, folded_tables: Sequence[Sequence[int]]) -> List[int]:
        """
        Given tables already folded on prefix (r_0, ..., r_{i-1}), compute exact univariate
        polynomial s_i(X) = sum_{b in {0,1}^{n-1-i}} g(r_{<i}, X, b) mod q
        as monomial coefficients [a_0, ..., a_d] via evaluation at X = 0, 1, ..., d.
        """
        half = len(folded_tables[0]) // 2
        q = self.q
        points: List[Tuple[int, int]] = []
        for x_val in range(self.d + 1):
            f0 = (1 - x_val) % q
            f1 = x_val % q
            acc = 0
            for j in range(half):
                p = 1
                for tbl in folded_tables:
                    val = (tbl[j] * f0 + tbl[j + half] * f1) % q
                    p = (p * val) % q
                acc = (acc + p) % q
            points.append((x_val, acc))
        return lagrange_interpolate_univariate(points, q)

    def honest_round_poly(self, prefix: Sequence[int]) -> List[int]:
        """Convenience wrapper folding from scratch along prefix."""
        folded = []
        for table in self.tables:
            cur = [v % self.q for v in table]
            for coord in prefix:
                half = len(cur) // 2
                f0 = (1 - coord) % self.q
                f1 = coord % self.q
                cur = [(cur[j] * f0 + cur[j + half] * f1) % self.q for j in range(half)]
            folded.append(cur)
        return self.round_poly_from_folded(folded)


def run_sumcheck_session(
    poly: ProductOfMLEs,
    claimed_sum: int,
    prover_mode: str,
    rng: random.Random,
) -> bool:
    """
    Execute a full n-round interactive Sumcheck protocol between Verifier and Prover.
    prover_mode:
      - 'honest': sends true s_i(X) every round.
      - 'naive_cheater': if current claim C_i != true_sum_i, adds constant offset (C_i - true_sum_i)/2
        to s_i(X) (which has 0 roots and cannot get lucky!).
      - 'optimal_cheater': if current claim C_i != true_sum_i, crafts degree-d perturbation Delta(X)
        with d distinct roots in F_q and Delta(0)+Delta(1) = C_i - true_sum_i, achieving the exact
        Schwartz-Zippel maximum round-fooling probability d/q! If lucky on any round (C_i == true_sum_i),
        switches to honest play for all remaining rounds.
    """
    q = poly.q
    d = poly.d
    n = poly.n
    target = claimed_sum % q
    challenges: List[int] = []
    folded_tables = [[v % q for v in t] for t in poly.tables]

    for rnd in range(n):
        true_poly = poly.round_poly_from_folded(folded_tables)
        true_sum_i = (poly_eval(true_poly, 0, q) + poly_eval(true_poly, 1, q)) % q

        if prover_mode == "honest" or target == true_sum_i:
            sent_poly = true_poly
        elif prover_mode == "naive_cheater":
            delta = (target - true_sum_i) % q
            half_inv = (delta * mod_inv(2, q)) % q
            sent_poly = list(true_poly)
            sent_poly[0] = (sent_poly[0] + half_inv) % q
        elif prover_mode == "optimal_cheater":
            delta = (target - true_sum_i) % q
            roots = list(range(2, 2 + d))
            while True:
                p0 = 1
                p1 = 1
                for a in roots:
                    p0 = (p0 * (-a)) % q
                    p1 = (p1 * (1 - a)) % q
                denom = (p0 + p1) % q
                if denom != 0:
                    break
                roots[-1] = (roots[-1] + 1) % q
                while roots[-1] in roots[:-1]:
                    roots[-1] = (roots[-1] + 1) % q
            scale = (delta * mod_inv(denom, q)) % q
            delta_poly = [scale]
            for a in roots:
                nxt = [0] * (len(delta_poly) + 1)
                for k, c in enumerate(delta_poly):
                    nxt[k] = (nxt[k] - c * a) % q
                    nxt[k + 1] = (nxt[k + 1] + c) % q
                delta_poly = nxt
            sent_poly = [(true_poly[k] + delta_poly[k]) % q for k in range(d + 1)]
        else:
            raise ValueError(f"Unknown prover_mode: {prover_mode}")

        # Verifier checks degree <= d and s_i(0) + s_i(1) == target (mod q)
        if len(sent_poly) > d + 1:
            return False
        s0 = poly_eval(sent_poly, 0, q)
        s1 = poly_eval(sent_poly, 1, q)
        if (s0 + s1) % q != target:
            return False

        # Verifier sends uniform random challenge r_i in F_q
        r_i = rng.randrange(q)
        challenges.append(r_i)
        target = poly_eval(sent_poly, r_i, q)

        # Incrementally fold prover tables along r_i
        half = len(folded_tables[0]) // 2
        f0 = (1 - r_i) % q
        f1 = r_i % q
        folded_tables = [
            [(tbl[j] * f0 + tbl[j + half] * f1) % q for j in range(half)]
            for tbl in folded_tables
        ]

    # Final oracle check: verifier evaluates g(r_0, ..., r_{n-1}) directly via algebraic oracle
    oracle_val = poly.eval(challenges)
    return target == oracle_val


def verify_exact_all_rounds_sz_bound(poly: ProductOfMLEs, rng: random.Random) -> None:
    """
    Deterministic proof on the finite instance that in EVERY round i in {0, ..., n-1},
    the optimal degree-d cheating polynomial agrees with the true round polynomial on
    EXACTLY d points out of all q points in F_q.
    Hence across n independent rounds, exact soundness error is 1 - (1 - d/q)^n <= n*d/q,
    and catch probability is (1 - d/q)^n >= 1 - n*d/q.
    """
    q = poly.q
    d = poly.d
    prefix: List[int] = []
    for _ in range(poly.n):
        true_poly = poly.honest_round_poly(prefix)
        true_sum = (poly_eval(true_poly, 0, q) + poly_eval(true_poly, 1, q)) % q
        false_sum = (true_sum + 1) % q
        delta = (false_sum - true_sum) % q  # == 1

        roots = list(range(2, 2 + d))
        while True:
            p0 = 1
            p1 = 1
            for a in roots:
                p0 = (p0 * (-a)) % q
                p1 = (p1 * (1 - a)) % q
            denom = (p0 + p1) % q
            if denom != 0:
                break
            roots[-1] = (roots[-1] + 1) % q
            while roots[-1] in roots[:-1]:
                roots[-1] = (roots[-1] + 1) % q
        scale = (delta * mod_inv(denom, q)) % q
        delta_poly = [scale]
        for a in roots:
            nxt = [0] * (len(delta_poly) + 1)
            for k, c in enumerate(delta_poly):
                nxt[k] = (nxt[k] - c * a) % q
                nxt[k + 1] = (nxt[k + 1] + c) % q
            delta_poly = nxt
        cheat_poly = [(true_poly[k] + delta_poly[k]) % q for k in range(d + 1)]

        # Verify sum check passes for the cheater
        assert (poly_eval(cheat_poly, 0, q) + poly_eval(cheat_poly, 1, q)) % q == false_sum
        # Exhaustively count collisions across ALL q elements of F_q
        collisions = sum(
            1 for r in range(q) if poly_eval(cheat_poly, r, q) == poly_eval(true_poly, r, q)
        )
        assert collisions == d, f"Expected exact d={d} collisions, got {collisions}"
        prefix.append(rng.randrange(q))


def test_sumcheck_protocol() -> None:
    rng = random.Random(20260009)
    configs = [
        (4, 1, 101),  # n=4, multilinear d=1, q=101
        (4, 2, 101),  # n=4, intersection product d=2, q=101
        (5, 2, 101),  # n=5, intersection product d=2, q=101
        (5, 2, 257),  # n=5, intersection product d=2, q=257
        (4, 3, 257),  # n=4, triple product d=3, q=257
    ]

    honest_trials = 100
    cheat_trials = 2000

    for n, d, q in configs:
        N = 1 << n
        tables = [[rng.randint(0, 1) for _ in range(N)] for _ in range(d)]
        poly = ProductOfMLEs(tables, n, q)
        H_true = poly.true_hypercube_sum()
        H_false = (H_true + rng.randrange(1, q)) % q

        # 1. Completeness: 100% pass for honest prover
        honest_passes = sum(
            1 for _ in range(honest_trials)
            if run_sumcheck_session(poly, H_true, "honest", rng)
        )
        assert honest_passes == honest_trials, f"Honest prover failed for {(n, d, q)}"

        # 2. Exact deterministic all-rounds Schwartz-Zippel root audit
        verify_exact_all_rounds_sz_bound(poly, rng)
        exact_catch_prob = (1.0 - d / q) ** n
        sz_lower_bound = 1.0 - (n * d) / q
        assert exact_catch_prob >= sz_lower_bound - 1e-12

        # 3. Naive cheater (constant shift) must be caught 100% of the time
        naive_caught = sum(
            1 for _ in range(100)
            if not run_sumcheck_session(poly, H_false, "naive_cheater", rng)
        )
        assert naive_caught == 100, f"Naive cheater somehow fooled verifier on {(n, d, q)}"

        # 4. Optimal d-root adaptive cheater: empirical catch rate matches (1 - d/q)^n >= 1 - nd/q
        opt_caught = sum(
            1 for _ in range(cheat_trials)
            if not run_sumcheck_session(poly, H_false, "optimal_cheater", rng)
        )
        emp_catch = opt_caught / cheat_trials
        # 4-sigma binomial tolerance around exact_catch_prob
        sigma = ((exact_catch_prob * (1.0 - exact_catch_prob)) / cheat_trials) ** 0.5
        assert abs(emp_catch - exact_catch_prob) <= 4.0 * sigma + 0.01, (
            f"Empirical catch {emp_catch:.4f} deviated from exact {exact_catch_prob:.4f}"
        )

        print(
            f"[PASS] Sumcheck (n={n}, d={d}, q={q}): honest={honest_passes}/{honest_trials} (100%), "
            f"naive_caught=100/100, opt_cheater_caught={opt_caught}/{cheat_trials} ({emp_catch:.4f}), "
            f"exact=(1-d/q)^n={exact_catch_prob:.4f} >= SZ bound 1-nd/q={sz_lower_bound:.4f}."
        )


# ---------------------------------------------------------------------------
# Pillar 3: Algebraic-Oracle Consistency & Aaronson-Wigderson Barrier Mechanics
# ---------------------------------------------------------------------------

def test_part_a_bgs_breaks_against_mle() -> None:
    """
    Show why Baker-Gill-Solovay diagonalization breaks under algebraic extension A~:
    On {0,1}^5 (size 32), flipping a SINGLE Boolean entry (A_0 == 0 vs A_1 == 1_{w*})
    is caught by a random Boolean query with prob 1/32 = 3.125%,
    yet caught by a SINGLE random algebraic query A~(r) over F_101 with exact prob
    (100/101)^5 = 95.146% >= 1 - 5/101 = 95.050%.
    """
    rng = random.Random(2026101)
    n = 5
    q = 101
    N = 1 << n
    w_star = 19  # single flipped Boolean entry
    A0 = [0] * N
    A1 = [1 if i == w_star else 0 for i in range(N)]

    trials = 2000
    bool_hits = 0
    alg_hits = 0
    for _ in range(trials):
        w_rand = rng.randrange(N)
        if A0[w_rand] != A1[w_rand]:
            bool_hits += 1
        r_rand = [rng.randrange(q) for _ in range(n)]
        if mle_eval_lagrange(A0, r_rand, q) != mle_eval_lagrange(A1, r_rand, q):
            alg_hits += 1

    bool_rate = bool_hits / trials
    alg_rate = alg_hits / trials
    exact_alg_rate = ((q - 1) / q) ** n
    sz_bound = 1.0 - n / q
    assert bool_rate < 0.10
    assert alg_rate > 0.93
    assert exact_alg_rate >= sz_bound

    print(
        f"[PASS] AW09 Part A (Why BGS Breaks under A~): weight-1 flip on {{0,1}}^{n} detected by "
        f"1 Boolean query at rate {bool_rate:.4f} (exact 1/32=0.0312), vs 1 algebraic query over F_{q} "
        f"at rate {alg_rate:.4f} (exact {exact_alg_rate:.4f} >= 1-n/q={sz_bound:.4f})."
    )


def test_part_b_aw09_disjointness_and_hiding() -> None:
    """
    Demonstrates the core Aaronson-Wigderson separating mechanism (NP^A not in BPP^{A~}):
    1. Exact bilinear decomposition for Set Disjointness oracle A(0, w) = X(w), A(1, w) = Y(w):
         A~(x_0, x') = (1 - x_0)*X~(x') + x_0*Y~(x') mod q,
       proving every algebraic query costs Alice & Bob only O(log q) bits of communication.
    2. Explicit finite-field algebraic-oracle collision construction:
       Against arbitrary non-Boolean algebraic query points r^(1), ..., r^(T) in F_q^5,
       explicitly construct SPARSE Boolean oracles A^(0) (DISJOINT, L_A = 0) and
       A^(1) (INTERSECTING, L_A = 1) whose low-degree extensions A~^(0) and A~^(1)
       return 100% IDENTICAL answers on ALL T algebraic queries!
    """
    rng = random.Random(2026257)
    n = 5
    half_n = n - 1
    N_half = 1 << half_n  # 16 coordinates for Alice X and 16 for Bob Y

    # 1. Verify exact Alice-Bob bilinear communication decomposition over F_101 and F_257
    for q in (101, 257):
        X = [rng.randint(0, 1) for _ in range(N_half)]
        Y = [rng.randint(0, 1) for _ in range(N_half)]
        A = X + Y  # MSB x_0 = 0 -> X, MSB x_0 = 1 -> Y
        for _ in range(100):
            x0 = rng.randrange(q)
            x_rest = [rng.randrange(q) for _ in range(half_n)]
            lhs = mle_eval_lagrange(A, [x0, *x_rest], q)
            rhs = ((1 - x0) * mle_eval_lagrange(X, x_rest, q) + x0 * mle_eval_lagrange(Y, x_rest, q)) % q
            assert lhs == rhs, f"Bilinear split failed mod {q}"

    # 2. Construct explicit sparse colliding pairs (A^(0) disjoint, A^(1) intersecting)
    #    matching identically on T non-Boolean queries over F_101 (T=3) and F_257 (T=2).
    for q, T in ((101, 3), (257, 2)):
        # Pick T genuinely non-Boolean algebraic query points in (F_q \ {0, 1})^n
        queries = [[rng.randrange(2, q) for _ in range(n)] for _ in range(T)]

        # Precompute evaluation column vectors chi_w(r^(j)) for every w in {0,1}^n
        chi_cols = [
            tuple(chi_basis(int_to_bits(w, n), r, q) for r in queries)
            for w in range(1 << n)
        ]

        def eval_signature(active_indices: Sequence[int]) -> Tuple[int, ...]:
            sig = [0] * T
            for w in active_indices:
                col = chi_cols[w]
                for j in range(T):
                    sig[j] = (sig[j] + col[j]) % q
            return tuple(sig)

        # Sample sparse DISJOINT tables (weight 4..6 out of 32: never have both w and w + 16 active)
        disjoint_buckets: dict[Tuple[int, ...], List[int]] = {}
        max_samples = 25000
        for _ in range(max_samples):
            weight = rng.randint(4, 6)
            coords = rng.sample(range(N_half), weight)
            # For each chosen coordinate c, place the 1 either in Alice (c) or Bob (c + 16), never both
            active = [c if rng.randint(0, 1) == 0 else c + N_half for c in coords]
            sig = eval_signature(active)
            if sig not in disjoint_buckets:
                disjoint_buckets[sig] = active
            if len(disjoint_buckets) >= 6000:
                break

        # Now find a sparse INTERSECTING table (weight 4..6, with >= 1 shared coordinate c & c+16)
        # that collides identically on ALL T algebraic field queries!
        found_pair = None
        for _ in range(max_samples * 4):
            shared = rng.randrange(N_half)
            extra_weight = rng.randint(2, 4)
            others = rng.sample([c for c in range(N_half) if c != shared], extra_weight)
            active = [shared, shared + N_half] + [
                c if rng.randint(0, 1) == 0 else c + N_half for c in others
            ]
            sig = eval_signature(active)
            if sig in disjoint_buckets:
                found_pair = (disjoint_buckets[sig], active, sig)
                break

        assert found_pair is not None, f"Failed to find colliding sparse pair for q={q}, T={T}"
        act0, act1, shared_sig = found_pair

        A0 = [1 if i in act0 else 0 for i in range(1 << n)]
        A1 = [1 if i in act1 else 0 for i in range(1 << n)]

        # Verify ground-truth NP^A Set-Disjointness labels differ
        inter0 = [c for c in range(N_half) if A0[c] == 1 and A0[c + N_half] == 1]
        inter1 = [c for c in range(N_half) if A1[c] == 1 and A1[c + N_half] == 1]
        assert len(inter0) == 0, "A0 must be DISJOINT"
        assert len(inter1) >= 1, "A1 must be INTERSECTING"

        # Verify A~^(0) and A~^(1) agree 100% identically on ALL T non-Boolean queries via full MLE
        for j, r in enumerate(queries):
            v0 = mle_eval_lagrange(A0, r, q)
            v1 = mle_eval_lagrange(A1, r, q)
            assert v0 == v1 == shared_sig[j], f"Algebraic query {j} mismatch mod {q}"

        # Verify sparsity and distinctness on {0,1}^n
        hamming_diff = sum(a ^ b for a, b in zip(A0, A1))
        assert 0 < hamming_diff <= 12

        print(
            f"[PASS] AW09 Part B (Algebraic-Oracle Hiding, q={q}, T={T} non-Boolean queries): "
            f"constructed sparse DISJOINT oracle (wt={sum(A0)}, L=0) & INTERSECTING oracle "
            f"(wt={sum(A1)}, L=1, witness={inter1[0]}, Hamming diff={hamming_diff}/32) with "
            f"IDENTICAL MLE query vector {shared_sig} mod {q}."
        )


def test_part_c_pspace_collapsing_oracle_consistency() -> None:
    """
    Demonstrates the core engine of AW09's collapsing oracle (NP^{A~} <= PSPACE^{A~} = P^A <= P^{A~}):
    When A is a QBF / PSPACE oracle, its multilinear extension A~(r) mod q is computable in PSPACE
    by streaming over w in {0,1}^n using O(n + log q) working space.
    We evaluate a concrete parameterized QBF oracle Phi_w (for w in {0,1}^4) directly by
    quantified backtracking (PSPACE) and confirm its streaming MLE equals the full-table MLE
    across F_101 and F_257.
    """
    n = 4

    def qbf_oracle(w: Tuple[int, ...]) -> int:
        """
        Parameterized QBF instance on 4 parameter bits w = (w0, w1, w2, w3):
          Phi_w := forall u in {0,1}, exists v in {0,1}, forall z in {0,1}:
                   ((u ^ w0) | (v ^ w1)) & ((v ^ w2) | (z ^ w3)) & (u | v | z | w0)
        Evaluated via recursive quantified backtracking (linear space in quantifier depth).
        """
        w0, w1, w2, w3 = w
        for u in (0, 1):
            exists_v = False
            for v in (0, 1):
                forall_z = True
                for z in (0, 1):
                    c1 = (u ^ w0) | (v ^ w1)
                    c2 = (v ^ w2) | (z ^ w3)
                    c3 = u | v | z | w0
                    if not (c1 and c2 and c3):
                        forall_z = False
                        break
                if forall_z:
                    exists_v = True
                    break
            if not exists_v:
                return 0
        return 1

    table = [qbf_oracle(int_to_bits(idx, n)) for idx in range(1 << n)]
    # Ensure the QBF oracle is non-trivial (neither constant 0 nor constant 1)
    assert 0 < sum(table) < (1 << n)

    rng = random.Random(2026999)
    for q in (101, 257):
        for _ in range(50):
            r = [rng.randrange(q) for _ in range(n)]
            v_stream = mle_eval_direct_sum(qbf_oracle, n, r, q)
            v_table = mle_eval_lagrange(table, r, q)
            assert v_stream == v_table

    print(
        f"[PASS] AW09 Part C (PSPACE Collapsing Oracle Consistency): parameterized QBF oracle "
        f"(true on {sum(table)}/{1 << n} inputs) verified streaming O(n + log q)-space MLE == "
        f"full-table MLE over F_101 and F_257 (50 random algebraic queries each)."
    )


def main() -> None:
    test_multilinear_extension()
    test_sumcheck_protocol()
    test_part_a_bgs_breaks_against_mle()
    test_part_b_aw09_disjointness_and_hiding()
    test_part_c_pspace_collapsing_oracle_consistency()
    print("ALL BATON #009 ALGEBRIZATION & SUMCHECK VERIFICATIONS PASSED.")


if __name__ == "__main__":
    main()
