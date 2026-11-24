"""Conformance tests for the positional Iteris Core codec."""

from fractions import Fraction
from random import Random
import unittest

from iteris_core import IterisNode, IterisNumber, decode_iteris, encode_iteris


class IterisCodecTests(unittest.TestCase):
    def test_canonical_examples(self):
        examples = (
            ("0", 1, (0,), (), "0"),
            ("-0.00", 1, (0,), (), "0"),
            (" \t+00042.000\r\n", 1, (42,), (), "42"),
            ("9999", 1, (9999,), (), "9999"),
            ("10000", 1, (1, 0), (), "10000"),
            ("100000000", 1, (1, 0, 0), (), "100000000"),
            ("100000005", 1, (1, 0, 5), (), "100000005"),
            ("0.0700", 1, (0,), (700,), "0.07"),
            ("0.00000001", 1, (0,), (0, 1), "0.00000001"),
            ("0.000100000001", 1, (0,), (1, 0, 1), "0.000100000001"),
            ("-3.14159", -1, (3,), (1415, 9000), "-3.14159"),
        )
        for raw, sign, integers, fractions, canonical in examples:
            with self.subTest(raw=raw):
                number = encode_iteris(raw)
                self.assertEqual(number.sign, sign)
                self.assertEqual(tuple(node.value for node in number.int_nodes), integers)
                self.assertEqual(tuple(node.value for node in number.frac_nodes), fractions)
                self.assertEqual(decode_iteris(number), canonical)
                self.assertEqual(encode_iteris(canonical), number)

    def test_exact_value_and_canonical_roundtrip(self):
        rng = Random(20261124)
        base = 10_000
        for _ in range(10_000):
            sign = rng.choice(("", "+", "-"))
            alphabet = "000000123456789"
            integer = "".join(rng.choices(alphabet, k=rng.randint(1, 48)))
            fraction = "".join(rng.choices(alphabet, k=rng.randint(0, 48)))
            raw = sign + integer + ("." + fraction if fraction else "")
            number = encode_iteris(raw)
            integer_value = 0
            for node in number.int_nodes:
                integer_value = integer_value * base + node.value
            fractional_value = sum(
                Fraction(node.value, base ** position)
                for position, node in enumerate(number.frac_nodes, start=1)
            )
            actual = number.sign * (integer_value + fractional_value)
            canonical = decode_iteris(number)
            self.assertEqual(actual, Fraction(raw), raw)
            self.assertEqual(Fraction(canonical), actual, raw)
            self.assertEqual(encode_iteris(canonical), number, raw)

    def test_long_decimal_is_processed_by_block(self):
        canonical = "1" + "0" * 4500 + ".000" + "1234" * 1100
        number = encode_iteris(canonical + "00")
        self.assertEqual(len(number.int_nodes), 1126)
        self.assertEqual(len(number.frac_nodes), 1101)
        self.assertEqual(decode_iteris(number), canonical)

    def test_malformed_decimal_is_rejected(self):
        for raw in (
            "", " ", ".", ".5", "1.", "-", "++1", "--1", "1 2", "1,25",
            "1_000", "1e3", "1\n2", "-\u0660", "0.\u0660", "\uff11\uff12", "\u22121",
        ):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                encode_iteris(raw)

    def test_every_node_has_a_distinct_quadrant_pattern(self):
        patterns = set()
        for value in range(10_000):
            node = IterisNode(value)
            quadrants = node.quadrants
            self.assertEqual(sum(digit * 10 ** index for index, digit in enumerate(quadrants)), value)
            strokes = node.strokes
            patterns.add(tuple(tuple(strokes[f"D{index}"]) for index in range(1, 5)))
        self.assertEqual(len(patterns), 10_000)
        self.assertEqual(
            IterisNode(9876).strokes,
            {"D1": ("p6",), "D2": ("p1", "p6"), "D3": ("p2", "p6"), "D4": ("p1", "p2", "p6")},
        )
        self.assertEqual(IterisNode(5432).strokes["D4"], ("p1", "p4"))

    def test_invalid_node_values_are_rejected(self):
        for value in (-1, 10_000, True, 3.5, "4"):
            with self.subTest(value=value), self.assertRaises((TypeError, ValueError)):
                IterisNode(value)

    def test_noncanonical_number_objects_are_rejected(self):
        zero, one = IterisNode(0), IterisNode(1)
        invalid = (
            (0, (one,), ()),
            (True, (one,), ()),
            (-1, (zero,), ()),
            (1, (), ()),
            (1, (zero, one), ()),
            (1, (one,), (one, zero)),
            (1, (one,), (zero,)),
            (1, [one], ()),
            (1, (one,), [one]),
            (1, (1,), ()),
            (1, (one,), (one, 2)),
        )
        for arguments in invalid:
            with self.subTest(arguments=arguments), self.assertRaises((TypeError, ValueError)):
                IterisNumber(*arguments)


if __name__ == "__main__":
    unittest.main()
