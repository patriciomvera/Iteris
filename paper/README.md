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
