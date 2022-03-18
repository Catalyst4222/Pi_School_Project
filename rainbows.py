#!/usr/bin/env python3
import itertools
import math
import sys
import time

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

matrix = RGBMatrix(options=options)


def gen_rainbow(offset):
    frequency = 0.3
    for i in range(offset, offset + 32):
        red = math.sin(frequency * i + 0) * 127 + 128
        green = math.sin(frequency * i + 2) * 127 + 128
        blue = math.sin(frequency * i + 4) * 127 + 128

        yield red, green, blue


try:
    print("Press CTRL-C to stop.")
    for i in itertools.count():
        for row in range(matrix.width):

            for col, (r, g, b) in zip(
                range(matrix.height), itertools.cycle(gen_rainbow(i + row))
            ):
                matrix.SetPixel(row, col, r, g, b)
        time.sleep(0.01)

except KeyboardInterrupt:
    sys.exit(0)
