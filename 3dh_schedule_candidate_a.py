cat > 3dh_schedule_candidate_a.py <<'EOF'
#!/usr/bin/env python3

import time
import numpy as np

# ============================================================
# 3DH-v1
# 3D Message Schedule Candidate A
# Experimental Avalanche Test
#
# NOTE:
# This is experimental research code.
# It is NOT yet a cryptographically validated hash function.
# ============================================================

# ------------------------------------------------------------
# Test configuration
# ------------------------------------------------------------

# Smartphone LIGHT test:
N = 64

# Number of mixing rounds
ROUNDS = 64

MASK64 = (1 << 64) - 1

# Rounds whose results will be displayed
REPORT_ROUNDS = {
    0, 1, 2, 3,
    7, 15, 31, 63
}


# ============================================================
# Generate deterministic 64-bit round constants
# ============================================================

def splitmix64(x):
    x = (
        x
        + 0x9E3779B97F4A7C15
    ) & MASK64

    z = x

    z = (
        (z ^ (z >> 30))
        * 0xBF58476D1CE4E5B9
    ) & MASK64

    z = (
        (z ^ (z >> 27))
        * 0x94D049BB133111EB
    ) & MASK64

    return (
        z ^ (z >> 31)
    ) & MASK64


K3D = np.array(
    [
        splitmix64(t)
        for t in range(ROUNDS)
    ],
    dtype=np.uint64
)


# ============================================================
# 64-bit rotate
# ============================================================

def rotl64(a, r):

    r = int(r)

    if not 1 <= r <= 63:
        raise ValueError(
            "rotation must be 1..63"
        )

    return (
        (a << np.uint64(r))
        |
        (a >> np.uint64(64 - r))
    )


def rotr64(a, r):

    r = int(r)

    if not 1 <= r <= 63:
        raise ValueError(
            "rotation must be 1..63"
        )

    return (
        (a >> np.uint64(r))
        |
        (a << np.uint64(64 - r))
    )


# ============================================================
# 3D Message Schedule
#
# t = round number
# NOT clock time
# ============================================================

def schedule(t, n):

    span = n - 1

    dx = (
        ((2 * t + 1) % span)
        + 1
    )

    dy = (
        ((4 * t + 3) % span)
        + 1
    )

    dz = (
        ((6 * t + 5) % span)
        + 1
    )

    # Change direction
    if t & 1:
        dx = -dx

    if t & 2:
        dy = -dy

    if t & 4:
        dz = -dz

    # Rotation amounts:
    # always 1..63
    r1 = (
        (7 * t) % 63
    ) + 1

    r2 = (
        (13 * t + 17) % 63
    ) + 1

    r3 = (
        (29 * t + 31) % 63
    ) + 1

    r4 = (
        (43 * t + 11) % 63
    ) + 1

    return (
        dx, dy, dz,
        r1, r2, r3, r4
    )


# ============================================================
# CH3
#
# X bit = 1 -> select Y
# X bit = 0 -> select Z
# ============================================================

def ch3(x, y, z):

    return (
        (x & y)
        ^
        ((~x) & z)
    )


# ============================================================
# MAJ3
#
# Majority vote of X,Y,Z
# ============================================================

def maj3(x, y, z):

    return (
        (x & y)
        ^
        (x & z)
        ^
        (y & z)
    )


# ============================================================
# One 3D-MIX64 round
# ============================================================

def mix_round(p, t):

    (
        dx, dy, dz,
        r1, r2, r3, r4
    ) = schedule(
        t,
        p.shape[0]
    )

    # 3D spatial movement
    # np.roll wraps around at the edge

    x = np.roll(
        p,
        dx,
        axis=0
    )

    y = np.roll(
        p,
        dy,
        axis=1
    )

    z = np.roll(
        p,
        dz,
        axis=2
    )

    # Direction selection
    choose = ch3(
        x, y, z
    )

    # XYZ majority
    majority = maj3(
        x, y, z
    )

    # 64-bit rotation
    rx = rotl64(
        x,
        r1
    )

    ry = rotr64(
        y,
        r2
    )

    rz = rotl64(
        z,
        r3
    )

    # uint64 addition automatically
    # wraps modulo 2^64

    with np.errstate(
        over="ignore"
    ):

        t1 = (
            rx
            + choose
            + K3D[t]
        )

        t2 = (
            ry
            + majority
        )

    t3 = (
        rz
        ^ p
    )

    new_state = (
        t1
        ^
        t2
        ^
        rotl64(
            t3,
            r4
        )
    )

    return new_state


# ============================================================
# Count changed bits
# ============================================================

def count_changed_bits(diff):

    total = 0

    for value in diff.ravel():

        total += (
            int(value).bit_count()
        )

    return total


# ============================================================
# Avalanche Test
# ============================================================

def run_test():

    print()
    print(
        "3DH-v1 "
        "Schedule Candidate A"
    )

    print(
        "================================"
    )

    print(
        "Grid       :",
        N,
        "x",
        N,
        "x",
        N
    )

    total_cells = (
        N ** 3
    )

    total_bits = (
        total_cells * 64
    )

    print(
        "Cells      :",
        f"{total_cells:,}"
    )

    print(
        "Cell width : 64 bit"
    )

    print(
        "Rounds     :",
        ROUNDS
    )

    print(
        "Difference : 1 input bit"
    )

    print()

    # State A
    a = np.zeros(
        (N, N, N),
        dtype=np.uint64
    )

    # State B
    # Exactly one bit differs
    b = a.copy()

    b[0, 0, 0] = (
        np.uint64(1)
    )

    print(
        "round"
        "   dx"
        "   dy"
        "   dz"
        "   changed_cells"
        "   changed_bits_%"
    )

    start = (
        time.perf_counter()
    )

    for t in range(ROUNDS):

        a = mix_round(
            a,
            t
        )

        b = mix_round(
            b,
            t
        )

        if t in REPORT_ROUNDS:

            diff = (
                a ^ b
            )

            changed_cells = int(
                np.count_nonzero(
                    diff
                )
            )

            changed_bits = (
                count_changed_bits(
                    diff
                )
            )

            changed_percent = (
                100.0
                * changed_bits
                / total_bits
            )

            (
                dx,
                dy,
                dz,
                r1,
                r2,
                r3,
                r4
            ) = schedule(
                t,
                N
            )

            print(
                f"{t + 1:5d}"
                f" {dx:4d}"
                f" {dy:4d}"
                f" {dz:4d}"
                f" {changed_cells:15d}"
                f" {changed_percent:16.6f}"
            )

    elapsed = (
        time.perf_counter()
        - start
    )

    print()

    print(
        "Elapsed:",
        f"{elapsed:.6f}",
        "seconds"
    )

    print()

    print(
        "IMPORTANT:"
    )

    print(
        "A result near 50% "
        "shows avalanche diffusion."
    )

    print(
        "It does NOT prove "
        "cryptographic security."
    )

    print()


# ============================================================
# Start
# ============================================================

if __name__ == "__main__":
    run_test()
EOF