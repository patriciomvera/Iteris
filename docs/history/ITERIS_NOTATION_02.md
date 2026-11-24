# Iteris Notation Specification v0.2

**Status:** Open Specification — Work in Progress  
**Origin:** Corpus Christi, Chile, April 2026  
**Author:** Patricio M. Vera  
**Reviewers:** Claude (Anthropic), Gemini (Google), ChatGPT (OpenAI)  
**Published by:** simbionte.org

> *"A number begins as a stem. How far it grows depends only on what it needs to say."*

---

## Changelog v0.1 → v0.2

- **Foundational reframe:** Iteris formally defined as a positional system in base B = 10⁴
- **Section 2:** Formal mathematical definition added
- **Section 4:** Radix anchor — decimal point formalized as exponent boundary, not typographic convention
- **Section 6:** Canonical Representation Rules — new section, closes all open ambiguities
- **Section 7:** Explicit Core / Extended separation — hyper-operations and quantum moved out of Core
- **Removed from Core:** Hyper-operation transition operator
- **Clarified:** Padding is visual only, not semantic
- **Clarified:** The "problem of context" is a standard property of positional systems, not a defect

---

## Guiding Principle

**Iteris is a base-10,000 spatial writing system with a canonical vertical rendering.**

It replaces how numbers are written, not how they are operated upon. The decimal system remains the foundation. All mathematical operators (+, −, ×, ÷, =, ∞, i) are preserved unchanged. Iteris defines only the visual encoding of numerical magnitude.

---

## 1. Historical Foundation

The Cistercian monks (c. 1200–1500 CE) developed a numeral notation in which a single glyph represents any integer from 1 to 9,999. Operating under a vow of silence across 500+ monasteries spanning medieval Europe, they required a compact, unambiguous written system.

Their solution: a vertical stem divided into four spatial quadrants, each encoding one decimal digit (0–9) through a vocabulary of line strokes. Place value is determined by quadrant position, not symbol length or sequence.

Iteris extends this system formally, preserving its spatial encoding principle while removing its upper bound.

---

## 2. Formal Definition

### 2.1 Base

Iteris Core is a positional notation system in base:

```
B = 10⁴ = 10,000
```

Every finite number in Iteris Core is represented as:

```
x = sign · ( Σ aᵢ · Bⁱ  +  Σ bⱼ · B⁻ʲ )
              i=0..k        j=1..m
```

Where each aᵢ and bⱼ ∈ {0, ..., 9999}.

### 2.2 The Node

A Node is a single base-10,000 digit. It is not a number by itself — it is a digit whose positional value is determined by its location relative to the radix anchor.

Just as the decimal digit `7` can mean 7, 70, 700, or 0.07 depending on position, a Node's value depends on its place in the chain. This is not ambiguity — it is standard positional notation.

Visually, a Node consists of:
- A vertical **stem**
- **Four quadrants** around the stem midpoint
- Each quadrant encodes one decimal digit (0–9)

```
  ← D2  │  D1 →
  ───────┼───────
  ← D4  │  D3 →
```

| Quadrant | Position | Place value |
|----------|----------|-------------|
| D1 | Top-right | Units (1s) |
| D2 | Top-left | Tens (10s) |
| D3 | Bottom-right | Hundreds (100s) |
| D4 | Bottom-left | Thousands (1,000s) |

One Node encodes a value from 0000 to 9999.

### 2.3 The Stem

The stem is a single vertical line — the base state of the system.

```
│
```

The stem alone represents **zero**. It is the unique canonical form of 0.

### 2.4 The Digit Vocabulary

Zero is the stem itself. Quadrants only carry values 1–9.

| Digit | Description | Type |
|-------|-------------|------|
| 0 | No stroke — zero is the stem | Base state |
| 1 | Horizontal at near edge | Primitive |
| 2 | Horizontal at far edge | Primitive |
| 3 | Diagonal — near-stem to far corner | Primitive |
| 4 | Diagonal — far corner to stem | Primitive |
| 5 | 1 + 4 | Composite |
| 6 | Vertical on outer edge | Primitive |
| 7 | 6 + 1 | Composite |
| 8 | 6 + 2 | Composite |
| 9 | 6 + 1 + 2 — three sides, open toward stem | Composite |

Same strokes apply in all quadrants. Orientation changes by position: mirrored horizontally for left quadrants, mirrored vertically for bottom quadrants.

### 2.5 Visual Proportions

```
  10% │ top padding
  20% │ upper digit area  (D1 / D2)
  40% │ bare stem — separation zone
  20% │ lower digit area  (D3 / D4)
  10% │ bottom padding
```

---

## 3. The Chain

For numbers requiring more than one base-10,000 digit, Nodes chain vertically downward.

```
┌─────────────┐
│   Node k    │  ← most significant digit
├─────────────┤
│   ...       │
├─────────────┤
│   Node 0    │  ← least significant digit
└─────────────┘
```

The stem is continuous — the spine of the entire number.

### 3.1 Range by Chain Length

| Nodes | Maximum value |
|-------|--------------|
| 1 | 9,999 |
| 2 | 99,999,999 |
| 3 | 999,999,999,999 |
| N | 10^(4N) − 1 |

### 3.2 Self-Similarity

The chain grows following the same reading order as the quadrants within each Node. Macro structure mirrors micro structure.

---

## 4. The Radix Anchor

The decimal point in Iteris is a **formal radix anchor** — not a typographic convention.

- Nodes to the **left** of the anchor belong to exponents B⁰, B¹, B², ...
- Nodes to the **right** of the anchor belong to exponents B⁻¹, B⁻², B⁻³, ...

This fully resolves the "problem of context": a Node derives its value from its position relative to the anchor, exactly as any digit does in any positional system.

---

## 5. Special Values

All use standard mathematical notation. No new symbols are introduced.

### 5.1 Zero
Stem alone. Unique canonical form.

### 5.2 Negative Numbers
Standard **−** precedes the chain. Never encoded in Node structure.

### 5.3 Rational Numbers
Standard division bar between two chains:
```
[chain a] / [chain b]
```

### 5.4 Decimal Numbers
Standard point as radix anchor between integer and fractional chains.
```
3.1415  →  [Node: 3] . [Node: 1415]
0.07    →  [stem]   . [Node: 0700]
```

### 5.5 Irrational and Transcendental Numbers
Infinite chain + standard **∞** marker. Precision specified by number of Nodes shown.

### 5.6 Complex Numbers
Two parallel chains + standard **i**:
```
[chain a] + [chain b]i
```

### 5.7 Scientific Notation
Standard × and superscript Node:
```
[Node] × [Node]^[Node-superscript]
```
Superscript Node rendered at reduced scale, sufficient to be visually distinct. Exact scale left to renderer.

---

## 6. Canonical Representation Rules

These rules ensure that every number has exactly one valid Iteris representation, and every Iteris representation decodes to exactly one number.

### Rule 1 — Base
Iteris Core is positional notation in base B = 10⁴.

### Rule 2 — Node value
Each Node encodes exactly one base-10,000 digit in {0, ..., 9999}.

### Rule 3 — Integer canonical form
Integers decompose uniquely into base-10,000 digits with **no leading zero Nodes**.

```
42      →  [Node: 0042]              ✓
10000   →  [Node: 0001][Node: 0000]  ✓
[0000][Node: 0042]                   ✗  (leading zero Node not canonical)
```

### Rule 4 — Fractional canonical form
Finite decimals are **normalized by removing trailing decimal zeros** before decomposition.

```
0.0700  ≡  0.07   (same canonical form)
1.2300  ≡  1.23   (same canonical form)
```

Iteris encodes value, not input format.

### Rule 5 — Rendering padding
Zero-padding inside the last fractional Node is **visual only** — it carries no additional semantic precision.

```
0.07  →  fractional block: [0700]
         trailing zeros are padding, not extra decimal places
```

### Rule 6 — Radix anchor
The decimal point separates nonnegative powers (integer Nodes) from negative powers (fractional Nodes) of B.

### Rule 7 — Zero
The stem alone is the unique canonical form of zero.

### Rule 8 — Sign
Negativity encoded only by the standard minus sign. Never by Node structure.

### Rule 9 — Uniqueness
Given these rules, every finite number with a terminating base-10,000 expansion has exactly one canonical Iteris form. Two expressions represent the same number if and only if they share the same canonical form after normalization.

---

## 7. Core vs. Extended

Iteris Core (this document) defines the positional notation system only. The following belong to separate specifications under development:

| Feature | Document |
|---------|----------|
| Hyper-operation transition operator | ITERIS_EXTENDED (planned) |
| Graham Number representation | ITERIS_EXTENDED (planned) |
| Qudit isomorphism | ITERIS_QUANTUM (planned) |
| Node parity constraint (ℤ₁₀) | ITERIS_QUANTUM (planned) |
| Phase homomorphism | ITERIS_QUANTUM (planned) |
| MPS / Hamiltonian analogy | ITERIS_QUANTUM (planned) |
| 3D Node extension | ITERIS_EXTENDED v2.0 (planned) |

**Why the separation matters:** the chain notation carries a complete positional semantics for integers and decimals. Layering hyper-operation semantics on the same chain requires an explicit mode marker — one that cannot be confused with ordinary positional reading. That formalization belongs in the Extended spec, not here.

---

## 8. Information Density

### 8.1 Per Node
- Possible values: 10,000
- Information: log₂(10,000) ≈ **13.3 bits**

### 8.2 Comparison

| System | Number | Cost |
|--------|--------|------|
| Decimal | 9,999 | 4 characters |
| Roman | 9,999 | 13 characters |
| Binary | 9,999 | 14 bits |
| **Iteris** | **9,999** | **1 Node** |
| Decimal | 99,999,999 | 8 characters |
| **Iteris** | **99,999,999** | **2 Nodes** |

Compression: **4 decimal digits per Node**, regardless of magnitude.

### 8.3 Honest Limitations

**Where Iteris helps:** large integers, dates, identifiers, dense numerical sequences.

**Where it is neutral or worse:** simple fractions, small decimals, everyday arithmetic. The system is a notation tool, not a universal compressor.

---

## 9. Mathematical Operations

All standard symbols preserved unchanged. Iteris replaces only number representation.

---

## 10. Roadmap

### Core v1.0
- [x] Node structure and quadrants
- [x] Zero as stem
- [x] Reading order and self-similarity
- [x] Digit vocabulary (strokes 0–9)
- [x] Formal definition as base-10,000 positional system
- [x] Canonical Representation Rules (Section 6)
- [x] Radix anchor formalization
- [x] Core / Extended separation
- [x] All special values using standard notation
- [ ] Visual reference chart — all 36 digit glyphs
- [ ] Formal parser specification
- [ ] Edge case validation

### Extended (future)
- [ ] Hyper-operation operator specification
- [ ] Iteris Quantum specification
- [ ] Python library
- [ ] arXiv submission

---

## 11. Origin

Iteris was conceived on Corpus Christi, April 2026, in Chile.  
The name derives from the Latin *iter* — journey, path, traversal.

Inspired by the Cistercian numeral system documented by David A. King in *The Ciphers of the Monks* (Franz Steiner Verlag, 2001).

---

*Iteris Notation v0.2 — simbionte.org — 2026*  
*Patricio M. Vera*
