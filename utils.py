from collections.abc import Iterable
from typing import Optional

try:
    from rgbmatrix import RGBMatrix
except ImportError:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions


# Hardcoded, fight me
M_WIDTH = 64
M_HEIGHT = 32

DEFAULT_OPTIONS = RGBMatrixOptions()
DEFAULT_OPTIONS.cols = M_WIDTH
DEFAULT_OPTIONS.rows = M_HEIGHT
DEFAULT_OPTIONS.chain_length = 1
DEFAULT_OPTIONS.parallel = 1
DEFAULT_OPTIONS.hardware_mapping = "adafruit-hat"


class Color(Iterable):
    def __init__(self, r: int, g: int, b: int):
        _locals = locals()
        _locals.pop("self")

        for color in _locals.values():
            if not 0 < color < 255:
                raise ValueError("Color values must be between 0 and 255 inclusive!")

        self.r: int = r
        self.g: int = g
        self.b: int = b

    def __iter__(self):
        return (self.r, self.g, self.b).__iter__()


class Pixel:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y

    def copy(self):
        return self.__class__(self.x, self.y)

    def __repr__(self):
        return f"<Pixel(x={self.x}, y={self.y})>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError  # Should make good error message sometime
        return self.x == other.x and self.y == other.y


class FormattedMatrix(RGBMatrix):
    def __init__(self, options: Optional[RGBMatrixOptions] = None):
        super().__init__(
            options=DEFAULT_OPTIONS if options is None else options,
        )
