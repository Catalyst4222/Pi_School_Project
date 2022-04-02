"""A set of functions for transitioning images. Credit goes to MuneLitJolty#0447"""
from .classes import Color
from .holders import ImageHolder
from .matrix import M_HEIGHT, M_WIDTH

try:
    from rgbmatrix import RGBMatrix
except ImportError:
    from RGBMatrixEmulator import RGBMatrix


def panColor(matrix: RGBMatrix, color: Color, speed: int = 1, inverse: int = False):
    """
    Fill the matrix from one side to the other with the set color

    :param matrix: The matrix to display on
    :type matrix: RGBMatrix
    :param color: The color to fill with
    :type color: Color
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
    color,
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
    :type color: Color
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


def crossFade(matrix: RGBMatrix, color: Color, speed: int = 1):
    """
    Draw sets of alternating lines from both sides of the matrix

    :param matrix: The matrix to display on
    :type matrix: RGBMatrix
    :param color: The color to fill with
    :type color: Color
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
