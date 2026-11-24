import re
import unittest
from pathlib import Path
from xml.etree import ElementTree

from iteris_core import encode_iteris
from iteris_svg import render_reference_svg, render_svg


_SVG = "{http://www.w3.org/2000/svg}"
_SEGMENT = re.compile(r"M(-?[0-9]+) (-?[0-9]+)L(-?[0-9]+) (-?[0-9]+)")


def _segments(svg):
    root = ElementTree.fromstring(svg)
    path = root.find(f"{_SVG}path")
    for coordinates in _SEGMENT.findall(path.attrib["d"]):
        x1, y1, x2, y2 = map(int, coordinates)
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

    def test_checked_in_reference_matches_renderer(self):
        chart = Path(__file__).with_name("iteris_reference.svg").read_text(encoding="utf-8")
        self.assertEqual(chart, render_reference_svg())
        root = ElementTree.fromstring(chart)
        placements = [
            group for group in root.iter(f"{_SVG}g")
            if group.attrib.get("transform", "").startswith("translate(")
            and "scale" not in group.attrib["transform"]
        ]
        self.assertEqual(len(placements), 36)


if __name__ == "__main__":
    unittest.main()
