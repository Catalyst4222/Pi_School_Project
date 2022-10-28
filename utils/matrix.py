import atexit
from atexit import register
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from queue import Queue
from threading import Thread
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

        self._thread: Thread = Thread(target=self._display_screen)
        self._running: bool = True
        self.image_queue: Queue[ImageHolder] = Queue()

        atexit.register(self.stop)
        atexit.register(lambda: print("stopping"))
        self._thread.start()

    def _display_screen(self):
        """Continuously grab an image from the queue and display it"""
        while self._running:
            print("a")
            image = self.image_queue.get()
            print("b")
            # self.display(image)
            image.display(self)

            if not self.image_queue.qsize():
                self.image_queue.put(image)

            ...  # more?

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

        self.image_queue.put(image)

    def stop(self):
        print("a")
        self._running = False

    @property
    def running(self):
        return self._running

    def __del__(self):
        self._running = False
        del self._thread
