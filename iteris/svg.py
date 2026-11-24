"""Reference SVG renderer for the Iteris Core geometry."""

import argparse
from xml.sax.saxutils import escape

from .core import IterisNode, IterisNumber, decode_iteris, encode_iteris


NODE_HEIGHT = 100
QUADRANT_WIDTH = 20
_CHAIN_GAP = 4 * QUADRANT_WIDTH
_MIDPOINT = NODE_HEIGHT // 2
_OUTER = NODE_HEIGHT // 10
_INNER = 3 * _OUTER
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


def _numeral(number: IterisNumber) -> str:
    segments = _chain_segments(number.int_nodes)
    if number.sign == -1:
        segments.append((-46, _MIDPOINT, -34, _MIDPOINT))
    if number.frac_nodes:
        segments.extend(_chain_segments(number.frac_nodes, _CHAIN_GAP))
    markup = _path(segments)
    if number.frac_nodes:
        markup += f'<circle cx="{_CHAIN_GAP // 2}" cy="{_MIDPOINT}" r="2.5" fill="currentColor"/>'
    return markup


def render_svg(number: IterisNumber) -> str:
    """Return a standalone, top-aligned SVG of a canonical Iteris number."""
    left = (-46 if number.sign == -1 else -QUADRANT_WIDTH) - _PADDING
    right = (_CHAIN_GAP if number.frac_nodes else 0) + QUADRANT_WIDTH + _PADDING
    height = max(len(number.int_nodes), len(number.frac_nodes)) * NODE_HEIGHT
    viewbox = f"{left} {-_PADDING} {right - left} {height + 2 * _PADDING}"
    title = escape(decode_iteris(number))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" '
        f'width="{right - left}" height="{height + 2 * _PADDING}" role="img">\n'
        f'<title>Iteris numeral {title}</title>\n{_numeral(number)}\n</svg>\n'
    )


def render_reference_svg() -> str:
    """Render all 36 nonzero digit placements and the first reading examples."""
    width, height = 730, 835
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img">',
        '<title>Iteris Core digit reference and reading examples</title>',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        '<g color="#172c43" fill="currentColor" font-family="system-ui, sans-serif">',
        '<text x="28" y="36" font-size="22" font-weight="700">Iteris digit reference</text>',
        '<path d="M28 69H702 M28 554H702" fill="none" stroke="#b9c9d8"/>',
    ]
    for digit in range(1, 10):
        elements.append(f'<text x="{124 + (digit - 1) * 68}" y="61" text-anchor="middle">{digit}</text>')

    for index, label in enumerate(("Units", "Tens", "Hundreds", "Thousands")):
        y = 82 + index * 114
        elements.append(f'<text x="28" y="{y + _MIDPOINT + 5}" font-size="13">{label}</text>')
        for digit in range(1, 10):
            x = 124 + (digit - 1) * 68
            nodes = (IterisNode(digit * 10**index),)
            elements.append(f'<g transform="translate({x} {y})">{_path(_chain_segments(nodes))}</g>')

    elements.append('<text x="28" y="586" font-size="19" font-weight="700">Reading zero blocks</text>')
    for index, (raw, label) in enumerate((
        ("9999", "9999"), ("10000", "1 0000"), ("100000000", "1 0000 0000"),
        ("100000005", "1 0000 0005"), ("0.00000001", "0.0000 0001"),
    )):
        x = 84 + index * 134
        elements.append(f'<text x="{x}" y="617" text-anchor="middle" font-size="13">{label}</text>')
        elements.append(f'<g transform="translate({x} 630) scale(.6)">{_numeral(encode_iteris(raw))}</g>')
    elements.extend(("</g>", "</svg>"))
    return "\n".join(elements) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("decimal", nargs="?", help="finite decimal to render")
    source.add_argument("--reference", action="store_true", help="render the digit reference chart")
    args = parser.parse_args()
    try:
        svg = render_reference_svg() if args.reference else render_svg(encode_iteris(args.decimal))
    except ValueError as error:
        parser.error(str(error))
    print(svg, end="")


if __name__ == "__main__":
    main()
