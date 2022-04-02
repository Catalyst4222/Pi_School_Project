import sys
import time

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

# from PIL import Image
#
# if len(sys.argv) < 2:
#     sys.exit("Require an image argument")
# else:
#     image_file = sys.argv[1]
#
# image = Image.open(image_file)

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


# # Make image fit our screen.
# image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
# matrix.SetImage(image.convert('RGB'))

# for x in range(matrix.width):
#     for y in range(matrix.height):
#         matrix.SetPixel(x, y, x, y, 555)


def flipper(thing):
    """`[1,2,3,4]` -> `[1,4,2,3]`"""
    res = []
    while thing:
        res.append(thing[0])
        thing = thing[:0:-1]

    return res


try:
    print("Press CTRL-C to stop.")
    # Control which way the lines are filled in
    forwards = 1
    up = 1

    while True:
        for i, (sideside, topbottom) in enumerate(
            zip(  # i to help prevent recoloring pixels
                flipper(
                    list(range(matrix.width))[::-1]
                ),  # sideside for left and right sides
                flipper(
                    list(range(matrix.height))
                ),  # topbottom for the top and bottom sides
            )
        ):
            print(f"{sideside=}, {topbottom=}")
            i = i // 2  # prevent scaling issues

            for leftright in list(range(i, matrix.width - i))[
                ::forwards
            ]:  # fill ceilings/floors
                matrix.SetPixel(leftright, topbottom, 64, 64, 64)
                print(f"{sideside=}, {topbottom=}, {leftright=}")
                time.sleep(0.01)

            for updown in list(range(i, matrix.height - i))[::up]:
                matrix.SetPixel(sideside, updown, 64, 64, 64)
                print(f"{sideside=}, {topbottom=}, {updown=}")
                time.sleep(0.01)

            forwards *= -1
            up *= -1

        matrix.Clear()
except KeyboardInterrupt:
    sys.exit(0)
