import time
from typing import Literal

from PIL import Image

import utils
from utils import GifHolder, ImageHolder, holders, transitions
from utils.matrix import M_HEIGHT, M_WIDTH, FormattedMatrix

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

# if len(sys.argv) < 2:
#     sys.exit("Require an image argument")
#     # image_file = "saab-1496319292.gif"
# else:
#
#     image_folder = pathlib.Path(sys.argv[1])


# os.getcwd()

# path = os.path.abspath(image_file)
# print(path)
# assert isinstance(path, str)
# if not image_folder.is_dir():
#     sys.exit("Must be a folder")
#
# pictures = [
#     img_tools.load_gif(str(image))
#     for image in image_folder.iterdir()
#     if not str(image).endswith("_out.gif")
# ]
# idle = pictures.pop(0)
#
# print(len(pictures))
#
# while True:
#     now = time.time()
#     while time.time() < now + 5:
#         img_tools.play_image(matrix, idle)
#     img_tools.play_image(matrix, random.choice(pictures))


#
# gif = utils.GifHolder("proto_neutral.gif", post_delay=0)
# while True:
#     gif.display(matrix)


# animation = utils.FrameHolder("animations")
matrix = FormattedMatrix()


def avg(a, b):
    return (a + b) // 2


# matrix.Fill(88, 255, 255)
im1 = Image.new("RGB", (M_WIDTH, M_HEIGHT), 0xBBFFFF)
im1.info["duration"] = 0
# im2 = Image.new("RGB", (M_WIDTH, M_HEIGHT), 0xFFFFFF)
utils.fadeImage(matrix, ImageHolder("rainbow.png"), GifHolder("proto_neutral.gif"))
i = 1
print("kauwegf")
# matrix.SetImage(Image.new("RGB", (M_WIDTH, M_HEIGHT), 0xFFD700))
# print(image := Image.open("proto_neutral.gif"))
# print(image.n_frames)
while True:
    utils.GifHolder("proto_neutral.gif").display(matrix)

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
    # transitions.fade(matrix, holders.ImageHolder("neutral.gif"))
    # while True:
    #     time.sleep(500)
    ...
    #     animation.display(matrix)
    # base = utils.ImageHolder("proto_neutral.gif", post_delay=0.001)
    # for i in range(64):
    # print('a')
    # i = int(audio.get_volume())
    # print(i)
    # canvas.Fill(0, 0, 0)
    #
    # a = min(i, 64)
    #
    # # base.display(canvas)
    #
    # block = Image.new('1', (64 - a, 32), 0xFFFFFF)
    # canvas.SetImage(block.convert("RGB"), a)
    #
    # matrix.SwapOnVSync(canvas)


# while True:
