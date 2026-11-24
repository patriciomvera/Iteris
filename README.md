## Iteris

Iteris is a spatial numeral notation inspired by Cistercian numerals. It writes signed finite decimals in base 10,000, with four decimal positions in each node and a continuous stem for each chain.

**Status** · Private work in progress  
**Author** · Patricio M. Vera, simbionte.org

- [Core v1.0 draft](ITERIS_CORE_v1.0.md) defines canonical decimal conversion and the reference geometry.
- [Review of Gemini's proposals](ITERIS_REVIEW.md) records what the core adopts and the open questions for Extended and Quantum.
- [Notation v0.2](ITERIS_NOTATION_02.md) and [exploratory v0.5](ITERIS_SPEC_v05.md) record the earlier design.

The Python reference uses the standard library and runs on Python 3.9 or later.

```sh
python -m unittest discover -v
python iteris_svg.py 100000005 > numeral.svg
python iteris_svg.py --reference > iteris_reference.svg
```

```python
from iteris_core import decode_iteris, encode_iteris

number = encode_iteris("0.00000001")
assert [node.value for node in number.frac_nodes] == [0, 1]
assert decode_iteris(number) == "0.00000001"
```

![Iteris digit reference and comparison of five numbers with grouped decimal notation](iteris_reference.svg)
