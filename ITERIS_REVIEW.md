# Review of Gemini’s Iteris proposals

[Project overview](README.md) · [Notation v0.2](ITERIS_NOTATION_02.md) · [Exploratory specification v0.5](ITERIS_SPEC_v05.md)

## Positional core

Notation v0.2 established base 10,000, vertical chains, the radix anchor, and canonical finite-decimal forms. Gemini’s consolidation made those rules implementable by specifying the quadrant strokes and reflections, the decimal parser, and the normalization examples. The [Core specification](ITERIS_CORE_v1.0.md) carries that work forward. It defines the domain of finite decimal values, the positive sign for zero, and the blocks that must survive normalization when their position carries value.

The useful visual test is whether a reader can recover the number from the continuous stem and strokes. Start with `9999`, `10000`, `100000000`, `100000005`, and `0.00000001`. Compare exact transcription and reading time with decimal digits grouped in fours after familiarization. Vary display size and include chains whose integer and fractional sides have different lengths.

## Extended notation

Under the v0.5 indexing, addition is `H₁`, multiplication is `H₂`, and exponentiation is `H₃`. For `n ≥ 3`, `Hₙ` uses `n − 2` Knuth arrows. The worked example `H₆₄(3, 3)` therefore uses 62 arrows. Gemini’s separate recurrence `S₃(64)` reproduces Graham’s number. It starts with four arrows between the two threes and uses the prior term as the next arrow count. [Graham recurrence](https://mathworld.wolfram.com/GrahamsNumber.html)

Specify a mode marker, permitted inputs, and the base cases before assigning either recursive interpretation to a chain. In Core, the unmarked chain `[0064][0003]` is the positional numeral `640003`. Test low-order examples and use symbolic evaluation for large expressions. Radial layouts and seals could use the same decode tests to check whether they preserve node order, the radix boundary, and zero blocks.

## Quantum directions

- **Parity.** The classical code over residues modulo ten imposes `q₁ + q₂ + q₃ + q₄ ≡ 0 (mod 10)`. Its 1,000 codewords have minimum Hamming distance two. Every single-symbol substitution changes the checksum. Paired opposite shifts and digit swaps can preserve it. A uniformly sampled target state fails the check in 9,000 of 10,000 cases, or 9,000 of 9,999 when conditioned on a change from a valid word. This result describes a classical error model. A quantum claim would require a code subspace, an explicit noise model, and a syndrome measurement. For example, a diagonal phase error can preserve every computational-basis parity outcome.
- **Phase.** The map `d ↦ exp(2πid/10)` preserves addition of residues. Union of visible strokes is idempotent, so a homomorphism from that operation to a group must send each stroke set to the identity. The examples for 5, 7, 8, and 9 remain compatible with modular addition when composing the stated distinct primitives. A phase-gate interpretation needs an explicitly defined gate family and composition rule.
- **Register capacity and circuits.** Four ten-level sites provide 10,000 computational-basis labels. The factor `log₂(10)` describes capacity per site. Any circuit-depth claim needs matched implementations of an arithmetic operation under a specified gate set, connectivity, and cost model. A small addition benchmark can report gate counts and depth separately.
- **Matrix product states.** A fixed digit string represented as a product of basis states has an MPS description with bond dimension one. A model of correlated digits or time evolution needs defined tensors, bonds, and dynamics. A first test would compare an explicit tensor construction with a direct simulation on a small fixed register.
