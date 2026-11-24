# Iteris Core v1.0

**Status** · Draft for review  
**Author** · Patricio M. Vera, simbionte.org

This draft builds on Notation v0.2 and Gemini's consolidation of the quadrant geometry, parser, and validation examples. Iteris uses a vertical Cistercian convention to write each block of four decimal digits as a single spatial glyph. A continuous stem connects the blocks of each chain. [Notation v0.2](history/ITERIS_NOTATION_02.md) · [Cistercian numerals](https://mathworld.wolfram.com/CistercianNumerals.html)

## Values and node order

Let $B = 10^4$. The domain is the signed finite decimal values, equivalently integers divided by nonnegative powers of ten. Each value is represented by a sign $s$, an integer chain $[a_k, \ldots, a_0]$, and an optional fractional chain $[b_1, \ldots, b_m]$. Every node value is an integer in `0..9999`. Both chains start with their most significant node.

$$
x = s\left(\sum_{i=0}^{k} a_i B^{i} + \sum_{j=1}^{m} b_j B^{-j}\right),\qquad s \in \{-1, +1\}.
$$

1. The integer chain has at least one node. Its first node is nonzero whenever the chain has more than one node.
2. The fractional chain is empty for integers. A nonempty fractional chain ends in a nonzero node.
3. A zero node anywhere else in a chain occupies one full position. A leading fractional zero contributes to the exponent of every node below it.
4. Zero has sign `+1`, integer chain `[0000]`, and an empty fractional chain. A minus sign precedes a negative value.

For uniqueness, two equal representations can be compared at the same precision by appending zero nodes to the shorter fractional chain and multiplying both magnitudes by the resulting power of $B$. The resulting integers have the same base-$B$ digits. Removing the extra fractional zeros recovers the same canonical chains. The sign is unique by rule 4 and the sign of the represented value.

## Decimal conversion

After trimming surrounding whitespace, the encoder accepts `[+-]?[0-9]+(?:\.[0-9]+)?`. Strip leading integer zeros and retain one digit for an empty integer part after stripping. Strip trailing fractional zeros. Right-align the integer digits and left-align the fractional digits into four-digit blocks, padding the exposed ends with zeros. Normalize signed zero to positive. Padding carries no precision metadata.

To decode, write the first integer node in decimal and pad every subsequent integer node to four digits. Pad every fractional node to four digits before joining them, then strip trailing zeros from the joined fraction. Include the radix point when a fractional part remains and the minus sign on a negative value. The reference implementation performs these steps and validates manually constructed nodes and chains. [Python codec](../iteris/core.py)

| Input | Integer nodes | Fractional nodes | Canonical decimal |
| --- | --- | --- | --- |
| `-0.00` | `0000` | | `0` |
| `9999` | `9999` | | `9999` |
| `10000` | `0001 0000` | | `10000` |
| `100000000` | `0001 0000 0000` | | `100000000` |
| `100000005` | `0001 0000 0005` | | `100000005` |
| `0.0700` | `0000` | `0700` | `0.07` |
| `0.00000001` | `0000` | `0000 0001` | `0.00000001` |
| `-3.14159` | `0003` | `1415 9000` | `-3.14159` |

## Reference geometry

A node has height $H$, with the stem at $x=0$ from $y=0$ to $y=H$. Coordinates grow to the right and downward. The reference renderer sets the width of each quadrant to $W=H/5$. The upper drawing region lies between $u=H/10$ and $v=3H/10$. The lower region is its reflection through the midpoint of the node.

| Quadrant | Position | Weight | Transform from D1 |
| --- | --- | --- | --- |
| D1 | Upper right | 1 | $(x,y)$ |
| D2 | Upper left | 10 | $(-x,y)$ |
| D3 | Lower right | 100 | $(x,H-y)$ |
| D4 | Lower left | 1,000 | $(-x,H-y)$ |

| Primitive | D1 segment endpoints |
| --- | --- |
| `p1` | `(0,u)` to `(W,u)` |
| `p2` | `(0,v)` to `(W,v)` |
| `p3` | `(0,u)` to `(W,v)` |
| `p4` | `(W,u)` to `(0,v)` |
| `p6` | `(W,u)` to `(W,v)` |

| Digit | Primitives | Digit | Primitives |
| --- | --- | --- | --- |
| 0 | Empty | 5 | `p1 p4` |
| 1 | `p1` | 6 | `p6` |
| 2 | `p2` | 7 | `p1 p6` |
| 3 | `p3` | 8 | `p2 p6` |
| 4 | `p4` | 9 | `p1 p2 p6` |

Each chain has one continuous stem of length $H$ times its node count. The integer and fractional stems start at the same height on axes $x=0$ and $x=4W$. When a fractional chain exists, the radix dot is centered at $(2W,H/2)$ with radius $H/40$. The minus sign is centered at $(-2W,H/2)$ and has length $3H/25$. The reference chart shows all 36 nonzero digit placements and examples with empty blocks. [Reference chart](assets/iteris_reference.svg)

Every nonzero digit contributes a segment reaching distance $W$ from its stem. For ideal vector geometry under uniform scaling, the lateral distance yields $H$ on any chain with a nonzero node. Its stem length then yields the node count, including all blank positions. A bare integer stem is the canonical zero integer part. Reading accuracy at finite display sizes is an empirical question.

## Scope

The canonical encoder covers finite decimal values. Arithmetic expressions, including fractions with nonterminating expansions, scientific notation, and complex numbers, can use ordinary mathematical syntax around Iteris numerals. The [review of Gemini's proposals](ITERIS_REVIEW.md) tracks the open rules for recursive notation, radial layouts, and quantum interpretations.
