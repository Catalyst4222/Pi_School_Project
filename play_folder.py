import pathlib
import random
import sys
import time
from typing import Literal

import img_tools

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat"  # If you have an Adafruit HAT: 'adafruit-hat'


# noinspection PyTypeHints
char = Literal[tuple(range(256))]
Color = tuple[char, char, char]

matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()


if len(sys.argv) < 2:
    sys.exit("Require an image argument")
else:

    image_folder = pathlib.Path(sys.argv[1])



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
