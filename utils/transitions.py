"""A set of functions for transitioning images. Credit goes to MuneLitJolty#0447"""
import time
from typing import Union

from .classes import Color
from .constants import M_HEIGHT, M_WIDTH
from .holders import ImageHolder

try:
    from rgbmatrix import RGBMatrix
except ImportError:
    from RGBMatrixEmulator import RGBMatrix


def panColor(
    matrix: RGBMatrix,
    color: Union[Color, tuple[int, int, int]],
    speed: int = 1,
    inverse: int = False,
):
    """
    Fill the matrix from one side to the other with the set color

    :param matrix: The matrix to display on
    :type matrix: RGBMatrix
    :param color: The color to fill with
    :type color: Union[Color, tuple[int, int, int]]
    :param speed: How many pixels to fill in a loop
    :type speed: int
    :param inverse: Go right to left instead of left to right, default False
    :type inverse: bool
    """
    canvas = matrix.CreateFrameCanvas()
    for x in range(M_WIDTH):
        if inverse:
            x = M_WIDTH - (x + 1)
        for y in range(M_HEIGHT):
            canvas.SetPixel(x, y, *color)
        if x % speed == 0:
            matrix.SwapOnVSync(canvas)


def panLines(
    matrix: RGBMatrix,
    color: Union[Color, tuple[int, int, int]],
    gap: int = 1,
    offset: int = 0,
    speed: int = 1,
    inverse: bool = False,
):
    """
    Fill the matrix from one side to the other lines of the set color

    :param matrix: The matrix to display on
    :type matrix: RGBMatrix
    :param color: The color to fill with
    :type color: Union[Color, tuple[int, int, int]]
    :param gap: How many lines to leave between each stroke, default 1
    :type gap: int
    :param offset: How many lines down to start
    :type offset: int
    :param speed: How many pixels to fill in a loop
    :type speed: int
    :param inverse: Go right to left instead of left to right, default False
    :type inverse: bool
    """
    canvas = matrix.CreateFrameCanvas()
    for x in range(M_WIDTH):
        if inverse:
            x = M_WIDTH - (x + 1)
        for y in range(M_HEIGHT):
            if (y + offset) % (gap + 1) == 0:
                canvas.SetPixel(x, y, *color)
        if x % speed == 0:
            matrix.SwapOnVSync(canvas)


def crossFill(
    matrix: RGBMatrix, color: Union[Color, tuple[int, int, int]], speed: int = 1
):
    """
    Draw sets of alternating lines from both sides of the matrix

    :param matrix: The matrix to display on
    :type matrix: RGBMatrix
    :param color: The color to fill with
    :type color: Union[Color, tuple[int, int, int]]
    :param speed: How many pixels to fill in a loop
    :type speed: int
    """
    canvas = matrix.CreateFrameCanvas()
    for x in range(M_WIDTH):
        for y in range(M_HEIGHT):
            if y % 2 == 0:
                canvas.SetPixel(x, y, *color)
            else:
                canvas.SetPixel(M_WIDTH - (x + 1), y, *color)
        if x % speed == 0:
            matrix.SwapOnVSync(canvas)


def panImage(matrix: RGBMatrix, image: ImageHolder):
    canvas = matrix.CreateFrameCanvas()
    for x in range(M_WIDTH):
        for y in range(M_HEIGHT):
            print(image.image.getpixel((x, y)))
            canvas.SetPixel(x, y, *image.image.getpixel((x, y)))
        matrix.SwapOnVSync(canvas)


def fadeImage(
    matrix: RGBMatrix,
    origin: ImageHolder,
    destination: ImageHolder,
    steps: int = 8,
    delay: float = 0.1,
):
    """
    Fades the display from one image to another

    :param matrix: The matrix to display on
    :type matrix: RGBMatrix
    :param origin: The image to start the transition from (will be `.display`ed)
    :type origin: ImageHolder
    :param destination: The image to end on (will be `.display`ed)
    :type destination: ImageHolder
    :param steps: How many frames to show in the transition
    :type steps: int
    :param delay: How long to show each step
    :type delay: float
    :return:
    :rtype:
    """
    origin.display(matrix)  # solid starting screen

    per_step = 256 // steps  # how much to shift per cycle

    layer = (
        destination.to_frames()[0]
        .convert("RGBA")
        .resize(
            (M_WIDTH, M_HEIGHT),
        )
    )  # will appear over time

    base = (
        origin.to_frames()[-1]
        .convert("RGBA")
        .resize(
            (M_WIDTH, M_HEIGHT),
        )
    )  # will disappear over time

    for step in range(steps):
        layer.putalpha(step * per_step)  # scale up visibility
        print(step * per_step)
        to_show = base.copy()  # copy to not overwrite
        to_show.paste(layer, (0, 0), layer)

        matrix.SetImage(to_show.convert("RGB"))
        time.sleep(delay)

    destination.display(matrix)  # solid ending screen
