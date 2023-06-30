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
    def __init__(self, options: Optional[RGBMatrixOptions] = None):
        super().__init__(
            options=DEFAULT_OPTIONS if options is None else options,
        )

    # async def display(self, image: Union[Image.Image, ImageHolder, Path, str]):
    #     if isinstance(image, str):
    #         image = GifHolder(image) if image.endswith(".gif") else ImageHolder(image)
    #     elif isinstance(image, Path):
    #         if image.is_dir():
    #             image = FrameHolder(image)
    #         elif image.suffix == ".gif":
    #             image = GifHolder(image)
    #         else:
    #             image = ImageHolder(image)
    #     elif isinstance(image, Image.Image):
    #         if getattr(image, "n_frames", 0) > 1:
    #             image = GifHolder(image)
    #         else:
    #             image = ImageHolder(image)
    #     elif not isinstance(image, ImageHolder):
    #         raise ValueError(
    #             f"image was not a valid type (got {image.__class__.__name__}"
    #         )
    #
    #     fut = asyncio.Future()
    #     await self.image_queue.put((image, fut))
    #     await fut
