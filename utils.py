import io
import json
import sys
import time
from typing import TYPE_CHECKING, Union, TypedDict, Optional
import pathlib

from PIL import Image, ImageSequence

if TYPE_CHECKING:
    try:
        from rgbmatrix import RGBMatrix
    except ImportError:
        from RGBMatrixEmulator import RGBMatrix


    # Todo move to another file
    class FrameData(TypedDict):
        name: str
        delay: float
        order: int


    class DataDict(TypedDict):
        frames: list[FrameData]
        resolved: bool
        export_to: str
        import_from: str

# Hardcoded, fight me
M_WIDTH = 64
M_HEIGHT = 32


class Pixel:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y

    def copy(self):
        return self.__class__(self.x, self.y)

    def __repr__(self):
        return f"<Pixel(x={self.x}, y={self.y})>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError  # Should make good error message sometime
        return self.x == other.x and self.y == other.y


class ImageHolder:
    def __init__(
            self, image: Union[str, "pathlib.Path", bytes, Image.Image], post_delay: float = 0
    ):
        self.image: Image.Image = self.prep_image(image)
        self.post_delay: float = post_delay

    @staticmethod
    def prep_image(image: Union[str, "pathlib.Path", bytes, Image.Image]) -> Image.Image:

        if not isinstance(image, Image.Image):
            image = Image.open(image)

        if image.width > M_WIDTH or image.height > M_HEIGHT:
            # Fit the image to the screen
            image.thumbnail((M_WIDTH, M_HEIGHT))

        return image

    def to_frames(self) -> list[Image.Image]:
        """Return all the individual frames of an image"""
        frames: list[Image.Image] = [frame.copy() for frame in ImageSequence.Iterator(self.image)]
        print(f"adding delay, before: {frames[-1].info['duration']}")
        frames[-1].info["duration"] += (self.post_delay * 1000)  # add delay and account for ms
        print(f"adding delay, after: {frames[-1].info['duration']}")
        return frames

    def display(self, matrix: "RGBMatrix"):
        matrix.SetImage(self.image.convert("RGB"))
        time.sleep(self.post_delay or self.image.info.get("duration"))


class GifHolder(ImageHolder):  # subclass woooo!
    @staticmethod
    def prep_image(image: Union[str, "pathlib.Path", bytes, Image.Image]) -> Image.Image:
        if not isinstance(image, Image.Image):
            image = Image.open(image)

        if image.width > M_WIDTH or image.height > M_HEIGHT:
            # Fit the image to the screen
            image.thumbnail((M_WIDTH, M_HEIGHT))

        return image

    def display(self, matrix: "RGBMatrix"):
        for frame in range(self.image.n_frames):
            self.image.seek(frame)
            matrix.SetImage(self.image.convert("RGB"))
            print(self.image.info["duration"])
            time.sleep(self.image.info["duration"] / 1000)

        print("sleeping")
        time.sleep(self.post_delay)
        print("slept")


class FrameHolder(GifHolder):  # Subclass due to being an "animation"
    # noinspection PyMissingConstructor
    def __init__(
            self, path: Union[str, "pathlib.Path"], post_delay: float = 0,
            export_to: Optional[Union[str, "pathlib.Path"]] = None
    ):
        self.post_delay = post_delay

        folder_path = pathlib.Path(path)
        data: DataDict = json.loads((folder_path / "data.json").read_text())

        if export_to is None:
            export_to = data.get("export_to")

        # noinspection PyUnboundLocalVariable
        if (
            data.get("resolved")
            and (import_from := data.get("import_from"))
            and pathlib.Path(import_from).exists()
        ):
            # The file has already been made, and data says it's good
            print(f"fetching image for {path} from resolved")
            self.image = Image.open(import_from)
            return

        valid_children = [frame["name"] for frame in data["frames"]]

        children = folder_path.iterdir()
        frame_sets = []

        # rather bad memory management
        for child in children:
            if child.name not in valid_children:
                # del child
                continue

            # checks the delay given by data.json, to be passed to post_delay
            delay = next(
                filter(lambda data_: data_["name"] == child.name, data["frames"]),
                {}
            ).get("delay", 0)

            if child.is_dir() and (child / "data.json").exists():
                # recursive animation folder
                frame_sets.append(FrameHolder(child, post_delay=delay))

            elif child.suffix == ".gif":
                gif = GifHolder(child, post_delay=delay)
                frame_sets.append(gif)

            else:
                frame_sets.append(ImageHolder(child, post_delay=delay))

        stream = open(export_to, "wb+") if (export_to is not None) else io.BytesIO()

        first_frames = frame_sets[0].to_frames()
        first_image = first_frames[0]

        durations = [first_image.info["duration"]] + [frame.info["duration"] for frame in first_frames]
        extra_images = []

        for holder in frame_sets[1:]:
            for frame in holder.to_frames():
                durations.append(frame.info["duration"])
                extra_images.append(frame)

        first_image.save(stream, format="GIF", save_all=True,
                         append_images=first_frames + extra_images, duration=durations)

        stream.seek(0)

        self.image = Image.open(stream)
