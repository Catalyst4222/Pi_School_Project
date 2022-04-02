from typing import Optional

try:
    from rgbmatrix import RGBMatrix
except ImportError:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions


# Hardcoded, fight me
M_WIDTH = 64
M_HEIGHT = 32

DEFAULT_OPTIONS = RGBMatrixOptions()
DEFAULT_OPTIONS.cols = M_WIDTH
DEFAULT_OPTIONS.rows = M_HEIGHT
DEFAULT_OPTIONS.chain_length = 1
DEFAULT_OPTIONS.parallel = 1
DEFAULT_OPTIONS.hardware_mapping = "adafruit-hat"


class FormattedMatrix(RGBMatrix):  # todo add helper methods
    def __init__(self, options: Optional[RGBMatrixOptions] = None):
        super().__init__(
            options=DEFAULT_OPTIONS if options is None else options,
        )
