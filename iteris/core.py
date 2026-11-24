"""Exact conversion between finite decimal strings and canonical Iteris nodes."""

import re
from dataclasses import dataclass


_BLOCK_DIGITS = 4
_BASE = 10**_BLOCK_DIGITS
_DECIMAL = re.compile(r"([+-]?)([0-9]+)(?:\.([0-9]+))?")
_QUADRANTS = ("D1", "D2", "D3", "D4")
_DIGIT_STROKES = (
    (),
    ("p1",),
    ("p2",),
    ("p3",),
    ("p4",),
    ("p1", "p4"),
    ("p6",),
    ("p1", "p6"),
    ("p2", "p6"),
    ("p1", "p2", "p6"),
)


@dataclass(frozen=True)
class IterisNode:
    """A single base-10,000 digit."""

    value: int

    def __post_init__(self) -> None:
        if type(self.value) is not int:
            raise TypeError("A node value must be an integer.")
        if not 0 <= self.value < _BASE:
            raise ValueError("A node value must be in 0..9999.")

    @property
    def quadrants(self) -> tuple[int, int, int, int]:
        """Digits in D1 through D4 order, from units to thousands."""
        value = self.value
        return (value % 10, value // 10 % 10, value // 100 % 10, value // 1000)

    @property
    def strokes(self) -> dict[str, tuple[str, ...]]:
        """The primitives present in each quadrant, before reflection."""
        return dict(zip(_QUADRANTS, (_DIGIT_STROKES[digit] for digit in self.quadrants)))


@dataclass(frozen=True)
class IterisNumber:
    """Canonical sign and chains, with the most significant nodes first."""

    sign: int
    int_nodes: tuple[IterisNode, ...]
    frac_nodes: tuple[IterisNode, ...] = ()

    def __post_init__(self) -> None:
        if type(self.sign) is not int:
            raise TypeError("The sign must be an integer.")
        if self.sign not in (-1, 1):
            raise ValueError("The sign must be +1 or -1.")
        for chain in (self.int_nodes, self.frac_nodes):
            if not isinstance(chain, tuple) or any(not isinstance(node, IterisNode) for node in chain):
                raise TypeError("Chains must be tuples of IterisNode objects.")
        if not self.int_nodes:
            raise ValueError("The integer chain must contain at least one node.")
        if len(self.int_nodes) > 1 and self.int_nodes[0].value == 0:
            raise ValueError("The integer chain cannot start with an extra zero node.")
        if self.frac_nodes and self.frac_nodes[-1].value == 0:
            raise ValueError("The fractional chain cannot end with a zero node.")
        if self.sign == -1 and self.int_nodes[0].value == 0 and not self.frac_nodes:
            raise ValueError("Zero must have sign +1.")


def _read_nodes(digits: str) -> tuple[IterisNode, ...]:
    return tuple(
        IterisNode(int(digits[start : start + _BLOCK_DIGITS]))
        for start in range(0, len(digits), _BLOCK_DIGITS)
    )


def encode_iteris(raw: str) -> IterisNumber:
    """Parse a signed finite decimal string and normalize its value exactly."""
    if not isinstance(raw, str):
        raise TypeError("The decimal input must be a string.")
    match = _DECIMAL.fullmatch(raw.strip())
    if match is None:
        raise ValueError("Expected ASCII decimal digits with an optional sign and point.")

    sign_char, integer, fraction = match.groups()
    integer = integer.lstrip("0") or "0"
    fraction = (fraction or "").rstrip("0")
    sign = -1 if sign_char == "-" and (integer != "0" or fraction) else 1

    integer = integer.zfill(len(integer) + (-len(integer) % _BLOCK_DIGITS))
    fraction = fraction.ljust(len(fraction) + (-len(fraction) % _BLOCK_DIGITS), "0")
    return IterisNumber(sign, _read_nodes(integer), _read_nodes(fraction))


def decode_iteris(number: IterisNumber) -> str:
    """Return the canonical ASCII decimal spelling of an Iteris number."""
    if not isinstance(number, IterisNumber):
        raise TypeError("Expected an IterisNumber.")
    leading, *rest = number.int_nodes
    integer = str(leading.value) + "".join(f"{node.value:04d}" for node in rest)
    fraction = "".join(f"{node.value:04d}" for node in number.frac_nodes).rstrip("0")
    sign = "-" if number.sign == -1 else ""
    return f"{sign}{integer}.{fraction}" if fraction else f"{sign}{integer}"
