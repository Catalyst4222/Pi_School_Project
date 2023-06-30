try:
    from rgbmatrix import RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import RGBMatrixOptions

M_WIDTH = 64
M_HEIGHT = 32

DEFAULT_OPTIONS = RGBMatrixOptions()
DEFAULT_OPTIONS.cols = M_WIDTH
DEFAULT_OPTIONS.rows = M_HEIGHT
DEFAULT_OPTIONS.chain_length = 1
DEFAULT_OPTIONS.parallel = 1
DEFAULT_OPTIONS.hardware_mapping = "adafruit-hat"
