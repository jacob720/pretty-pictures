import json
from pathlib import Path

from PIL import Image

FILE_TYPES = ["png", "jpg", "jpeg", "tif", "tiff"]


def get_weights(r: float, g: float, b: float) -> list[int, int, int]:
    return [int(r % 256 if r else 0), int(g % 256 if g else 0), int(b % 256 if b else 0)]


def get_parameters(png: int, jpg: int, jpeg: int, tif: int, tiff: int):
    params = (
        [
            {
                "width": 500,
                "height": 500,
                "weights": get_weights(255, 1 + i, 100 - i),
                "extension": "png",
            }
            for i in range(png)
        ]
        + [
            {
                "width": 600,
                "height": 200,
                "weights": get_weights(100 + i, 150 - i, 100),
                "extension": "jpg",
            }
            for i in range(jpg)
        ]
        + [
            {
                "width": 300,
                "height": 400,
                "weights": get_weights(100 - i, 150, 100 + i),
                "extension": "jpeg",
            }
            for i in range(jpeg)
        ]
        + [
            {
                "width": 300,
                "height": 200,
                "weights": get_weights(230 - 2 * i, 100 - 0.5 * i, 1 + i),
                "extension": "tif",
            }
            for i in range(tif)
        ]
        + [
            {
                "width": 200,
                "height": 300,
                "weights": get_weights(230 - 5 * i, 100 + 5 * i, 1 + 10 * i),
                "extension": "tiff",
            }
            for i in range(tiff)
        ]
    )

    return [image_params for image_params in params if image_params is not None]


json.dumps([])


def save_image(
    image,
    name="generated_image",
    extension="png",
):
    Path("images").mkdir(parents=True, exist_ok=True)
    image.save(f"images/{name}.{extension}")


def create_pattern(
    width: int,
    height: int,
    weights: tuple[int, int, int],
) -> Image.Image:
    image = Image.new("RGB", (width, height))
    pixels = image.load()
    for i in range(width):
        for j in range(height):
            pixels[i, j] = (
                (i + j * 50) % weights[0] if weights[0] else 0,
                weights[1],
                (i * 300 + j) % weights[2] if weights[2] else 0,
            )
    return image


# def save_h5(images: list):


params = get_parameters(png=256, jpg=0, jpeg=0, tif=0, tiff=0)
print(len(params))
for i, image_params in enumerate(params):
    image = create_pattern(
        image_params["width"], image_params["height"], image_params["weights"]
    )
    save_image(image, name=f"image-{i}", extension=image_params["extension"])
