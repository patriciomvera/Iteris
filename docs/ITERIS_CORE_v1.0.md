# Iteris Core v1.0

**Status** · Draft for review  
**Author** · Patricio M. Vera, simbionte.org

This draft builds on Notation v0.2 and Gemini's consolidation of the quadrant geometry, parser, and validation examples. Iteris uses a vertical Cistercian convention to write each block of four decimal digits as a single spatial glyph. In the reference vertical layout, a continuous stem connects the blocks of each chain. [Notation v0.2](history/ITERIS_NOTATION_02.md) · [Cistercian numerals](https://mathworld.wolfram.com/CistercianNumerals.html)

## Values and node order

Let $B = 10^4$. A signed finite decimal value is an integer divided by a nonnegative power of ten. Its representation has a sign $s$, an integer chain $[a_k, \ldots, a_0]$, and an optional fractional chain $[b_1, \ldots, b_m]$. Every node value is an integer in `0..9999`. Both chains start with their most significant node. Recurring rational values add a repeating block sequence as defined below.

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

## Recurring decimals

The input grammar for a recurring decimal is `[+-]?[0-9]+\.[0-9]*\([0-9]+\)` after trimming surrounding whitespace. The digits in parentheses repeat indefinitely. For example, `0.1(6)` denotes $1/6$ exactly. If $I$ is the integer part, the fractional prefix has $a$ digits and integer value $P$, and the repeating part has $b$ digits and integer value $R$, the signed value is

$$
x = s\left(I + \frac{P}{10^a} + \frac{R}{10^a(10^b-1)}\right), \qquad b \ge 1.
$$

An empty prefix has $a=0$ and $P=0$. Digit counts include leading zeros. A recurring sequence of zeros or nines denotes a terminating value and has the canonical finite representation. For example, `0.12(0)` becomes `0.12`, `0.12(9)` becomes `0.13`, and `0.(9)` becomes `1`.

### Canonical base-10,000 sequence

Write the absolute value as a reduced fraction $n/q$ with $q>0$. The integer part is $\lfloor n/q \rfloor$, and the initial fractional remainder is $r_0 = n \bmod q$. Use integer arithmetic for each step.

1. Before producing a node, check the current remainder. A zero remainder ends the fractional sequence. A remainder already seen marks the start of the repeating part at the position where that remainder first appeared.
2. Otherwise, record the current remainder and its node position. Emit the quotient $\lfloor Br_i/q \rfloor$ as a four-digit node and set $r_{i+1} = Br_i \bmod q$.

The recurring representation contains the nodes before the first occurrence of the repeated remainder, followed by one copy of the cycle. At each node boundary the remaining fractional value is $r_i/q$. Equal remainders therefore give equal continuations, and a recurring sequence of nodes returns to the same remainder. The first repeated remainder yields the shortest prefix and shortest nonempty cycle in base 10,000. The cycle is measured in complete nodes, including zeros within the prefix or cycle.

To read the value back, interpret the $p$ nodes under the overbar as a base-$B$ integer $C$, with their leading zero nodes counted in $p$. When $m$ fractional nodes precede the cycle, its contribution to the magnitude is $C / \bigl(B^m(B^p - 1)\bigr)$. The sign applies to the whole result.

### Horizontal notation

The experimental horizontal layout draws nodes from left to right, keeping the vertical geometry of each individual glyph. The radix point separates the integer and fractional nodes. A continuous overbar starts above the first repeating node and ends above the last node of the cycle. For terminating values, the row has no overbar. [Interactive demo](../demo/index.html)

| Value | Input | Fractional prefix | Nodes under the overbar |
| --- | --- | --- | --- |
| $1/3$ | `0.(3)` | Empty | `[3333]` |
| $1/6$ | `0.1(6)` | `[1666]` | `[6666]` |
| $1/7$ | `0.(142857)` | Empty | `[1428] [5714] [2857]` |

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

The Python reference codec covers finite decimals. The horizontal demo also renders recurring decimals using the canonical rational representation. Arithmetic expressions, including fractions, scientific notation, and complex numbers, can use ordinary mathematical syntax around Iteris numerals. The review tracks the open rules for recursive notation, radial layouts, and quantum interpretations. [Review of Gemini's proposals](ITERIS_REVIEW.md)
