"""Reference SVG renderer for the Iteris Core geometry."""

import argparse
from xml.sax.saxutils import escape

from .core import IterisNode, IterisNumber, decode_iteris, encode_iteris


NODE_HEIGHT = 100
QUADRANT_WIDTH = 20
_CHAIN_GAP = 4 * QUADRANT_WIDTH
_NODE_SLOT = 3 * QUADRANT_WIDTH
_TOKEN_SLOT = QUADRANT_WIDTH
_MIDPOINT = NODE_HEIGHT // 2
_OUTER = NODE_HEIGHT // 10
_INNER = 3 * _OUTER
_MINUS_HALF = 3 * NODE_HEIGHT // 50
_DOT_RADIUS = NODE_HEIGHT / 40
_PERIOD_Y = -_OUTER
_PADDING = 8
_PRIMITIVES = {
    "p1": (0, _OUTER, QUADRANT_WIDTH, _OUTER),
    "p2": (0, _INNER, QUADRANT_WIDTH, _INNER),
    "p3": (0, _OUTER, QUADRANT_WIDTH, _INNER),
    "p4": (QUADRANT_WIDTH, _OUTER, 0, _INNER),
    "p6": (QUADRANT_WIDTH, _OUTER, QUADRANT_WIDTH, _INNER),
}
_REFLECTIONS = {
    "D1": (1, 1, 0),
    "D2": (-1, 1, 0),
    "D3": (1, -1, NODE_HEIGHT),
    "D4": (-1, -1, NODE_HEIGHT),
}
_Segment = tuple[int, int, int, int]


def _chain_segments(nodes: tuple[IterisNode, ...], axis: int = 0) -> list[_Segment]:
    segments = [(axis, 0, axis, len(nodes) * NODE_HEIGHT)]
    for index, node in enumerate(nodes):
        for quadrant, strokes in node.strokes.items():
            x_sign, y_sign, y_offset = _REFLECTIONS[quadrant]
            offset = index * NODE_HEIGHT + y_offset
            for stroke in strokes:
                x1, y1, x2, y2 = _PRIMITIVES[stroke]
                segments.append((
                    axis + x_sign * x1, offset + y_sign * y1,
                    axis + x_sign * x2, offset + y_sign * y2,
                ))
    return segments


def _path(segments: list[_Segment]) -> str:
    data = " ".join(f"M{x1} {y1}L{x2} {y2}" for x1, y1, x2, y2 in segments)
    return f'<path d="{data}" fill="none" stroke="currentColor" stroke-width="2"/>'


def _vertical_numeral(number: IterisNumber) -> str:
    segments = _chain_segments(number.int_nodes)
    if number.sign == -1:
        center = -2 * QUADRANT_WIDTH
        segments.append((center - _MINUS_HALF, _MIDPOINT, center + _MINUS_HALF, _MIDPOINT))
    if number.frac_nodes:
        segments.extend(_chain_segments(number.frac_nodes, _CHAIN_GAP))
    markup = _path(segments)
    if number.frac_nodes:
        markup += _radix_dot(_CHAIN_GAP // 2)
    return markup


def _radix_dot(center: int) -> str:
    return f'<circle cx="{center}" cy="{_MIDPOINT}" r="{_DOT_RADIUS:g}" fill="currentColor"/>'


def _row_segments(nodes: tuple[IterisNode, ...], start: int) -> list[_Segment]:
    return [
        segment
        for index, node in enumerate(nodes)
        for segment in _chain_segments((node,), start + index * _NODE_SLOT + _NODE_SLOT // 2)
    ]


def _horizontal_numeral(
    integer: tuple[IterisNode, ...],
    fractional: tuple[IterisNode, ...] = (),
    period: tuple[IterisNode, ...] = (),
    *,
    negative: bool = False,
) -> tuple[int, str]:
    segments = []
    cursor = 0
    if negative:
        center = _TOKEN_SLOT // 2
        segments.append((center - _MINUS_HALF, _MIDPOINT, center + _MINUS_HALF, _MIDPOINT))
        cursor += _TOKEN_SLOT
    segments.extend(_row_segments(integer, cursor))
    cursor += len(integer) * _NODE_SLOT

    radix = ""
    if fractional or period:
        radix = _radix_dot(cursor + _TOKEN_SLOT // 2)
        cursor += _TOKEN_SLOT
    segments.extend(_row_segments(fractional + period, cursor))
    end = cursor + (len(fractional) + len(period)) * _NODE_SLOT
    if period:
        inset = _NODE_SLOT // 2 - QUADRANT_WIDTH
        start = cursor + len(fractional) * _NODE_SLOT + inset
        segments.append((start, _PERIOD_Y, end - inset, _PERIOD_Y))
    return end, _path(segments) + radix


def render_svg(number: IterisNumber, *, horizontal: bool = False) -> str:
    """Return a standalone SVG in the selected layout."""
    if horizontal:
        row_width, markup = _horizontal_numeral(number.int_nodes, number.frac_nodes, negative=number.sign == -1)
        left = -_PADDING
        width = row_width + 2 * _PADDING
        height = NODE_HEIGHT + 2 * _PADDING
    else:
        left = (-2 * QUADRANT_WIDTH - _MINUS_HALF if number.sign == -1 else -QUADRANT_WIDTH) - _PADDING
        right = (_CHAIN_GAP if number.frac_nodes else 0) + QUADRANT_WIDTH + _PADDING
        width = right - left
        height = max(len(number.int_nodes), len(number.frac_nodes)) * NODE_HEIGHT + 2 * _PADDING
        markup = _vertical_numeral(number)

    viewbox = f"{left} {-_PADDING} {width} {height}"
    title = escape(decode_iteris(number))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" '
        f'width="{width}" height="{height}" role="img">\n'
        f'<title>Iteris numeral {title}</title>\n{markup}\n</svg>\n'
    )


def _chart_sample(center: int, label_y: int, drawing_y: int, label: str, width: int, markup: str) -> tuple[str, str]:
    scale = .52
    left = center - scale * width / 2
    return (
        f'<text x="{center}" y="{label_y}" text-anchor="middle" font-size="13">{escape(label)}</text>',
        f'<g aria-label="{escape(label)}" transform="translate({left:g} {drawing_y}) scale({scale})">{markup}</g>',
    )


def render_reference_svg() -> str:
    """Render the digit placements, horizontal numerals, and formula examples."""
    width, height = 730, 1010
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img">',
        '<title>Iteris Core digit reference, horizontal numerals, and formulas</title>',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        '<g color="#172c43" fill="currentColor" font-family="system-ui, sans-serif">',
        '<text x="28" y="36" font-size="22" font-weight="700">Iteris digit reference</text>',
        '<path d="M28 69H702 M28 554H702 M28 824H702" fill="none" stroke="#b9c9d8"/>',
    ]
    for digit in range(1, 10):
        elements.append(f'<text x="{124 + (digit - 1) * 68}" y="61" text-anchor="middle">{digit}</text>')

    for index, label in enumerate(("Units", "Tens", "Hundreds", "Thousands")):
        y = 82 + index * 114
        elements.append(f'<text x="28" y="{y + _MIDPOINT + 5}" font-size="13">{label}</text>')
        for digit in range(1, 10):
            x = 124 + (digit - 1) * 68
            nodes = (IterisNode(digit * 10**index),)
            elements.append(f'<g class="digit-placement" transform="translate({x} {y})">{_path(_chain_segments(nodes))}</g>')

    elements.append('<text x="28" y="586" font-size="19" font-weight="700">Horizontal numerals</text>')
    for index, (raw, label) in enumerate((
        ("9999", "9999"), ("10000", "1 0000"), ("100000000", "1 0000 0000"),
        ("100000005", "1 0000 0005"), ("0.00000001", "0.0000 0001"),
    )):
        number = encode_iteris(raw)
        row = _horizontal_numeral(number.int_nodes, number.frac_nodes)
        elements.extend(_chart_sample(91 + index * 137, 619, 638, label, *row))

    zero = (IterisNode(0),)
    for center, label, prefix, repeating in (
        (200, "0.0000(3)", zero, (IterisNode(3333),)),
        (530, "0.(142857)", (), tuple(IterisNode(value) for value in (1428, 5714, 2857))),
    ):
        row = _horizontal_numeral(zero, prefix, repeating)
        elements.extend(_chart_sample(center, 727, 746, label, *row))

    elements.append('<text x="28" y="858" font-size="19" font-weight="700">Numerals in formulas</text>')
    base_width, base = _horizontal_numeral((IterisNode(2),))
    exponent_width, exponent = _horizontal_numeral(encode_iteris("10000").int_nodes)
    scaling = .6
    power = base + f'<g transform="translate({base_width} -34) scale({scaling})">{exponent}</g>'
    elements.extend(_chart_sample(200, 891, 931, "2^(10 000)", base_width + int(exponent_width * scaling), power))
    zero_width, stem = _horizontal_numeral(zero)
    absolute_width = zero_width + _TOKEN_SLOT
    bars = _path([(0, -10, 0, 110), (absolute_width, -10, absolute_width, 110)])
    absolute = bars + f'<g transform="translate({_TOKEN_SLOT // 2} 0)">{stem}</g>'
    elements.extend(_chart_sample(530, 891, 931, "|0|", absolute_width, absolute))
    elements.extend(("</g>", "</svg>"))
    return "\n".join(elements) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("decimal", nargs="?", help="finite decimal to render")
    source.add_argument("--reference", action="store_true", help="render the digit reference chart")
    parser.add_argument("--horizontal", action="store_true", help="render a decimal in the horizontal reference layout")
    args = parser.parse_args()
    try:
        svg = render_reference_svg() if args.reference else render_svg(encode_iteris(args.decimal), horizontal=args.horizontal)
    except ValueError as error:
        parser.error(str(error))
    print(svg, end="")


if __name__ == "__main__":
    main()
