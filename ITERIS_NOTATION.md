# Iteris — Notation Specification v0.1

**Status:** Open Specification — Work in Progress  
**Origin:** Corpus Christi, Chile, April 2026  
**Author:** Patricio M. Vera  
**Published by:** simbionte.org

> *"A number begins as a stem. How far it grows depends only on what it needs to say."*

---

## Guiding Principle

Iteris is a **positional and spatial numerical notation system**.

It replaces how numbers are written, not how they are operated upon. The decimal system remains the foundation. Iteris is the representation.

All standard mathematical operations (+, −, ×, ÷, =) and symbols (∞, i, −) are preserved unchanged. Iteris only defines how a number looks, not what you do with it.

---

## 1. Historical Foundation

The Cistercian monks (c. 1200–1500 CE) developed a numeral notation in which a single glyph represents any integer from 1 to 9,999. Operating under a vow of silence across 500+ monasteries spanning medieval Europe, they needed a compact, unambiguous written system.

Their solution: a vertical stem divided into four spatial quadrants, each encoding one decimal digit (0–9) through a small vocabulary of line strokes. Place value is determined by quadrant position, not by symbol length or reading sequence.

A single Cistercian glyph encodes log₂(10,000) ≈ **13.3 bits** — representing up to four decimal digits in one symbol. Roman numerals for the same range require up to 15 characters.

Iteris extends this system formally, preserving its spatial encoding principle while removing its upper bound.

---

## 2. Core Elements

### 2.1 The Stem

The stem is a single vertical line. It is the origin of the system.

```
│
```

The stem alone represents **zero**. It is not the absence of a symbol — it is the symbol in its base state. Every Iteris number begins with the stem.

### 2.2 The Node

A Node is the fundamental unit of Iteris. It consists of:

- A vertical **stem**
- **Four quadrants** arranged around the stem midpoint
- Each quadrant encodes one decimal digit (0–9)
- One Node represents exactly **4 decimal digits** (0000–9999)

```
  ← D2  │  D1 →
  ───────┼───────
  ← D4  │  D3 →
```

| Position | Quadrant | Place value |
|----------|----------|-------------|
| Top-right | D1 | Units (1s) |
| Top-left | D2 | Tens (10s) |
| Bottom-right | D3 | Hundreds (100s) |
| Bottom-left | D4 | Thousands (1,000s) |

### 2.3 Reading Order

Within a Node, digits are read in this order:

```
1st → top-right    (Units)
2nd → top-left     (Tens)
3rd → bottom-right (Hundreds)
4th → bottom-left  (Thousands)
```

This follows the spiral pattern of the original Cistercian system.

### 2.4 The Digit Vocabulary

Zero is the stem itself — not an empty quadrant. When a digit is zero, its quadrant contributes nothing. The quadrants only exist to carry digits 1–9.

| Digit | Description | Type |
|-------|-------------|------|
| 0 | No stroke — zero is the stem | Base state |
| 1 | Horizontal at near edge (close to stem) | Primitive |
| 2 | Horizontal at far edge | Primitive |
| 3 | Diagonal — near-stem corner to far corner | Primitive |
| 4 | Diagonal — far corner back to stem | Primitive |
| 5 | 1 + 4 combined | Composite |
| 6 | Vertical on outer edge | Primitive |
| 7 | 6 + 1 | Composite |
| 8 | 6 + 2 | Composite |
| 9 | 6 + 1 + 2 — three sides of a square, open toward stem | Composite |

The same stroke shapes apply in all quadrants. Orientation changes by quadrant — mirrored horizontally for left quadrants, mirrored vertically for bottom quadrants.

### 2.5 Visual Proportions

```
  10% │ top padding
  20% │ upper digit area  (D1 / D2)
  40% │ bare stem — separation zone
  20% │ lower digit area  (D3 / D4)
  10% │ bottom padding
```

This ensures upper and lower digit areas never overlap, preserving spatial clarity at any scale.

---

## 3. The Chain — Numbers Beyond 9,999

For numbers larger than 9,999, Nodes chain vertically downward:

```
┌─────────────┐
│   Node 1    │  → digits 1–4      (units to thousands)
├─────────────┤
│   Node 2    │  → digits 5–8      (ten-thousands to tens of millions)
├─────────────┤
│   Node 3    │  → digits 9–12
├─────────────┤
│   Node N    │  → digits 4N-3 to 4N
└─────────────┘
```

The stem is continuous across all Nodes — the spine of the entire number.

### 3.1 Range by Chain Length

| Nodes | Maximum value |
|-------|--------------|
| 1 | 9,999 |
| 2 | 99,999,999 |
| 3 | 999,999,999,999 |
| 4 | 9,999,999,999,999,999 |
| N | 10^(4N) − 1 |

### 3.2 Self-Similarity

The chain grows downward following the same reading order as the quadrants within each Node. The macro structure mirrors the micro structure. The organization is fractal.

---

## 4. Hyper-Operations — Very Large Numbers

For numbers beyond direct positional representation, Node position encodes the level of operation implicitly.

### 4.1 The Transition Operator

Let Nₖ be the Node at position k (k=1 is the base). Let V(N) be the scalar value of a Node (0–9,999). Let Hₙ(a,b) be the Ackermann/Knuth hyper-operation:

- H₁(a,b) = a + b
- H₂(a,b) = a × b
- H₃(a,b) = aᵇ
- H₄(a,b) = a↑↑b (tetration)
- Hₙ = hyper-operation of level n

Evaluation of a chain of m Nodes:

```
E(N₁) = V(N₁)

E(N₁, ..., Nₘ) = H_{V(Nₘ)}( E(N₁, ..., Nₘ₋₁), V(Nₘ₋₁) )
```

The top Node selects the operator. The sub-chain below is the operand.

### 4.2 Example

Chain with N₁=3, N₂=64:

```
E(N₁=3, N₂=64) = H₆₄(3, 3) = 3↑⁶⁴3
```

This is an astronomically large number — but not the Graham Number. The distinction is explicit and maintained.

### 4.3 [RESEARCH DIRECTION] The Graham Number

The full Graham Number requires a self-referential recursive operator distinct from the general definition above. A candidate formalization (proposed by Gemini, 2026):

```
S_a(1) = a↑^(a+1) a
S_a(k) = a↑^(S_a(k-1)) a

Graham Number = S₃(64)
```

This is a research direction reserved for the formal paper, where it can be developed with full rigor and verified independently.

---

## 5. Special Values

All use standard mathematical notation — no new symbols introduced.

### 5.1 Zero
Stem alone. No strokes. No quadrant activity.

### 5.2 Negative Numbers
Standard **-** precedes the chain.
```
-[Node]  →  negative number
```

### 5.3 Rational Numbers
Standard division bar between two chains:
```
┌──────────┐
│  Chain a │  ← numerator
├══════════╡
│  Chain b │  ← denominator
└──────────┘
```

### 5.4 Irrational and Transcendental Numbers
Infinite chain with standard **∞** at the end.
```
[Node 1][Node 2]...[Node N] ∞
```
The precision (number of Nodes shown) is specified explicitly.

### 5.5 Complex Numbers
Two parallel chains with standard **i**:
```
┌──────────┐     ┌──────────┐
│  Chain a │  +  │  Chain b │ i
└──────────┘     └──────────┘
```

---

## 6. Information Density

### 6.1 Per Node
- Possible states: 10,000
- Information content: log₂(10,000) ≈ **13.3 bits**

### 6.2 Comparison

| System | Number | Cost |
|--------|--------|------|
| Decimal | 9,999 | 4 characters |
| Roman numerals | 9,999 | 13 characters (MMMCMXCIX) |
| Binary | 9,999 | 14 bits |
| **Iteris** | **9,999** | **1 Node** |
| Decimal | 99,999,999 | 8 characters |
| **Iteris** | **99,999,999** | **2 Nodes** |
| Decimal | 10^20 | 21 characters |
| **Iteris** | **10^20** | **5 Nodes** |

The compression ratio relative to decimal notation converges to **4 decimal digits per Node**, regardless of the magnitude of the number.

---

## 7. Mathematical Operations

All standard symbols are preserved unchanged:

| Symbol | Meaning |
|--------|---------|
| + − × ÷ = | Standard arithmetic |
| ∞ | Infinity / continuation |
| i | Imaginary unit |
| - | Negative sign |
| / | Division |
| All others | Unchanged |

Iteris replaces only the **representation of numbers**, never the language of operations.

---

## 8. Reference Implementation

A working renderer of the Cistercian base system (0–9,999) is available at:

**[cistercian-gamma.vercel.app](https://cistercian-gamma.vercel.app)**

Source: [github.com/patriciomvera/cistercian](https://github.com/patriciomvera/cistercian)

The Iteris chain renderer (multi-Node) is in development.

---

## 9. What This Document Does Not Cover

The following are intentionally excluded from this notation specification and are developed separately in `ITERIS_QUANTUM.md`:

- Connection to qudit-based quantum computing
- Node parity constraint as error detection
- Phase isomorphism with quantum states
- Circuit depth compression
- Matrix Product State analogy

Those are potential applications and research directions. This document defines the notation system itself — independent of any specific application.

---

## 10. Roadmap

- [x] Node structure and quadrants
- [x] Zero as stem
- [x] Reading order
- [x] Digit vocabulary (strokes 0–9)
- [x] Chain and growth direction
- [x] Hyper-operation transition operator
- [x] All special values using standard notation
- [ ] Visual reference chart — all 36 digit glyphs
- [ ] Full multi-Node renderer
- [ ] Formal paper on notation system

---

## 11. Origin

Iteris was conceived on Corpus Christi, April 2026, in Chile. The name derives from the Latin *iter* — journey, path, traversal.

Inspired by the Cistercian numeral system documented by historian David A. King in *The Ciphers of the Monks* (Franz Steiner Verlag, 2001), and popularized by Numberphile.

---

*Iteris Notation v0.1 — simbionte.org — 2026*  
*Patricio M. Vera*
