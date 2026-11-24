# Iteris Core v1.0

**Status** · Draft for review  
**Author** · Patricio M. Vera, simbionte.org

This draft builds on Notation v0.2 and Gemini's consolidation of the quadrant geometry, parser, and validation examples. Iteris uses a vertical Cistercian convention to write each block of four decimal digits as a single spatial glyph. The reference layout arranges those glyphs in a horizontal row. [Notation v0.2](history/ITERIS_NOTATION_02.md) · [Cistercian numerals](https://mathworld.wolfram.com/CistercianNumerals.html)

## Values and node order

Let $B = 10^4$. A canonical numeral has a sign $s$, an integer chain $[a_k, \ldots, a_0]$, a possibly empty fractional prefix $[b_1, \ldots, b_m]$, and an optional nonempty period. Every node value is an integer in `0..9999`. The nodes are listed in reading order, most significant first. A terminating numeral has no period and represents a signed finite decimal value.

$$
x = s\left(\sum_{i=0}^{k} a_i B^{i} + \sum_{j=1}^{m} b_j B^{-j}\right),\qquad s \in \{-1, +1\}.
$$

1. The integer chain has at least one node. Its first node is nonzero whenever the chain has more than one node.
2. A terminating numeral has an empty fractional prefix for an integer. Its last fractional node is nonzero when the prefix is nonempty.
3. A recurring numeral has the shortest prefix and shortest nonempty period found by the repeated-remainder rule below. Every zero node in the prefix or period occupies a full position, including a zero at the end of the prefix.
4. Zero has sign `+1`, integer chain `[0000]`, an empty prefix and no period. A minus sign precedes a negative numeral.

For uniqueness among terminating numerals, compare two equal values at the same precision by appending zero nodes to the shorter fractional prefix and multiplying both magnitudes by the resulting power of $B$. The resulting integers have the same base-$B$ digits. Removing the extra fractional zeros recovers the same canonical chains. Rule 4 and the sign of the represented value determine the sign.

## Finite decimal conversion

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

An empty prefix has $a=0$ and $P=0$. Digit counts include leading zeros. A period consisting entirely of zeros or entirely of nines denotes a terminating value and takes the canonical finite representation. For example, `0.12(0)` becomes `0.12`, `0.12(9)` becomes `0.13`, and `0.(9)` becomes `1`. A mixed period such as `0.(09)` remains recurring.

### Canonical base-10,000 sequence

Write the absolute value as a reduced fraction $n/q$ with $q>0$. The integer part is $\lfloor n/q \rfloor$, and the initial fractional remainder is $r_0 = n \bmod q$. Use integer arithmetic for each step.

1. Before producing a node, check the current remainder. A zero remainder ends the fractional sequence. A remainder already seen marks the start of the repeating part at the position where that remainder first appeared.
2. Otherwise, record the current remainder and its node position. Emit the quotient $\lfloor Br_i/q \rfloor$ as a four-digit node and set $r_{i+1} = Br_i \bmod q$.

The recurring representation contains the nodes before the first occurrence of the repeated remainder, followed by one copy of the cycle. At each node boundary the remaining fractional value is $r_i/q$. Equal remainders therefore give equal continuations, and a recurring sequence of nodes returns to the same remainder. The first repeated remainder yields the shortest prefix and shortest nonempty cycle in base 10,000. The cycle is measured in complete nodes, including zeros within the prefix or cycle.

To read the value back, interpret the $p$ nodes under the overbar as a base-$B$ integer $C$, with their leading zero nodes counted in $p$. When $m$ fractional nodes precede the cycle, its contribution to the magnitude is $C / \bigl(B^m(B^p - 1)\bigr)$. The sign applies to the whole result.

### Recurring examples

| Value | Input | Fractional prefix | Nodes under the overbar |
| --- | --- | --- | --- |
| $1/3$ | `0.(3)` | Empty | `[3333]` |
| $1/6$ | `0.1(6)` | `[1666]` | `[6666]` |
| $1/7$ | `0.(142857)` | Empty | `[1428] [5714] [2857]` |
| $1/30000$ | `0.0000(3)` | `[0000]` | `[3333]` |
| $1/11$ | `0.(09)` | Empty | `[0909]` |

## Node geometry

A node has height $H$, with the stem at $x=0$ from $y=0$ to $y=H$. Coordinates grow to the right and downward. Each quadrant has width $W=H/5$. The upper drawing region lies between $u=H/10$ and $v=3H/10$. The lower region is its reflection through the midpoint of the node. The reference drawings use $H=100$ and may be scaled uniformly.

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

## Horizontal reference layout

Read the row from left to right. A minus sign appears first for a negative numeral. Place the integer nodes next, then the radix point if the fraction has a prefix or a period. Place the fractional prefix after the radix point and append one copy of the period when present. The overbar marks exactly the nodes in that period. [Interactive demo](../demo/index.html)

- Start at $x=0$ and allocate adjacent slots from left to right. Each node occupies a slot of width $3W$. The stem is centered in its slot and spans $y=0$ to $y=H$. A zero occupies a full slot and shows the bare stem.
- The minus sign and radix point each occupy a slot of width $W$. Center each mark horizontally in its slot and vertically at $y=H/2$. The minus stroke has length $3H/25$. The radix point has radius $H/40$.
- Draw the continuous overbar at $y=-H/10$, from $W$ to the left of the first repeating node's stem to $W$ to the right of the final repeating node's stem.
- Cell outlines and decimal labels may guide readers. The marks that encode the numeral are the stems and their strokes, the sign, the radix point and the overbar.

The reference chart shows all 36 nonzero digit placements, zero nodes, periods and notation examples. [Reference chart](assets/iteris_reference.svg)

### Vertical variant for terminating numerals

The vertical variant stacks each chain downward, with one continuous stem of length $H$ times its node count. The integer and fractional stems start at the same height on axes $x=0$ and $x=4W$. The radix point, when present, is centered at $(2W,H/2)$ with radius $H/40$. The minus sign is centered at $(-2W,H/2)$ and has length $3H/25$. This is the default layout of the Python renderer. [SVG renderer](../iteris/svg.py)

Every nonzero digit contributes a segment reaching distance $W$ from its stem. In an ideal uniformly scaled vertical drawing, that distance yields $H$ on any chain with a nonzero node. Its stem length then yields the node count, including blank positions. A bare integer stem represents zero.

## Numerals in mathematical expressions

Replace each numeral with its Iteris glyph row at the same place in the expression. Operators, grouping marks, variable names, and the precedence of the expression retain their usual meanings.

- In $2^{10{,}000}$, place the glyph for $2$ at the base position and the whole row `[0001] [0000]` at superscript scale as one exponent.
- In $|0|$, place the absolute-value bars outside the zero node's slot, extending above and below its stem. The centered stem belongs to the numeral.
- The minus in $-2^2$ remains outside the scope of the exponentiation. Parentheses in $(-2)^2$ keep the minus within the base.
- In $1/3$, the fraction bar can separate the glyphs for numerator and denominator. The recurring numeral `0.(3)` is another exact way to write the value. Constants such as $\pi$ retain their symbolic forms.

## Scope

The Python reference codec covers finite decimals. The horizontal demo also renders recurring decimals using the canonical rational representation. Reading accuracy at finite display sizes remains an empirical question. The review tracks the open rules for recursive notation, radial layouts, and quantum interpretations. [Review of Gemini's proposals](ITERIS_REVIEW.md)
