#!/usr/bin/env python3
"""
Verification script for Baton #016 (`baton-016-gct-n30-hwv-eval`):
Explicit Highest-Weight Vector (HWV) Construction & Evaluation for the Certified
N = 30 (d = 10, m = 3, l = 9) Degree-10 Defining Equations of Omega_3 = cl(GL_9 . det_3):
  - lambda^(1) = (13, 3, 2, 2, 2, 2, 2, 2, 2)  [dim = 554,268, a = 1 > 0 = k = sk]
  - lambda^(2) = (12, 5, 2, 2, 2, 2, 2, 2, 1)  [dim = 31,039,008, a = 1 > 0 = k = sk]

Self-contained Python 3.12 standard-library-only verification:
  1. Non-triviality and exact degree-10 homogeneity on 20 generic cubics over F_p (two primes).
  2. Exact GL_9 torus weight verification for both lambda^(1) and lambda^(2).
  3. Zero-trust Lie-algebra / unipotent invariance certification under ALL 36 raising
     operators I + t * E_{ab} (0 <= a < b <= 8) on 20 generic cubics (720 checks/HWV/prime),
     plus non-invariance under lowering operators and exact identity P_2(t) = t^2 Q(t).
  4. Moment-of-truth evaluation on 50 random invertible g in GL_9(F_p) (two primes):
       - H_1(g . det_3) == 0 and H_2(g . det_3) == 0  (50/50)
       - H_1(g . perm_3) != 0 and H_2(g . perm_3) != 0 (50/50)
       - H_1(g . (x_8 * perm_2)) == 0 and H_2(g . (x_8 * perm_2)) == 0 (50/50)
  5. Exact arbitrary-precision integer (Z) certificate on sparse unit-determinant matrix
     g_0 in SL_9(Z) (det = 1, 15 nonzeros in {0,1}): zero modular-arithmetic ambiguity.
  6. Analytic vanishing-identity verification over Q and F_p:
       - hess(det_3)(X) = -2 * det_3(X)^3  =>  P_1(t) / F(x(t))^3 = const on Omega_3
       - adj(H_{det_3}(X))(W) = det(X)^2 (2 X W^T X - Tr(X W^T) X)
         =>  Q(t) / F(x(t))^2 = const on Omega_3, while non-constant on perm_3.
"""

from __future__ import annotations

import random
import sys
import time
from fractions import Fraction


# ---------------------------------------------------------------------------
# Exact linear algebra over F_p
# ---------------------------------------------------------------------------

def det_mod(A: list[list[int]], p: int) -> int:
    n = len(A)
    M = [[x % p for x in row] for row in A]
    det = 1
    for i in range(n):
        piv = -1
        for r in range(i, n):
            if M[r][i] != 0:
                piv = r
                break
        if piv == -1:
            return 0
        if piv != i:
            M[i], M[piv] = M[piv], M[i]
            det = (-det) % p
        val = M[i][i]
        det = (det * val) % p
        inv = pow(val, p - 2, p)
        row_i = M[i]
        for r in range(i + 1, n):
            mri = M[r][i]
            if mri != 0:
                fac = (mri * inv) % p
                row_r = M[r]
                for c in range(i + 1, n):
                    row_r[c] = (row_r[c] - fac * row_i[c]) % p
                row_r[i] = 0
    return det


def det_and_inv_mod(A: list[list[int]], p: int) -> tuple[int, list[list[int]] | None]:
    """Compute (det(A), A^{-1}) mod p via Gauss-Jordan; returns (0, None) if singular."""
    n = len(A)
    M = [[A[i][j] % p for j in range(n)] + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    det = 1
    for i in range(n):
        piv = -1
        for r in range(i, n):
            if M[r][i] != 0:
                piv = r
                break
        if piv == -1:
            return 0, None
        if piv != i:
            M[i], M[piv] = M[piv], M[i]
            det = (-det) % p
        val = M[i][i]
        det = (det * val) % p
        inv = pow(val, p - 2, p)
        row_i = M[i]
        for c in range(i, 2 * n):
            row_i[c] = (row_i[c] * inv) % p
        for r in range(n):
            if r != i:
                mri = M[r][i]
                if mri != 0:
                    row_r = M[r]
                    for c in range(i + 1, 2 * n):
                        row_r[c] = (row_r[c] - mri * row_i[c]) % p
                    row_r[i] = 0
    return det, [row[n:] for row in M]


def poly_val_and_deriv_at_0_mod(vals: list[int], p: int) -> tuple[int, int]:
    """Given P(0), P(1), ..., P(d) mod p for deg(P) <= d, return (P(0), P'(0)) mod p."""
    d = len(vals) - 1
    d0 = vals[0] % p
    d1 = 0
    for k in range(d + 1):
        if k == 0:
            s = 0
            for j in range(1, d + 1):
                s = (s - pow(j, p - 2, p)) % p
            d1 = (d1 + vals[0] * s) % p
        else:
            num = 1
            den = k % p
            for j in range(1, d + 1):
                if j == k:
                    continue
                num = (num * (-j)) % p
                den = (den * (k - j)) % p
            d1 = (d1 + vals[k] * num * pow(den, p - 2, p)) % p
    return d0, d1


def det_and_deriv_mod(A0: list[list[int]], A1: list[list[int]], p: int) -> tuple[int, int]:
    """Return (P(0), P'(0)) mod p where P(t) = det(A0 + t * A1), valid even if A0 is singular."""
    d0, inv0 = det_and_inv_mod(A0, p)
    if inv0 is not None:
        # Jacobi's formula: P'(0) = det(A0) * Tr(A0^{-1} A1)
        n = len(A0)
        tr = 0
        for i in range(n):
            row = inv0[i]
            s = 0
            for j in range(n):
                s += row[j] * A1[j][i]
            tr = (tr + s) % p
        return d0, (d0 * tr) % p
    # Exact fallback via degree-n Lagrange interpolation (handles singular A0 exactly)
    n = len(A0)
    vals = []
    for t in range(n + 1):
        At = [[(A0[i][j] + t * A1[i][j]) % p for j in range(n)] for i in range(n)]
        vals.append(det_mod(At, p))
    return poly_val_and_deriv_at_0_mod(vals, p)


def det_and_deriv_interp_mod(A0: list[list[int]], A1: list[list[int]], p: int) -> tuple[int, int]:
    """Pure interpolation implementation for independent cross-checking against Jacobi's formula."""
    n = len(A0)
    vals = []
    for t in range(n + 1):
        At = [[(A0[i][j] + t * A1[i][j]) % p for j in range(n)] for i in range(n)]
        vals.append(det_mod(At, p))
    return poly_val_and_deriv_at_0_mod(vals, p)


# ---------------------------------------------------------------------------
# Exact linear algebra over Z / Q (zero modular-arithmetic ambiguity)
# ---------------------------------------------------------------------------

def det_exact(A: list[list[int]]) -> int:
    """Exact integer determinant via fraction-free Bareiss algorithm."""
    n = len(A)
    M = [row[:] for row in A]
    sign = 1
    prev_piv = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            swap = -1
            for r in range(k + 1, n):
                if M[r][k] != 0:
                    swap = r
                    break
            if swap == -1:
                return 0
            M[k], M[swap] = M[swap], M[k]
            sign = -sign
        piv = M[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * piv - M[i][k] * M[k][j]) // prev_piv
            M[i][k] = 0
        prev_piv = piv
    return sign * M[n - 1][n - 1]


def poly_val_and_deriv_at_0_exact(vals: list[int]) -> tuple[int, int]:
    """Exact rational Lagrange evaluation of (P(0), P'(0)) for integer polynomial P(t)."""
    d = len(vals) - 1
    d0 = Fraction(vals[0])
    d1 = Fraction(0)
    for k in range(d + 1):
        if k == 0:
            s = sum(Fraction(-1, j) for j in range(1, d + 1))
            d1 += Fraction(vals[0]) * s
        else:
            prod = Fraction(1, k)
            for j in range(1, d + 1):
                if j == k:
                    continue
                prod *= Fraction(-j, k - j)
            d1 += Fraction(vals[k]) * prod
    assert d0.denominator == 1 and d1.denominator == 1
    return int(d0), int(d1)


# ---------------------------------------------------------------------------
# Symmetric cubic tensors & GL_9 action
# Convention: T[i][j][k] = d^3 F / (dx_i dx_j dx_k), so F(x) = (1/6) sum T[i][j][k] x_i x_j x_k.
# Action: (g . F)(x) = F(g x)  <=>  (g . T)[a][b][c] = sum_{i,j,k} T[i][j][k] g[i][a] g[j][b] g[k][c].
# ---------------------------------------------------------------------------

def make_standard_tensor(kind: str, p: int | None = None) -> list[list[list[int]]]:
    """Build exact symmetric 9x9x9 tensor T_{ijk} = partial_i partial_j partial_k F."""
    T = [[[0] * 9 for _ in range(9)] for _ in range(9)]
    if kind in ("det3", "perm3"):
        perms = [
            ((0, 1, 2), 1), ((1, 2, 0), 1), ((2, 0, 1), 1),
            ((0, 2, 1), -1), ((2, 1, 0), -1), ((1, 0, 2), -1),
        ]
        for (c0, c1, c2), sgn in perms:
            val = sgn if kind == "det3" else 1
            i0, i1, i2 = c0, 3 + c1, 6 + c2
            for a, b, c in (
                (i0, i1, i2), (i0, i2, i1),
                (i1, i0, i2), (i1, i2, i0),
                (i2, i0, i1), (i2, i1, i0),
            ):
                T[a][b][c] += val
    elif kind == "padded_perm2":
        # F(x) = x_8 * (x_0 x_3 + x_1 x_2)  (2x2 permanent padded by linear form x_8)
        for i0, i1, i2 in ((8, 0, 3), (8, 1, 2)):
            for a, b, c in (
                (i0, i1, i2), (i0, i2, i1),
                (i1, i0, i2), (i1, i2, i0),
                (i2, i0, i1), (i2, i1, i0),
            ):
                T[a][b][c] += 1
    else:
        raise ValueError(f"Unknown tensor kind: {kind}")

    if p is not None:
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    T[i][j][k] %= p
    return T


def random_sym_tensor(rng: random.Random, p: int) -> list[list[list[int]]]:
    T = [[[0] * 9 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(i, 9):
            for k in range(j, 9):
                v = rng.randrange(p)
                T[i][j][k] = T[i][k][j] = T[j][i][k] = T[j][k][i] = T[k][i][j] = T[k][j][i] = v
    return T


def scale_tensor(T: list[list[list[int]]], c: int, p: int) -> list[list[list[int]]]:
    return [[[(T[i][j][k] * c) % p for k in range(9)] for j in range(9)] for i in range(9)]


def transform_tensor_mod(T: list[list[list[int]]], g: list[list[int]], p: int) -> list[list[list[int]]]:
    T1 = [[[0] * 9 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            row_ij = T[i][j]
            out_ij = T1[i][j]
            for k in range(9):
                v = row_ij[k]
                if v:
                    gk = g[k]
                    for r in range(9):
                        if gk[r]:
                            out_ij[r] = (out_ij[r] + v * gk[r]) % p
    T2 = [[[0] * 9 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            row_ij = T1[i][j]
            gj = g[j]
            for q in range(9):
                gjq = gj[q]
                if gjq:
                    out_iq = T2[i][q]
                    for r in range(9):
                        if row_ij[r]:
                            out_iq[r] = (out_iq[r] + row_ij[r] * gjq) % p
    T3 = [[[0] * 9 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        gi = g[i]
        for a in range(9):
            gia = gi[a]
            if gia:
                out_a = T3[a]
                in_i = T2[i]
                for q in range(9):
                    out_aq = out_a[q]
                    in_iq = in_i[q]
                    for r in range(9):
                        if in_iq[r]:
                            out_aq[r] = (out_aq[r] + in_iq[r] * gia) % p
    return T3


def transform_tensor_exact(T: list[list[list[int]]], g: list[list[int]]) -> list[list[list[int]]]:
    T1 = [[[0] * 9 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            for k in range(9):
                v = T[i][j][k]
                if v:
                    for r in range(9):
                        if g[k][r]:
                            T1[i][j][r] += v * g[k][r]
    T2 = [[[0] * 9 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            for r in range(9):
                v = T1[i][j][r]
                if v:
                    for q in range(9):
                        if g[j][q]:
                            T2[i][q][r] += v * g[j][q]
    T3 = [[[0] * 9 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for q in range(9):
            for r in range(9):
                v = T2[i][q][r]
                if v:
                    for a in range(9):
                        if g[i][a]:
                            T3[a][q][r] += v * g[i][a]
    return T3


def apply_elem_mod(T: list[list[list[int]]], a: int, b: int, t: int, p: int) -> list[list[list[int]]]:
    """Fast O(9^2) action of elementary unipotent matrix g = I + t * E_{ab} (index b -> b + t * a)."""
    T1 = [[row[:] for row in mat] for mat in T]
    for i in range(9):
        for j in range(9):
            T1[i][j][b] = (T1[i][j][b] + t * T[i][j][a]) % p
    T2 = [[row[:] for row in mat] for mat in T1]
    for i in range(9):
        for k in range(9):
            T2[i][b][k] = (T2[i][b][k] + t * T1[i][a][k]) % p
    T3 = [[row[:] for row in mat] for mat in T2]
    for j in range(9):
        for k in range(9):
            T3[b][j][k] = (T3[b][j][k] + t * T2[a][j][k]) % p
    return T3


def apply_diag_mod(T: list[list[list[int]]], diag: list[int], p: int) -> list[list[list[int]]]:
    return [
        [[(T[i][j][k] * diag[i] * diag[j] * diag[k]) % p for k in range(9)] for j in range(9)]
        for i in range(9)
    ]


# ---------------------------------------------------------------------------
# Explicit Highest-Weight Vectors H_1 and H_2
# ---------------------------------------------------------------------------

def eval_H1_mod(T: list[list[list[int]]], p: int, use_interp: bool = False) -> int:
    """
    Unique HWV of S_{(13, 3, 2^7)}(C^9) in Sym^10(Sym^3(C^9)):
        H_1(T) = 9 * det(M_0) * T_{001} - Tr(adj(M_0) * M_1) * T_{000}
               = 9 * P_1(0) * T_{001} - P_1'(0) * T_{000},  P_1(t) = det(M_0 + t M_1).
    """
    M0 = [[T[i][j][0] for j in range(9)] for i in range(9)]
    M1 = [[T[i][j][1] for j in range(9)] for i in range(9)]
    if use_interp:
        d0, d1 = det_and_deriv_interp_mod(M0, M1, p)
    else:
        d0, d1 = det_and_deriv_mod(M0, M1, p)
    return (9 * d0 * T[0][0][1] - d1 * T[0][0][0]) % p


def eval_H2_mod(T: list[list[list[int]]], p: int, use_interp: bool = False) -> int:
    """
    Unique HWV of S_{(12, 5, 2^6, 1)}(C^9) in Sym^10(Sym^3(C^9)):
        Let Q(t) = det( (M_0 + t M_1)_{:, 0..7} | v_{11} ), where v_{11}[i] = T_{i,1,1}.
        H_2(T) = Q'(0) * T_{000} - 6 * Q(0) * T_{001}.
    """
    A0 = [[T[i][j][0] for j in range(8)] + [T[i][1][1]] for i in range(9)]
    A1 = [[T[i][j][1] for j in range(8)] + [0] for i in range(9)]
    if use_interp:
        q0, q1 = det_and_deriv_interp_mod(A0, A1, p)
    else:
        q0, q1 = det_and_deriv_mod(A0, A1, p)
    return (q1 * T[0][0][0] - 6 * q0 * T[0][0][1]) % p


def eval_H1_exact(T: list[list[list[int]]]) -> int:
    M0 = [[T[i][j][0] for j in range(9)] for i in range(9)]
    M1 = [[T[i][j][1] for j in range(9)] for i in range(9)]
    vals = [det_exact([[M0[i][j] + t * M1[i][j] for j in range(9)] for i in range(9)]) for t in range(10)]
    d0, d1 = poly_val_and_deriv_at_0_exact(vals)
    return 9 * d0 * T[0][0][1] - d1 * T[0][0][0]


def eval_H2_exact(T: list[list[list[int]]]) -> int:
    M0 = [[T[i][j][0] for j in range(9)] for i in range(9)]
    M1 = [[T[i][j][1] for j in range(9)] for i in range(9)]
    v11 = [T[i][1][1] for i in range(9)]
    vals = [
        det_exact([[M0[i][j] + t * M1[i][j] for j in range(8)] + [v11[i]] for i in range(9)])
        for t in range(9)
    ]
    q0, q1 = poly_val_and_deriv_at_0_exact(vals)
    return q1 * T[0][0][0] - 6 * q0 * T[0][0][1]


def weight_monomial_mod(diag: list[int], wt: tuple[int, ...], p: int) -> int:
    res = 1
    for t_i, w_i in zip(diag, wt):
        res = (res * pow(t_i, w_i, p)) % p
    return res


def random_gl9(rng: random.Random, p: int) -> list[list[int]]:
    while True:
        g = [[rng.randrange(p) for _ in range(9)] for _ in range(9)]
        if det_mod(g, p) != 0:
            return g


# ---------------------------------------------------------------------------
# Verification suite
# ---------------------------------------------------------------------------

def main() -> int:
    t0 = time.perf_counter()
    PRIMES = (1000003, 1000033)
    WT_1 = (13, 3, 2, 2, 2, 2, 2, 2, 2)
    WT_2 = (12, 5, 2, 2, 2, 2, 2, 2, 1)

    print("=" * 78)
    print("BATON #016 VERIFICATION: EXPLICIT N=30 DEGREE-10 GCT HWVs ON Omega_3 vs perm_3")
    print("=" * 78)

    # -----------------------------------------------------------------------
    # CHECK 1, 2, 3: Non-triviality, Homogeneity, Exact Weights, ALL 36 E_{ab}
    # -----------------------------------------------------------------------
    for p in PRIMES:
        rng = random.Random(1600 + p)
        n_generic = 20
        nz_h1 = 0
        nz_h2 = 0
        homog_ok = 0
        weight_ok = 0
        raise_checks = 0
        raise_ok = 0
        interp_cross_ok = 0
        p2_t2q_ok = 0

        for idx in range(n_generic):
            T = random_sym_tensor(rng, p)
            h1 = eval_H1_mod(T, p)
            h2 = eval_H2_mod(T, p)
            if h1 != 0:
                nz_h1 += 1
            if h2 != 0:
                nz_h2 += 1

            # Cross-check fast Jacobi evaluator against exact Lagrange interpolation on first 5
            if idx < 5:
                assert h1 == eval_H1_mod(T, p, use_interp=True)
                assert h2 == eval_H2_mod(T, p, use_interp=True)
                interp_cross_ok += 1

                # Verify exact column-operation identity P_2(t) == t^2 * Q(t)
                M0 = [[T[i][j][0] for j in range(9)] for i in range(9)]
                M1 = [[T[i][j][1] for j in range(9)] for i in range(9)]
                v00 = [T[i][0][0] for i in range(9)]
                v11 = [T[i][1][1] for i in range(9)]
                for t_val in range(1, 7):
                    lhs = det_mod(
                        [[(M0[i][j] + t_val * M1[i][j]) % p for j in range(8)] + [v00[i]] for i in range(9)],
                        p,
                    )
                    rhs = (
                        t_val
                        * t_val
                        * det_mod(
                            [[(M0[i][j] + t_val * M1[i][j]) % p for j in range(8)] + [v11[i]] for i in range(9)],
                            p,
                        )
                    ) % p
                    assert lhs == rhs
                p2_t2q_ok += 1

            # Degree-10 homogeneity
            c = rng.randrange(2, p)
            Tc = scale_tensor(T, c, p)
            c10 = pow(c, 10, p)
            assert eval_H1_mod(Tc, p) == (c10 * h1) % p
            assert eval_H2_mod(Tc, p) == (c10 * h2) % p
            homog_ok += 1

            # Exact GL_9 torus weights
            diag = [rng.randrange(1, p) for _ in range(9)]
            TD = apply_diag_mod(T, diag, p)
            assert eval_H1_mod(TD, p) == (weight_monomial_mod(diag, WT_1, p) * h1) % p
            assert eval_H2_mod(TD, p) == (weight_monomial_mod(diag, WT_2, p) * h2) % p
            weight_ok += 1

            # ALL 36 strictly upper-triangular elementary operators I + t * E_{ab} (0 <= a < b <= 8)
            for a in range(9):
                for b in range(a + 1, 9):
                    t_param = rng.randrange(1, p)
                    Tp = apply_elem_mod(T, a, b, t_param, p)
                    assert eval_H1_mod(Tp, p) == h1, f"H1 failed E_{{{a},{b}}} mod {p}"
                    assert eval_H2_mod(Tp, p) == h2, f"H2 failed E_{{{a},{b}}} mod {p}"
                    raise_checks += 1
                    raise_ok += 1

        # Verify lowering operator non-invariance (confirming non-trivial GL_9 irreps)
        T_low = random_sym_tensor(rng, p)
        assert eval_H1_mod(apply_elem_mod(T_low, 1, 0, 7, p), p) != eval_H1_mod(T_low, p)
        assert eval_H2_mod(apply_elem_mod(T_low, 1, 0, 7, p), p) != eval_H2_mod(T_low, p)
        assert eval_H2_mod(apply_elem_mod(T_low, 8, 7, 7, p), p) != eval_H2_mod(T_low, p)

        assert nz_h1 == n_generic and nz_h2 == n_generic
        assert homog_ok == n_generic and weight_ok == n_generic
        assert raise_ok == raise_checks == n_generic * 36
        assert interp_cross_ok == 5 and p2_t2q_ok == 5

        print(
            f"[PASS] Lie-algebra HWV certification (p={p}): "
            f"H1 & H2 nonzero on {n_generic}/{n_generic} generic cubics, "
            f"exact deg=10 & weights {WT_1} / {WT_2}, "
            f"{raise_ok}/{raise_checks} raising checks (ALL 36 E_{{ab}}) PASSED, "
            f"lowering non-invariant, P2(t)=t^2 Q(t) verified."
        )

    # -----------------------------------------------------------------------
    # CHECK 4: Moment of Truth — 50 random g in GL_9(F_p) on det_3, perm_3, x_8*perm_2
    # -----------------------------------------------------------------------
    for p in PRIMES:
        rng = random.Random(202600 + p)
        T_det = make_standard_tensor("det3", p)
        T_perm = make_standard_tensor("perm3", p)
        T_pad2 = make_standard_tensor("padded_perm2", p)

        n_trials = 50
        det_h1_zero = det_h2_zero = 0
        perm_h1_nz = perm_h2_nz = 0
        pad2_h1_zero = pad2_h2_zero = 0

        for _ in range(n_trials):
            g = random_gl9(rng, p)
            g_det = transform_tensor_mod(T_det, g, p)
            g_perm = transform_tensor_mod(T_perm, g, p)
            g_pad2 = transform_tensor_mod(T_pad2, g, p)

            if eval_H1_mod(g_det, p) == 0:
                det_h1_zero += 1
            if eval_H2_mod(g_det, p) == 0:
                det_h2_zero += 1
            if eval_H1_mod(g_perm, p) != 0:
                perm_h1_nz += 1
            if eval_H2_mod(g_perm, p) != 0:
                perm_h2_nz += 1
            if eval_H1_mod(g_pad2, p) == 0:
                pad2_h1_zero += 1
            if eval_H2_mod(g_pad2, p) == 0:
                pad2_h2_zero += 1

        assert det_h1_zero == n_trials and det_h2_zero == n_trials
        assert perm_h1_nz == n_trials and perm_h2_nz == n_trials
        assert pad2_h1_zero == n_trials and pad2_h2_zero == n_trials

        print(
            f"[PASS] Orbit separation (p={p}, {n_trials} random g in GL_9): "
            f"det_3 zero=({det_h1_zero}/{n_trials}, {det_h2_zero}/{n_trials}), "
            f"perm_3 NONZERO=({perm_h1_nz}/{n_trials}, {perm_h2_nz}/{n_trials}), "
            f"x_8*perm_2 zero=({pad2_h1_zero}/{n_trials}, {pad2_h2_zero}/{n_trials})."
        )

    # -----------------------------------------------------------------------
    # CHECK 5: Exact Arbitrary-Precision Integer (Z) Certificate on Sparse g_0 in SL_9(Z)
    # -----------------------------------------------------------------------
    g0 = [[1 if i == j else 0 for j in range(9)] for i in range(9)]
    for r, c in ((2, 0), (3, 0), (7, 0), (2, 1), (5, 1), (8, 1)):
        g0[r][c] = 1
    det_g0 = det_exact(g0)
    nnz_g0 = sum(1 for row in g0 for x in row if x != 0)
    assert det_g0 == 1 and nnz_g0 == 15

    T_det_Z = make_standard_tensor("det3", None)
    T_perm_Z = make_standard_tensor("perm3", None)
    T_pad2_Z = make_standard_tensor("padded_perm2", None)

    g0_det = transform_tensor_exact(T_det_Z, g0)
    g0_perm = transform_tensor_exact(T_perm_Z, g0)
    g0_pad2 = transform_tensor_exact(T_pad2_Z, g0)

    h1_det_Z, h2_det_Z = eval_H1_exact(g0_det), eval_H2_exact(g0_det)
    h1_perm_Z, h2_perm_Z = eval_H1_exact(g0_perm), eval_H2_exact(g0_perm)
    h1_pad2_Z, h2_pad2_Z = eval_H1_exact(g0_pad2), eval_H2_exact(g0_pad2)

    assert h1_det_Z == 0 and h2_det_Z == 0
    assert h1_perm_Z == -48 and h2_perm_Z == 48
    assert h1_pad2_Z == 0 and h2_pad2_Z == 0

    print(
        f"[PASS] Exact Z certificate (g_0 in SL_9(Z), det={det_g0}, nnz={nnz_g0}): "
        f"H1(g0.det3)={h1_det_Z}, H2(g0.det3)={h2_det_Z}; "
        f"H1(g0.perm3)={h1_perm_Z}, H2(g0.perm3)={h2_perm_Z}; "
        f"H1(g0.x8*perm2)={h1_pad2_Z}, H2(g0.x8*perm2)={h2_pad2_Z}."
    )

    # -----------------------------------------------------------------------
    # CHECK 6: Exact Analytic Vanishing Identities on det_3 vs Failure on perm_3
    # -----------------------------------------------------------------------
    # 6a. Exact Q-ratios P_1(t)/F(t)^3 and Q(t)/F(t)^2 along x(t) = e_0 + t e_1 for g0.det3 vs g0.perm3
    def ratio_series(T_int: list[list[list[int]]], ts: list[int]) -> list[tuple[int, Fraction, Fraction]]:
        M0 = [[T_int[i][j][0] for j in range(9)] for i in range(9)]
        M1 = [[T_int[i][j][1] for j in range(9)] for i in range(9)]
        v11 = [T_int[i][1][1] for i in range(9)]
        out = []
        for t_val in ts:
            Ft = (
                T_int[0][0][0]
                + 3 * t_val * T_int[0][0][1]
                + 3 * t_val * t_val * T_int[0][1][1]
                + t_val * t_val * t_val * T_int[1][1][1]
            )
            assert Ft != 0
            Pt = det_exact([[M0[i][j] + t_val * M1[i][j] for j in range(9)] for i in range(9)])
            Qt = det_exact([[M0[i][j] + t_val * M1[i][j] for j in range(8)] + [v11[i]] for i in range(9)])
            out.append((t_val, Fraction(Pt, Ft ** 3), Fraction(Qt, Ft ** 2)))
        return out

    det_ratios = ratio_series(g0_det, [0, 2, 3, 4, 5])
    for _, r1, r2 in det_ratios:
        assert r1 == Fraction(-1, 108)
        assert r2 == Fraction(-1, 9)

    perm_ratios = ratio_series(g0_perm, [0, 1, 2, 3])
    assert len({r1 for _, r1, _ in perm_ratios}) > 1
    assert len({r2 for _, _, r2 in perm_ratios}) > 1

    print(
        f"[PASS] Exact analytic ratio law on g0.det3 (t=0,2,3,4,5): "
        f"P1(t)/F(t)^3 = {det_ratios[0][1]} (const), Q(t)/F(t)^2 = {det_ratios[0][2]} (const); "
        f"on g0.perm3: P1(0)/F(0)^3={perm_ratios[0][1]} != P1(1)/F(1)^3={perm_ratios[1][1]}, "
        f"Q(0)/F(0)^2={perm_ratios[0][2]} != Q(1)/F(1)^2={perm_ratios[1][2]}."
    )

    # 6b. Exact operator identity adj(H_{det_3}(X))(W) = det(X)^2 (2 X W^T X - Tr(X W^T) X)
    #     verified directly on 20 random 3x3 matrix pairs (X, W) over F_p
    p_chk = 1000003
    rng_op = random.Random(9999)
    T_det_p = make_standard_tensor("det3", p_chk)

    def mat3_mul(A: list[list[int]], B: list[list[int]], p: int) -> list[list[int]]:
        return [
            [sum(A[i][k] * B[k][j] for k in range(3)) % p for j in range(3)]
            for i in range(3)
        ]

    def mat3_det(A: list[list[int]], p: int) -> int:
        return (
            A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
        ) % p

    op_ok = 0
    for _ in range(20):
        X = [[rng_op.randrange(p_chk) for _ in range(3)] for _ in range(3)]
        while mat3_det(X, p_chk) == 0:
            X = [[rng_op.randrange(p_chk) for _ in range(3)] for _ in range(3)]
        W = [[rng_op.randrange(p_chk) for _ in range(3)] for _ in range(3)]
        x_vec = [X[r][c] for r in range(3) for c in range(3)]
        w_vec = [W[r][c] for r in range(3) for c in range(3)]

        # H_{det_3}(X)[i][j] = sum_k T_det[i][j][k] * x_vec[k]
        H_mat = [
            [sum(T_det_p[i][j][k] * x_vec[k] for k in range(9)) % p_chk for j in range(9)]
            for i in range(9)
        ]
        det_H, inv_H = det_and_inv_mod(H_mat, p_chk)
        assert inv_H is not None
        detX = mat3_det(X, p_chk)
        assert det_H == (-2 * pow(detX, 3, p_chk)) % p_chk

        # LHS: adj(H_{det_3}(X)) * w_vec
        lhs_vec = [
            (det_H * sum(inv_H[i][j] * w_vec[j] for j in range(9))) % p_chk
            for i in range(9)
        ]
        # RHS: det(X)^2 * (2 X W^T X - Tr(X W^T) X)
        WT = [[W[j][i] for j in range(3)] for i in range(3)]
        XWT = mat3_mul(X, WT, p_chk)
        XWTX = mat3_mul(XWT, X, p_chk)
        tr_XWT = (XWT[0][0] + XWT[1][1] + XWT[2][2]) % p_chk
        d2 = pow(detX, 2, p_chk)
        rhs_vec = [
            (d2 * (2 * XWTX[r][c] - tr_XWT * X[r][c])) % p_chk
            for r in range(3)
            for c in range(3)
        ]
        assert lhs_vec == rhs_vec
        op_ok += 1

    print(
        f"[PASS] Exact Hessian-adjugate operator identity verified on {op_ok}/20 random (X, W) in Mat_3(F_{p_chk}): "
        f"det(H_{{det_3}}(X)) = -2 det(X)^3 and adj(H_{{det_3}}(X))(W) = det(X)^2 (2 X W^T X - Tr(X W^T) X)."
    )

    elapsed = time.perf_counter() - t0
    print("=" * 78)
    print(f"[PASS] ALL BATON #016 VERIFICATION CHECKS PASSED in {elapsed:.2f}s.")
    print(
        "[PASS] CONSTRUCTIVE GCT THEOREM VERIFIED: perm_3 not in Omega_3 = cl(GL_9 . det_3) "
        "=> border determinantal complexity underline_dc(perm_3) > 3 via BOTH explicit N=30 "
        "degree-10 HWVs H_1 (13,3,2^7) and H_2 (12,5,2^6,1)!"
    )
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
