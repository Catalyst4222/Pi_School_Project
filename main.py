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

    image_folder = pathlib.Path(sys.argv[1])

import img_tools

# os.getcwd()  # TODO search for pre-scaled image

# path = os.path.abspath(image_file)
# print(path)
# assert isinstance(path, str)
if not image_folder.is_dir():
    sys.exit("Must be a folder")

pictures = [
    img_tools.load_gif(str(image))
    for image in image_folder.iterdir()
    if not str(image).endswith("_out.gif")
]
idle = pictures.pop(0)

print(len(pictures))

while True:
    now = time.time()
    while time.time() < now + 5:
        img_tools.play_image(matrix, idle)
    img_tools.play_image(matrix, random.choice(pictures))
