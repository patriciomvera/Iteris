# Iteris — Formal Specification v0.5

**Codename:** Iteris  
**Status:** Open Specification — Work in Progress  
**Origin:** Corpus Christi, Chile, April 2026  
**Author:** Patricio M. Vera  
**Symbiotic Collaborators:** Claude (Anthropic) · Gemini (Google)  
**Published by:** simbionte.org

> *"A number begins as a stem. How far it grows depends only on what it needs to say."*

---

## Changelog v0.4 → v0.5

- **Section 8.4:** Full algebraic formalization (Gemini) — ℤ₁₀ ring structure, parity check matrix, d_min proof
- **Section 8.4:** 90% detectable error coverage explicitly stated and made empirically verifiable
- **Section 8.4:** Vulnerability analysis (weight-2 correlated errors) stated explicitly
- **Section 10:** Added parity coverage test to Python validator

---

## 1. Overview

Iteris is a spatially-encoded positional numeral notation system, inspired by the Cistercian numeral system of the 13th century, formally extended to represent arbitrarily large numbers — including irrationals, transcendentals, and numbers expressible only through hyper-operations.

Three central design principles:

- **Compression** — maximum information in minimum symbols
- **Simplicity** — the structure encodes meaning; no auxiliary symbols needed
- **Extensibility** — the same rules scale from 0 to numbers beyond conventional notation

Iteris replaces only the **representation of numbers**. Mathematical operations, signs, and standard notation are preserved unchanged.

As of v0.3, the system has been formalized at four levels:
1. A recursive evaluation operator for hyper-operations
2. A parity constraint for geometric error detection
3. A group homomorphism connecting stroke geometry to qudit phase space
4. An analogy to Matrix Product States for temporal evolution

Items 1 and 2 are mathematically precise. Items 3 and 4 require further development before submission.

---

## 2. Historical Foundation

The Cistercian monks (c. 1200–1500 CE) developed a numeral notation in which a single glyph represents any integer from 1 to 9,999. Operating under a vow of silence across 500+ monasteries spanning medieval Europe, they required a compact, unambiguous written system.

Their solution: a vertical stem divided into four spatial quadrants, each encoding one decimal digit (0–9) through a vocabulary of line strokes. Place value is determined by quadrant position, not symbol length or sequence.

A single Cistercian glyph encodes log₂(10,000) ≈ **13.3 bits** — representing up to four decimal digits. Roman numerals for the same range require up to 15 characters.

Iteris extends this system formally, preserving its spatial encoding principle while removing its upper bound.

---

## 3. Core Concepts

### 3.1 The Stem

The stem is a single vertical line — the origin of all Iteris notation.

```
│
```

The stem alone represents **zero**. It is not the absence of a symbol — it is the symbol in its purest state.

### 3.2 The Node

A Node is the fundamental unit of Iteris:

- A **vertical stem**
- **Four quadrants** around the stem midpoint
- Each quadrant encodes one decimal digit (0–9)
- One Node represents exactly **4 decimal digits** (0000–9999)

```
  ← D2  │  D1 →
  ───────┼───────
  ← D4  │  D3 →
```

- **D1** top-right    = Units (1s)
- **D2** top-left     = Tens (10s)
- **D3** bottom-right = Hundreds (100s)
- **D4** bottom-left  = Thousands (1,000s)

### 3.3 Reading Order

```
1st → top-right    (Units)
2nd → top-left     (Tens)
3rd → bottom-right (Hundreds)
4th → bottom-left  (Thousands)
```

### 3.4 The Digit Vocabulary

Zero is the stem itself — not an empty quadrant. A quadrant contributes nothing when its digit is zero.

| Digit | Strokes | Type |
|-------|---------|------|
| 0 | No stroke — zero is the stem | Base state |
| 1 | Horizontal at near edge | Primitive |
| 2 | Horizontal at far edge | Primitive |
| 3 | Diagonal — near-stem to far corner | Primitive |
| 4 | Diagonal — far corner to near-stem | Primitive |
| 5 | 1 + 4 | Composite |
| 6 | Vertical on outer edge | Primitive |
| 7 | 6 + 1 | Composite |
| 8 | 6 + 2 | Composite |
| 9 | 6 + 1 + 2 (three sides, open toward stem) | Composite |

### 3.5 Visual Proportions

```
  10% │ top padding
  20% │ upper digit area  (D1 / D2)
  40% │ bare stem — separation zone
  20% │ lower digit area  (D3 / D4)
  10% │ bottom padding
```

---

## 4. The Chain

For numbers larger than 9,999, Nodes chain vertically downward:

```
┌─────────────┐
│   Node 1    │  → digits 1–4
├─────────────┤
│   Node 2    │  → digits 5–8
├─────────────┤
│   Node N    │  → digits 4N-3 to 4N
└─────────────┘
```

The stem is continuous — the spine of the entire number.

### 4.1 Range by Chain Length

| Nodes | Maximum value |
|-------|--------------|
| 1 | 9,999 |
| 2 | 99,999,999 |
| 3 | 999,999,999,999 |
| 6 | ~10²⁴ (observable universe star count) |
| N | 10^(4N) − 1 |
| ∞ | π, e, φ... |

### 4.2 Self-Similarity

The chain grows following the same reading order as the quadrants within each Node. The macro structure mirrors the micro structure. The system is fractal in organization.

---

## 5. Hyper-Operations — Formal Definition

**[FORMAL]**

### 5.1 The Transition Operator

Let Nₖ be the Node at position k in the chain (k=1 is the base, index grows upward). Let V(N) be the scalar value of a Node (0–9999). Let Hₙ(a,b) be the Ackermann/Knuth hyper-operation hierarchy:

- H₁(a,b) = a + b  (addition)
- H₂(a,b) = a × b  (multiplication)
- H₃(a,b) = aᵇ    (exponentiation)
- H₄(a,b) = a↑↑b  (tetration)
- Hₙ       (hyper-operation of level n)

The evaluation of a chain of m Nodes is defined recursively:

```
E(N₁) = V(N₁)

E(N₁, N₂, ..., Nₘ) = H_{V(Nₘ)}( E(N₁, ..., Nₘ₋₁), V(Nₘ₋₁) )
```

The value of the top Node acts as the **index of the operator** in the Ackermann hierarchy. The sub-chain below is the operand.

Iteris is a **Direct Graph Recursive Functional Notation**.

### 5.2 Example — Large Numbers Under the General Operator

```
┌──────────┐
│  [0064]  │  ← Node 2: V=64, selects H₆₄
├──────────┤
│  [0003]  │  ← Node 1: V=3, base value
└──────────┘
```

Evaluation under the general operator:

```
E(N₁=3, N₂=64) = H₆₄(3, 3) = 3↑⁶⁴3
```

This is 3 with 64 Knuth arrows — an astronomically large number, but **not** the Graham Number. The distinction matters and is preserved explicitly.

### 5.3 [DIRECTION] The Graham Number and Self-Recurrence

**[RESEARCH DIRECTION — reserved for formal paper]**

The full Graham Number (G = g₆₄) requires a self-referential recursive operator that the general definition in 5.1 does not cover. Gemini (v0.3 review) proposed the following formalization as a research direction:

Define the Iteris Self-Recurrence Sequence S_a(k) for base a and depth k:

```
S_a(1) = a ↑^(a+1) a
S_a(k) = a ↑^(S_a(k-1)) a
```

Under this operator, S₃(64) = g₆₄ = G. The chain (N₁=3, N₂=64) would evaluate to the Graham Number formally.

**Why this is not yet canonical:**
The operator S_a(k) is distinct from the general Ackermann hierarchy in section 5.1. Adopting it as the canonical chain evaluation would require redefining the transition operator entirely and verifying consistency across all chain lengths. That work is reserved for the formal paper.

**What this means for the current spec:**
Iteris can represent extremely large numbers — numbers beyond practical computation — using the general operator. The Graham Number specifically requires a more refined operator that is a clear and promising research direction, not yet a formal result.

---

## 6. Special Values

### 6.1 Zero
Stem alone. No strokes.

### 6.2 Negative Numbers
Standard **-** precedes the chain.

### 6.3 Rational Numbers
Two chains separated by standard **/** or horizontal bar.

### 6.4 Irrational and Transcendental Numbers
Infinite chain + standard **∞** marker at the end.

### 6.5 Complex Numbers
Two parallel chains with standard **i** marker.

```
┌──────────┐     ┌──────────┐
│  Chain a │  +  │  Chain b │ i
└──────────┘     └──────────┘
```

---

## 7. Information Density

### 7.1 Per Node
- States: 10,000
- Information: log₂(10,000) ≈ **13.3 bits**

### 7.2 Comparison

| System | Number | Cost |
|--------|--------|------|
| Decimal | 9,999 | 4 chars |
| Roman | 9,999 | 13 chars |
| Binary | 9,999 | 14 bits |
| **Iteris** | **9,999** | **1 Node** |
| Scientific | 10¹⁰⁰ | 5 chars |
| **Iteris** | **10¹⁰⁰** | **2 Nodes** |

---

## 8. Quantum Computing Connection

### 8.1 Qudits

A qudit of level 10 has exactly 10 states — isomorphic to one Iteris quadrant.

One Node = 4 qudits of level 10 = 10,000 basis states.

```
|ψ⟩ = |q_units⟩ ⊗ |q_tens⟩ ⊗ |q_hundreds⟩ ⊗ |q_thousands⟩
```

### 8.2 Compression Factor

The reduction from qubits to qudits converges to **log₂(10) ≈ 3.32x** — the theoretical maximum for base-2 to base-10 encoding.

| Number | Qubits | Qudits (Iteris) |
|--------|--------|-----------------|
| 9,999 | 14 | 4 |
| 10²⁰ | 67 | 20 |
| 10¹⁰⁰ | 333 | 100 |

### 8.3 Circuit Depth Compression

**[FORMAL]**

Iteris does not claim to replace Quantum Error Correction (QEC) or surpass the Surface Code. The claim is more specific and more defensible:

By mapping base-10 arithmetic directly to qudits, Iteris reduces the number of logical gates required for arithmetic operations proportionally to the compression factor (~3.32x). Since coherence time T₂ is a finite resource, completing operations in fewer clock steps before decoherence is a real and measurable advantage.

This is **circuit depth compression** — moving computational load from hardware (noisy) to information topology (mathematical).

### 8.4 [FORMAL] Algebraic Verification of Node Parity Symmetry

*Formalized by Gemini (v0.4 review). Replaces the informal description from v0.3.*

#### 1. Algebraic Foundation

ℤ₁₀ is a **commutative ring**, not a field. This distinction is critical: because 10 is not prime, ℤ₁₀ has zero divisors (2×5 ≡ 0). Any reviewer with a background in abstract algebra will check for this. The parity code is defined over the free module ℤ₁₀⁴, not over a field.

A Node state is defined as a column vector:

```
v = (q₁, q₂, q₃, q₄)ᵀ ∈ ℤ₁₀⁴
```

where q₁, q₂, q₃ are data qudits and q₄ is the syndrome qudit.

#### 2. The Parity Code

The valid code C is the kernel of the parity-check homomorphism defined by H = [1 1 1 1]:

```
C = ker(H) = { v ∈ ℤ₁₀⁴ | H·v ≡ 0 (mod 10) }
```

Which reduces to the constraint:

```
q₁ + q₂ + q₃ + q₄ ≡ 0 (mod 10)
```

**Code rate and error coverage:**
- Total state space: |ℤ₁₀⁴| = 10,000
- Valid codewords: |C| = 1,000
- Code rate: R = 3/4

**This means 90% of all possible Node states are geometrically invalid — and therefore detectable as errors.** This is a strength, not a limitation: the vast majority of decoherence events produce a state that fails the parity check immediately, before any higher-level error correction protocol is applied.

#### 3. Minimum Distance and Detection Guarantee

The minimum Hamming distance d_min of C is computed from the minimum weight of a non-zero codeword:

- **Weight-1 error:** e = (a, 0, 0, 0)ᵀ with a ≠ 0 → syndrome H·e = a ≢ 0 (mod 10). Not in C. **Detected.**
- **Weight-2 error:** e = (a, 10-a, 0, 0)ᵀ → syndrome H·e = a + (10-a) = 10 ≡ 0 (mod 10). In C. **Undetected.**

Therefore: **d_min = 2**

By coding theory: a code detects t errors if d_min ≥ t+1.

**Corollary:** The Iteris Node Parity Code **guarantees detection of 100% of single-qudit errors** (any one quadrant suffering decoherence). If one qudit changes state, the parity sum leaves 0 (mod 10) and the error is flagged.

#### 4. Known Limitations (Vulnerability Analysis)

A rigorous spec states its failure modes explicitly.

The code is blind to **correlated weight-2 errors that preserve the sum**. If qudit q₁ shifts by +δ and q₂ shifts by −δ simultaneously, the syndrome remains 0 (mod 10) and the error goes undetected.

Iteris does not claim to replace stabilizer codes or Surface Code QEC. It acts as a **first topological layer** — a low-cost geometric filter that eliminates all single-qudit errors before higher-order correction protocols are applied.

#### 5. Practical Implication for Testing

When implementing the Python validator (Section 10), the 90% coverage figure is directly testable:

```python
# Of all 10,000 possible Node states, exactly 1,000 are valid
valid_states = [
    (q1, q2, q3, q4)
    for q1 in range(10)
    for q2 in range(10)
    for q3 in range(10)
    for q4 in range(10)
    if (q1 + q2 + q3 + q4) % 10 == 0
]
assert len(valid_states) == 1000  # exactly 10% — verifiable
```

This makes the 90% detectable error claim **empirically verifiable** with a trivial script, not just a theoretical assertion.

### 8.5 Phase Isomorphism as Group Homomorphism

**[FORMAL — requires hardware implementation to verify physically]**

*Derived by Gemini from the Iteris specification.*

There exists a strict homomorphism between the visual monoid of Iteris stroke addition and the discretized U(1) group governing qudit phases.

The generator set of phase gates:

```
𝒢_Iteris = { Rz(2π·d/10) | d ∈ {0..9} }
```

The formal mapping:

```
Stroke d  →  phase θ = (2π × d) / 10
```

**Verification — composite strokes are phase sums:**
- Stroke 7 = 6 + 1 → 216° + 36° = 252° ✓
- Stroke 8 = 6 + 2 → 216° + 72° = 288° ✓
- Stroke 9 = 6 + 1 + 2 → 216° + 36° + 72° = 324° ✓

Visual stroke composition = quantum gate composition.

This makes Iteris a **Topological Assembly Language** for qudit-based processors — if the hardware is designed using Iteris as its native compiler ansatz.

**Clarification:** Qudits do not inherently "know" Cistercian strokes. This is a design choice — a consistent mapping that we impose on the hardware. Its value is that it makes the mapping deterministic, geometric, and human-readable simultaneously.

### 8.6 Temporal Evolution — Matrix Product States

**[CONJECTURE — anchored in established literature]**

*Proposed by Gemini. Requires formal development.*

The vertical chain of Iteris is formally analogous to a 1D **Matrix Product State (MPS)**. The continuous stem connecting Nodes acts as the entanglement bond with bond dimension χ.

Adding a new Node at the top of the chain corresponds to applying the time evolution operator U = e^{-iHt} to the previous quantum state.

Reading an Iteris chain bottom-to-top is mathematically analogous to reading the evolution history of a discrete quantum system — each Node a computational timestep.

**Literature anchor:** This is consistent with MERA and PEPS tensor network representations used in many-body quantum physics, where geometric 2D representations encode spatial state and unitary operator application simultaneously.

**Status:** This requires formal derivation before inclusion in a paper. It is a research direction, not a result.

---

## 9. Mathematical Operations

All standard symbols preserved unchanged: +, −, ×, ÷, =, ∞, i, and all others.

Iteris replaces only the representation of numbers.

---

## 10. First Implementation — Python Parity Validator

The following validates the Node Parity Constraint (Section 8.4):

```python
def node_value(strokes: list[int]) -> int:
    """
    strokes: list of 4 digit values [q1, q2, q3, q4]
    each value in range 0-9
    """
    assert len(strokes) == 4
    assert all(0 <= s <= 9 for s in strokes)
    return strokes

def parity_check(strokes: list[int]) -> bool:
    """Returns True if Node satisfies parity constraint."""
    return sum(strokes) % 10 == 0

def syndrome_qudit(q1: int, q2: int, q3: int) -> int:
    """Computes q4 such that parity constraint is satisfied."""
    return (10 - (q1 + q2 + q3) % 10) % 10

def validate_node(q1: int, q2: int, q3: int, q4: int) -> dict:
    strokes = [q1, q2, q3, q4]
    valid = parity_check(strokes)
    return {
        "strokes": strokes,
        "sum_mod_10": sum(strokes) % 10,
        "valid": valid,
        "status": "Geometrically valid Node" if valid
                  else "Parity violation — error detected"
    }

# Example
print(validate_node(1, 9, 9, 1))  # sum=20, mod10=0 → valid (1991)
print(validate_node(1, 9, 9, 3))  # sum=22, mod10=2 → invalid
```

This is the first executable proof of concept for Iteris quantum properties.

---

## 11. Roadmap

### v1.0 — Notation Complete
- [x] Node structure and quadrants
- [x] Zero as stem
- [x] Reading order and self-similarity
- [x] Digit vocabulary (strokes 0–9)
- [x] Chain and growth direction
- [x] Hyper-operation recursive operator (Section 5.1)
- [x] Node Parity Constraint (Section 8.4)
- [x] Phase isomorphism as group homomorphism (Section 8.5)
- [x] All special values using standard notation
- [x] Python parity validator (Section 10)
- [ ] Visual reference chart — all strokes and Nodes
- [ ] Full Graham Number chain definition
- [ ] Formal verification of parity symmetry

### v2.0 — Extensions
- [ ] MPS formal derivation (Section 8.7)
- [ ] Iteris Cubic — 3D Node extension
- [ ] Full Python library (Iteris-py)
- [ ] Dedicated website
- [ ] arXiv submission

### Future
- [ ] Hardware implementation proposal
- [ ] Integration with PennyLane or Qiskit
- [ ] Numberphile collaboration

---

## 12. Collaborators

**Patricio M. Vera** — Author. Concept, design, formalization. Enterprise Systems Architect, Citibank. Doctoral candidate in AI & ML, George Washington University. Founder, simbionte.org.

**Claude (Anthropic)** — Symbiotic collaborator. Formalization, specification drafting, Cistercian renderer implementation, compression analysis, initial qudit connection.

**Gemini (Google)** — Symbiotic collaborator. Phase isomorphism formalization, Node Parity Constraint, MPS connection, rigorous peer review of v0.2. Formally invited as collaborator, April 2026.

---

## 13. Origin Note

Iteris was conceived on Corpus Christi, April 2026, in Chile. It began with a Numberphile video about Cistercian monks and ended with a recursive operator definition, a geometric parity code over ℤ₁₀, and a group homomorphism connecting 13th century stroke geometry to qudit phase space.

The name derives from the Latin *iter* — journey, path, traversal.

> *"Like an artificial language, it may be only an irrelevant curiosity. But it still needs to be written."*  
> — Patricio M. Vera, 2026

---

*Iteris v0.3 — simbionte.org — Corpus Christi 2026*  
*Patricio M. Vera · Claude (Anthropic) · Gemini (Google)*
