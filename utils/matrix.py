import asyncio
import threading
from pathlib import Path
from typing import Optional, Union

from PIL import Image

from .constants import DEFAULT_OPTIONS
from .holders import ImageHolder, get_holder

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions


class FormattedMatrix(
    RGBMatrix
):  # todo add helper methods, clean up the emulation disparity

    # There's a discrepancy between the emulator and the matrix, so very bad code is needed
    def __new__(cls, *args, options: Optional[RGBMatrixOptions] = None, **kwargs):
        if RGBMatrix.__module__.startswith("RGBMatrixEmulator"):
            return super().__new__(
                cls,
            )
        return super().__new__(
            cls,
            *args,
            options=DEFAULT_OPTIONS if options is None else options,
            **kwargs,
        )

    def __init__(self, *args, options: Optional[RGBMatrixOptions] = None, **kwargs):
        if RGBMatrix.__module__.startswith("RGBMatrixEmulator"):
            # noinspection PyArgumentList
            super().__init__(
                *args, options=DEFAULT_OPTIONS if options is None else options, **kwargs
            )

    def display(self, image: Union[Image.Image, ImageHolder, Path, str]):
        holder = get_holder(image)

        holder.display(self)
