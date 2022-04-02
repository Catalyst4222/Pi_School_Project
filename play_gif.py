import sys
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

    image_file = sys.argv[1]


image = img_tools.load_gif(image_file)

while True:
    img_tools.play_image(matrix, image)
