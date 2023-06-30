import asyncio
import queue
import threading
from pathlib import Path
from typing import Union

from PIL import Image

try:
    from RGBMatrix import RGBMatrix
except ImportError:
    from RGBMatrixEmulator import RGBMatrix

from utils import FrameHolder, GifHolder, ImageHolder


def set_result(future: asyncio.Future, result):
    if not future.done():
        future.set_result(result)


def resolve(future: asyncio.Future, result=None):
    loop = future.get_loop()
    loop.call_soon_threadsafe(set_result, future, result)


class Display(threading.Thread):
    """A class to display things asynchronously"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queue: queue.Queue[
            tuple[asyncio.Future, ImageHolder, RGBMatrix]
        ] = queue.Queue()
        self.running = True

    async def display(
        self, image: Union[Image.Image, ImageHolder, Path, str], matrix: RGBMatrix
    ):
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

        fut = asyncio.get_event_loop().create_future()
        self.queue.put_nowait((fut, image, matrix))
        await fut

    def run(self):
        # Inspired from the aiosqlite library, though it is missing the try/except part
        while True:
            try:
                fut, image, matrix = self.queue.get(timeout=0.1)
            except queue.Empty:
                if self.running:
                    continue
                break

            image.display(matrix)

            resolve(fut)
