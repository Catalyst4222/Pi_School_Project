import time
from typing import Literal

from utils import holders, transitions
from utils.matrix import FormattedMatrix

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








matrix = FormattedMatrix()
matrix.Fill(0xBB, 255, 255)
i = 1

# rms
# low 100-
# med 100-1000
# high 1000+
# cap = ~15000

# decibles
# "none" 20
# med 30-50
# high 50+
# canvas = matrix.CreateFrameCanvas()
transitions.panImage(matrix, holders.ImageHolder("neutral.gif"))
while True:
    time.sleep(500)
    ...


