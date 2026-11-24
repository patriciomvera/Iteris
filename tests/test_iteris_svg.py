import re
import unittest
from pathlib import Path
from xml.etree import ElementTree

from iteris import encode_iteris
from iteris.svg import render_reference_svg, render_svg


_SVG = "{http://www.w3.org/2000/svg}"
_COORD = r"(-?[0-9]+)"
_SEGMENT = re.compile(rf"M{_COORD} {_COORD}(?:L{_COORD} {_COORD}|H{_COORD}|V{_COORD})")


def _segments(svg):
    root = ElementTree.fromstring(svg) if isinstance(svg, str) else svg
    for path in root.iter(f"{_SVG}path"):
        for x, y, x_line, y_line, horizontal, vertical in _SEGMENT.findall(path.attrib["d"]):
            start = (int(x), int(y))
            end = (int(x_line or horizontal or x), int(y_line or vertical or y))
            yield tuple(sorted((start, end)))
    for line in root.iter(f"{_SVG}line"):
        x1, y1, x2, y2 = (int(line.attrib[axis]) for axis in ("x1", "y1", "x2", "y2"))
        yield tuple(sorted(((x1, y1), (x2, y2))))


class IterisSvgTests(unittest.TestCase):
    def test_all_nodes_have_distinct_segment_sets(self):
        drawings = {
            frozenset(_segments(render_svg(encode_iteris(str(node)))))
            for node in range(10000)
        }
        self.assertEqual(len(drawings), 10000)

    def test_integer_zero_blocks_preserve_stem_length(self):
        for decimal, height, tail in (
            ("10000", 200, []),
            ("100000000", 300, []),
            ("100000005", 300, [((0, 210), (20, 210)), ((0, 230), (20, 210))]),
        ):
            with self.subTest(decimal=decimal):
                svg = render_svg(encode_iteris(decimal))
                expected = {((0, 0), (0, height)), ((0, 10), (20, 10)), *tail}
                self.assertEqual(set(_segments(svg)), expected)

    def test_fractional_zero_block_and_radix_survive_rendering(self):
        svg = render_svg(encode_iteris("-0.00000001"))
        self.assertEqual(set(_segments(svg)), {
            ((0, 0), (0, 100)), ((80, 0), (80, 200)),
            ((80, 110), (100, 110)), ((-46, 50), (-34, 50)),
        })
        root = ElementTree.fromstring(svg)
        dot = root.find(f"{_SVG}circle")
        self.assertEqual((dot.attrib["cx"], dot.attrib["cy"]), ("40", "50"))

    def test_horizontal_rollover_preserves_zero_slot(self):
        svg = render_svg(encode_iteris("10000"), horizontal=True)
        self.assertEqual(set(_segments(svg)), {
            ((30, 0), (30, 100)), ((90, 0), (90, 100)), ((30, 10), (50, 10)),
        })

    def test_horizontal_sign_radix_and_fractional_slots_align(self):
        svg = render_svg(encode_iteris("-0.00000001"), horizontal=True)
        self.assertEqual(set(_segments(svg)), {
            ((50, 0), (50, 100)), ((130, 0), (130, 100)), ((190, 0), (190, 100)),
            ((190, 10), (210, 10)), ((4, 50), (16, 50)),
        })
        root = ElementTree.fromstring(svg)
        dot = root.find(f".//{_SVG}circle")
        self.assertEqual((dot.attrib["cx"], dot.attrib["cy"], dot.attrib["r"]), ("90", "50", "2.5"))

    def test_checked_in_reference_matches_renderer(self):
        reference = Path(__file__).resolve().parents[1] / "docs" / "assets" / "iteris_reference.svg"
        chart = reference.read_text(encoding="utf-8")
        self.assertEqual(chart, render_reference_svg())
        root = ElementTree.fromstring(chart)
        placements = [
            group for group in root.iter(f"{_SVG}g")
            if "digit-placement" in group.attrib.get("class", "").split()
        ]
        self.assertEqual(len(placements), 36)

    def test_reference_overbar_excludes_the_finite_prefix(self):
        root = ElementTree.fromstring(render_reference_svg())
        example = root.find(f".//{_SVG}g[@aria-label='0.0000(3)']")
        segments = set(_segments(example))
        self.assertTrue({
            ((30, 0), (30, 100)), ((110, 0), (110, 100)), ((170, 0), (170, 100)),
        }.issubset(segments))
        self.assertEqual(
            {segment for segment in segments if segment[0][1] == segment[1][1] == -10},
            {((150, -10), (190, -10))},
        )

    def test_reference_overbar_covers_a_whole_multinode_period(self):
        root = ElementTree.fromstring(render_reference_svg())
        example = root.find(f".//{_SVG}g[@aria-label='0.(142857)']")
        segments = set(_segments(example))
        self.assertTrue({
            ((110, 0), (110, 100)), ((170, 0), (170, 100)), ((230, 0), (230, 100)),
        }.issubset(segments))
        self.assertEqual(
            {segment for segment in segments if segment[0][1] == segment[1][1] == -10},
            {((90, -10), (250, -10))},
        )

    def test_reference_shows_numerals_inside_ordinary_formulas(self):
        root = ElementTree.fromstring(render_reference_svg())
        for label in ("2^(10 000)", "|0|"):
            with self.subTest(label=label):
                example = root.find(f".//{_SVG}g[@aria-label='{label}']")
                self.assertIsNotNone(example)
                self.assertTrue(set(_segments(example)))


if __name__ == "__main__":
    unittest.main()
