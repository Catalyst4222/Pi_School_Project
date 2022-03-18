import itertools
import math
import os
import pathlib
import random
import sys
import time
from collections import deque, namedtuple
from random import randint
from threading import Thread
from typing import Annotated, Literal, Sequence

from PIL import Image, ImageSequence

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
# options.pixel_mapper_config = 'adafruit-hat'
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat"  # If you have an Adafruit HAT: 'adafruit-hat'
# options.gpio_slowdown = 1
# options.disable_hardware_pulsing = True


# noinspection PyTypeHints
char = Literal[tuple(range(256))]
Color = tuple[char, char, char]

matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()


if len(sys.argv) < 2:
    sys.exit("Require an image argument")
    # image_file = "saab-1496319292.gif"
else:

    image_file = sys.argv[1]

import img_tools

image = img_tools.load_gif(image_file)

while True:
    img_tools.play_image(matrix, image)
    time.sleep(5)
