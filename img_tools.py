import os
import time

from PIL import Image, ImageSequence


# Resize gif frames to matrix
def resized_thumbnails(frames):
    for frame in frames:
        thumbnail = frame.copy()
        thumbnail.thumbnail((64, 32), Image.ANTIALIAS)  # Your matrix size here
        yield thumbnail


def load_gif(image_file: str) -> Image.Image:
    if not image_file.endswith("_out.gif"):
        new_file = f"{image_file[:-4]}_out.gif"

        if not os.path.exists(new_file):
            return prep_gif(image_file)
        image_file = new_file

    return Image.open(image_file)


def prep_gif(file):
    print(f"Resizing file {file}")
    im: Image.Image = Image.open(file)

    print("Gathering frames")
    frames = resized_thumbnails(ImageSequence.Iterator(im))

    # Save output
    print(f"Writing image to {file[:-4]}_out.gif")
    om = next(frames)  # Handle first frame separately
    print(type(om))
    om.info = im.info  # Copy sequence info
    om.save(f"{file[:-4]}_out.gif", save_all=True, append_images=list(frames))

    return om


def play_image(matrix, image: Image.Image):
    for frame in range(image.n_frames):
        image.seek(frame)
        print(image.info["duration"])
        matrix.SetImage(image.convert("RGB"))
        time.sleep(image.info["duration"] / 1000)
