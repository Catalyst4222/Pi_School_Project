"""
various functions to manipulate colors and images
for simplicity, all colors are assumed rgb unless stated otherwise
"""
from math import sqrt
from typing import TypeVar, Union

from PIL.Image import Image

from .classes import Color
from .constants import M_HEIGHT, M_WIDTH
from .holders import ImageHolder

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


def resize(
    image: Union[Image, ImageHolder], size: tuple[int, int] = (M_WIDTH, M_HEIGHT)
):
    """Resized the image in-place to fit in the given size. Defaults to the matrix size"""
    if isinstance(image, Image):
        image.thumbnail(size)
    elif isinstance(image, ImageHolder):
        image.image.thumbnail(size)
    else:
        raise TypeError(
            f"Expected Image or ImageHolder, got {image.__class__.__name__}"
        )
