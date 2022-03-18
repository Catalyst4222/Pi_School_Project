import sys
import time
from typing import TYPE_CHECKING, Union

from PIL import Image

if TYPE_CHECKING:
    import pathlib

    try:
        from rgbmatrix import RGBMatrix
    except ImportError:
        from RGBMatrixEmulator import RGBMatrix

# Hardcoded, fight me
M_WIDTH = 64
M_HEIGHT = 32


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


class ImageHolder:
    def __init__(
        self, image: Union[str, "pathlib.Path", bytes, Image.Image], post_delay: float = 0
    ):
        self.image: Image.Image = self.prep_image(image)
        self.post_delay: float = post_delay

    @staticmethod
    def prep_image(image: Union[str, "pathlib.Path", bytes, Image.Image]) -> Image.Image:

        if not isinstance(image, Image.Image):
            image = Image.open(image)

        if image.width > M_WIDTH or image.height > M_HEIGHT:
            # Fit the image to the screen
            image.thumbnail((M_WIDTH, M_HEIGHT))

        return image

    #


    def display(self, matrix: "RGBMatrix"):
        matrix.SetImage(self.image.convert("RGB"))
        time.sleep(self.image.info.get("duration") or self.post_delay)


class GifHolder(ImageHolder):  # subclass woooo!
    @classmethod
    def from_file(
        cls, file: Union[str, "pathlib.Path"]
    ):  # to do figure out how to load other ways
        # Prefer preproccessed images, less loading time
        if not str(file).endswith("_out.py"):
            ...  # wtf do I do here?
            print("You should really prep the image", file=sys.stderr)

        image: Image.Image = Image.open(file)




    def display(self, matrix: "RGBMatrix"):
        for image in self.images:
            image.display(matrix)

        time.sleep(self.post_delay)
