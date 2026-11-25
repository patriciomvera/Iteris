#!/usr/bin/env python3
"""Checks for Section 3 of "Rational Numerals and Carry Geometry in Iteris".

* Theorem 1: for every reduced denominator q < 4000 the block division rule in
  base B = 10**4 gives exactly t = ceil(max(a, b) / 4) prefix blocks and, when
  M > 1, a period of ord_M(B) = ord_M(10) / gcd(ord_M(10), 4) blocks.  Every
  numerator p coprime to q is tested for q < 600; for larger q, the numerators
  1, 2, 7, q - 1 and a deterministic sample are tested.
* Proposition 1: a well-formed numeral is canonical exactly when it equals
  N(V(w)).  Checked by exhaustive enumeration of short numerals in the small
  bases 2, 3, 4, 5 and 10, and over a restricted block alphabet in base 10**4.

Standard library only.  Run from the repository root:
    python paper/iteris_extra_checks.py
"""
from fractions import Fraction
from itertools import product
from math import gcd
import random


def order(a, m):
    k, x = 1, a % m
    while x != 1:
        x = x * a % m
        k += 1
    return k


def to_blocks(n, base):
    if n == 0:
        return (0,)
    out = []
    while n:
        out.append(n % base)
        n //= base
    return tuple(reversed(out))


def division_rule(x, base):
    """N(x): sign, integer word, prefix, cycle."""
    x = Fraction(x)
    sign = -1 if x < 0 else 1
    p, q = abs(x).numerator, abs(x).denominator
    whole, r = divmod(p, q)
    seen, blocks = {}, []
    while r and r not in seen:
        seen[r] = len(blocks)
        b, r = divmod(base * r, q)
        blocks.append(b)
    if r == 0:
        return sign, to_blocks(whole, base), tuple(blocks), ()
    j = seen[r]
    return sign, to_blocks(whole, base), tuple(blocks[:j]), tuple(blocks[j:])


def decode(sign, a, b, e, base):
    v = Fraction(sum(d * base ** (len(a) - 1 - i) for i, d in enumerate(a)))
    v += sum(Fraction(d, base ** (j + 1)) for j, d in enumerate(b))
    if e:
        c = sum(d * base ** (len(e) - 1 - i) for i, d in enumerate(e))
        v += Fraction(c, base ** len(b) * (base ** len(e) - 1))
    return sign * v


def primitive(w):
    n = len(w)
    return all(w != w[d:] + w[:d] for d in range(1, n) if n % d == 0)


def conditions(sign, a, b, e, base):
    """Conditions (1)-(5) of Section 3."""
    if not (a[0] != 0 or len(a) == 1):
        return False
    if sign < 0 and not any(a + b + e):
        return False
    if not e:
        return not b or b[-1] != 0
    if not primitive(e) or e in ((0,), (base - 1,)):
        return False
    return not b or b[-1] != e[-1]


def check_theorem1(limit=4000, full_below=600):
    B = 10 ** 4
    rng = random.Random(20261125)
    cases = 0
    for q in range(1, limit):
        a = b = 0
        M = q
        while M % 2 == 0:
            M //= 2
            a += 1
        while M % 5 == 0:
            M //= 5
            b += 1
        t = -(-max(a, b) // 4)
        ell = 0
        if M > 1:
            L = order(10, M)
            ell = order(B, M)
            assert ell == L // gcd(L, 4), q
        if q < full_below:
            numerators = range(q)
        else:
            numerators = {1, 2, 7, q - 1} | {rng.randrange(1, q) for _ in range(8)}
        for p in numerators:
            if gcd(p, q) != 1:
                continue
            for x in (Fraction(p, q), Fraction(-p - 3 * q, q)):
                _, _, pre, cyc = division_rule(x, B)
                assert len(pre) == t and len(cyc) == ell, (p, q)
                assert decode(*division_rule(x, B), B) == x
                cases += 1
    print(f"Theorem 1: {cases:,} rationals with q < {limit} checked")


def check_proposition1():
    total = 0
    settings = [(2, 3, 4), (3, 3, 3), (4, 2, 3), (5, 2, 3), (10, 2, 2)]
    for base, max_prefix, max_cycle in settings:
        digits = range(base)
        count = 0
        integer_words = [w for n in (1, 2) for w in product(digits, repeat=n)]
        for a in integer_words:
            for sign in (1, -1):
                for lp in range(max_prefix + 1):
                    for b in product(digits, repeat=lp):
                        for lc in range(max_cycle + 1):
                            for e in product(digits, repeat=lc):
                                w = (sign, a, b, e)
                                canonical = division_rule(decode(*w, base), base) == w
                                assert canonical == conditions(*w, base), (base, w)
                                count += 1
        print(f"Proposition 1, base {base}: {count:,} numerals enumerated")
        total += count
    B = 10 ** 4
    alphabet = (0, 1, 5000, B - 2, B - 1)
    count = 0
    for a in ((0,), (1,), (0, 1), (1, 0)):
        for sign in (1, -1):
            for lp in range(3):
                for b in product(alphabet, repeat=lp):
                    for lc in range(4):
                        for e in product(alphabet, repeat=lc):
                            w = (sign, a, b, e)
                            canonical = division_rule(decode(*w, B), B) == w
                            assert canonical == conditions(*w, B), w
                            count += 1
    print(f"Proposition 1, base 10^4 restricted alphabet: {count:,} numerals")
    return total + count


def check_examples():
    B = 10 ** 4
    expected = {
        Fraction(1, 6): ((1666,), (6666,)),
        Fraction(1, 7): ((), (1428, 5714, 2857)),
        Fraction(1, 30000): ((0,), (3333,)),
        Fraction(-314159, 100000): ((1415, 9000), ()),
        Fraction(1, 17): ((), (588, 2352, 9411, 7647)),
        Fraction(1, 101): ((), (99,)),
    }
    for x, (pre, cyc) in expected.items():
        assert division_rule(x, B)[2:] == (pre, cyc), x
    assert pow(10, 8, 17) == 16
    print("Section 3 worked examples: all match")


if __name__ == "__main__":
    check_examples()
    check_theorem1()
    check_proposition1()
    print("All Section 3 checks passed.")
