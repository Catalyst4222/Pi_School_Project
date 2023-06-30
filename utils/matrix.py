import asyncio
import threading
from pathlib import Path
from typing import Optional, Union

from PIL import Image

from .constants import DEFAULT_OPTIONS
from .holders import FrameHolder, GifHolder, ImageHolder

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions


class FormattedMatrix(RGBMatrix):  # todo add helper methods

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
        if isinstance(image, str):
            image = GifHolder(image) if image.endswith(".gif") else ImageHolder(image)
        elif isinstance(image, Path):
            if image.is_dir():
                image = FrameHolder(image)
            elif image.suffix == ".gif":
                image = GifHolder(image)
            else:
                image = ImageHolder(image)
        elif isinstance(image, Image.Image):
            if getattr(image, "n_frames", 0) > 1:
                image = GifHolder(image)
            else:
                image = ImageHolder(image)
        elif not isinstance(image, ImageHolder):
            raise ValueError(
                f"image was not a valid type (got {image.__class__.__name__}"
            )

        image.display(self)
