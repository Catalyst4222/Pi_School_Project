"""
various functions to manipulate colors and images
for simplicity, all colors are assumed rgb unless stated otherwise
"""
from math import sqrt
from typing import TypeVar

from utils.classes import Color

_T = TypeVar("_T")
_Color = TypeVar(
    "_Color", Color, tuple[int, int, int], int
)  # Class, components, and hex, respectively


def hex_to_tuple(hex_: int) -> tuple[int, int, int]:
    return hex_ >> 16 & 255, hex_ >> 8 & 255, hex_ & 255


def tuple_to_hex(values: tuple[int, int, int]) -> int:
    return (values[0] << 16) + (values[1] << 8) + values[2]


def average_colors(col1: _Color, col2: _Color) -> tuple[int, int, int]:
    if isinstance(col1, int):
        col1 = hex_to_tuple(col1)

    if isinstance(col2, int):
        col2 = hex_to_tuple(col2)

    # read that it was better to pythagoras it
    # noinspection PyTypeChecker
    return tuple(
        int(sqrt(col1[component] ** 2 + col2[component] ** 2)) // 2
        for component in range(3)
    )
