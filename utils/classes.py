from collections import Sequence
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


# Do not trust
class Color(Sequence):
    def __init__(self, r: int, g: int, b: int):
        _locals = locals()
        _locals.pop("self")

        for color in _locals.values():
            if not 0 < color < 255:
                raise ValueError("Color values must be between 0 and 255 inclusive!")

        self.r: int = r
        self.g: int = g
        self.b: int = b
        self.tuple: tuple[int, int, int] = (r, g, b)

    # We're a tuple :wink:
    def __getattribute__(self, name):
        if name == "tuple":
            return super().__getattribute__(name)

        try:
            return self.tuple.__getattribute__(name)
        except AttributeError:
            return super().__getattribute__(name)

    def __len__(self):
        return 3

    def __getitem__(self, item):
        if not isinstance(item, (int, slice)):
            raise TypeError(
                f"{self.__class__.__name__} indices must be integers or slices, not str"
            )

        return self.tuple[item]


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
