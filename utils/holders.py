import io
import json
import pathlib
import time
from typing import TYPE_CHECKING, Optional, Union

from PIL import Image, ImageSequence

from .constants import M_HEIGHT, M_WIDTH

if TYPE_CHECKING:
    from classes import DataDict

    try:
        from rgbmatrix import RGBMatrix
    except ImportError:
        from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions


class ImageHolder:
    def __init__(
        self,
        image: Union[str, "pathlib.Path", bytes, Image.Image],
        post_delay: float = 0,
    ):
        self.image: Image.Image = self.prep_image(image)
        self.post_delay: float = post_delay

    @staticmethod
    def prep_image(
        image: Union[str, "pathlib.Path", bytes, Image.Image]
    ) -> Image.Image:

        if not isinstance(image, Image.Image):
            image = Image.open(image)

        if image.width > M_WIDTH or image.height > M_HEIGHT:
            # Fit the image to the screen
            image.thumbnail((M_WIDTH, M_HEIGHT))

        return image

    def to_frames(self) -> list[Image.Image]:
        """Return all the individual frames of an image"""
        frames: list[Image.Image] = [
            frame.copy() for frame in ImageSequence.Iterator(self.image)
        ]
        print(f"adding delay, before: {frames[-1].info.get('duration')}")
        frames[-1].info["duration"] = frames[-1].info.get("duration", 0) + (
            self.post_delay * 1000
        )  # add delay and account for ms
        print(f"adding delay, after: {frames[-1].info.get('duration')}")
        return frames

    def display(self, matrix: "RGBMatrix"):
        matrix.SetImage(self.image.convert("RGB"))
        time.sleep(self.post_delay or self.image.info.get("duration", 0))


class GifHolder(ImageHolder):  # subclass woooo!
    @staticmethod
    def prep_image(
        image: Union[str, "pathlib.Path", bytes, Image.Image]
    ) -> Image.Image:
        if not isinstance(image, Image.Image):
            image = Image.open(image)

        if image.width > M_WIDTH or image.height > M_HEIGHT:
            # Fit the image to the screen
            image.thumbnail((M_WIDTH, M_HEIGHT))

        return image

    def display(self, matrix: "RGBMatrix"):
        # self.image.seek(1)
        # frames: list[Image.Image] = [
        #     frame.copy() for frame in ImageSequence.Iterator(self.image)
        # ]
        # for frame in frames:
        #     matrix.SetImage(frame.convert("RGB"))
        #     time.sleep(frame.info.get("duration", 0) / 1000)

        # this broke for some reason
        for frame, delay in enumerate(self.get_frame_timings(self.image)):
            self.image.seek(frame)
            # print(self.image.info)
            matrix.SetImage(self.image.convert("RGB"))
            # print(delay)
            time.sleep(delay / 1000)

        print("sleeping")
        time.sleep(self.post_delay)
        print("slept")

    @staticmethod
    def get_frame_timings(image: Image.Image) -> list[int]:
        image.seek(0)
        frame = 0
        durations: list[int] = []
        while True:
            try:
                frame += 1
                durations.append(image.info["duration"])
                image.seek(image.tell() + 1)
            except EOFError:
                return durations


class FrameHolder(GifHolder):  # Subclass due to being an "animation"
    # noinspection PyMissingConstructor
    def __init__(
        self,
        path: Union[str, "pathlib.Path"],
        post_delay: float = 0,
        export_to: Optional[Union[str, "pathlib.Path"]] = None,
    ):
        self.post_delay = post_delay

        folder_path = pathlib.Path(path)
        data: "DataDict" = json.loads((folder_path / "data.json").read_text())

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
                continue

            # checks the delay given by data.json, to be passed to post_delay
            delay = next(
                filter(lambda data_: data_["name"] == child.name, data["frames"]), {}
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

        durations = [first_image.info["duration"]] + [
            frame.info["duration"] for frame in first_frames
        ]
        extra_images = []

        for holder in frame_sets[1:]:
            for frame in holder.to_frames():
                durations.append(frame.info["duration"])
                extra_images.append(frame)

        first_image.save(
            stream,
            format="GIF",
            save_all=True,
            append_images=first_frames + extra_images,
            duration=durations,
        )

        stream.seek(0)

        self.image = Image.open(stream)
