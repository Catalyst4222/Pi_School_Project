import argparse

from utils import FormattedMatrix, get_holder
from utils import resize as resize_image


def main():
    parser = argparse.ArgumentParser(description="Display an image")
    parser.add_argument(
        "file",
        type=str,
    )
    parser.add_argument(
        "-r",
        "--resize",
        action="store_true",
        help="Resize the image to fit the board",
    )
    parser.add_argument(
        "-b",
        "--brightness",
        type=int,
        help="How bright the image should be. 0-100, default 100 (normal)",  # todo check if 100 is maximum
        default=100,
    )
    args = parser.parse_args()
    show(args.file, args.resize, brightness=args.brightness)


def show(file, resize=False, brightness=100):
    matrix = FormattedMatrix()
    holder = get_holder(file)

    if resize:
        print("resozed")

        resize_image(holder)
        holder.image.show()

    # todo brightness

    try:
        while True:
            holder.display(matrix)
    except KeyboardInterrupt:
        matrix.Clear()


if __name__ == "__main__":
    main()
