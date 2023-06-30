import argparse

from utils import FormattedMatrix


def main(file):
    matrix = FormattedMatrix()
    try:
        while True:
            matrix.display(file)
    except KeyboardInterrupt:
        matrix.Clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display an image")
    parser.add_argument(
        "file",
        type=str,
    )
    file = parser.parse_args().file
    main(file)
