from collections.abc import Iterable
from typing import TypedDict


class FrameData(TypedDict):
    name: str
    delay: float
    order: int


class DataDict(TypedDict):
    frames: list[FrameData]
    resolved: bool
    export_to: str
    import_from: str


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
