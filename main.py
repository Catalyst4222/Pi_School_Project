import time
from typing import Literal

from PIL import Image

import utils
from utils import (
    M_HEIGHT,
    M_WIDTH,
    FormattedMatrix,
    GifHolder,
    ImageHolder,
    holders,
    transitions,
)

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


# Color = tuple[char, char, char]

import webpanel.server

matrix = FormattedMatrix()
print(matrix)

# matrix.display(GifHolder(Image.open("proto_neutral.gif")))
webpanel.server.start_server(matrix)
