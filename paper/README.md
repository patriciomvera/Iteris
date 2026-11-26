# Iteris manuscript companion

This directory accompanies *Rational Numerals and Carry Geometry in Iteris*.
Run the numerical checks from the repository root with Python 3:

```sh
python paper/check_iteris_paper.py
```

The script uses only the standard library. It checks the digit graph,
carry statistics and traversal costs for widths one through four, and
all 362,880 digit assignments with zero fixed. The four-position totals
are 19,986 edits for numerical order, 10,014 for the optimal open order,
and 10,016 for the optimal cyclic order.

The manuscript source uses `iteris.sty` to render its examples.
Keep the style file next to `main.tex` when compiling the manuscript.

## Lean 4 checks

The two standalone files were checked with Lean 4.36.0.
They require no Mathlib.

- [IterisChecksV02.lean](IterisChecksV02.lean) covers the digit graph,
  carry costs, example rational expansions, and a traversal of all
  10,000 nodes.
- [IterisChecksExtra.lean](IterisChecksExtra.lean) adds parity counts,
  total counting cost, and period-length checks over finite ranges.

From the repository root, run both files with an available Lean 4
toolchain.

```sh
lean paper/IterisChecksV02.lean
lean paper/IterisChecksExtra.lean
```

These files specify finite checks. The manuscript supplies the general
proofs. The numerical results were also checked independently.
