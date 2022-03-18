import sys

if len(sys.argv) < 2:
    sys.exit("Require an image argument")
else:
    image_file = sys.argv[1]

from PIL import Image, ImageSequence

print(f"Opening file {image_file}")
im = Image.open(image_file)


# Resize gif frames to matrix
def thumbnails(frames):
    for frame in frames:
        thumbnail = frame.copy()
        thumbnail.thumbnail((64, 32), Image.ANTIALIAS)  # Your matrix size here
        yield thumbnail


print("Gathering frames")
frames = thumbnails(ImageSequence.Iterator(im))

# Save output
print(f"Writing image to {image_file[:-4]}_out.gif")
om = next(frames)  # Handle first frame separately
om.info = im.info  # Copy sequence info
om.save(f"{image_file[:-4]}_out.gif", save_all=True, append_images=list(frames))

print("Done!")
