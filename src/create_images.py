import json
import time
from collections.abc import Generator, Iterable, Iterator
from pathlib import Path
import imageio.v3 as iio

import numpy as np
from PIL import Image
from itertools import tee
from templates import Template

FILE_TYPES = ["png", "jpg", "jpeg", "tif", "tiff"]


def get_weights(
    r: float,
    g: float,
    b: float,
    turn_back_r=False,
    turn_back_g=False,
    turn_back_b=False,
) -> list[int, int, int]:
    return {
        "r": int(
            r % 256 if ((not turn_back_r) or ((r // 256) % 2 == 0)) else 256 - r % 256
        ),
        "g": int(
            g % 256 if ((not turn_back_g) or ((g // 256) % 2 == 0)) else 256 - g % 256
        ),
        "b": int(
            b % 256 if ((not turn_back_b) or ((b // 256) % 2 == 0)) else 256 - b % 256
        ),
    }


def get_parameters(n: int, template: Template) -> Generator[dict]:
    params = (
        {
            "width": template.width,
            "height": template.height,
            "weights": get_weights(
                template.initial_r + i * template.velocity_r,
                template.initial_g + i * template.velocity_g,
                template.initial_b + i * template.velocity_g,
                template.turn_back_r,
                template.turn_back_g,
                template.turn_back_b,
            ),
            "levels": {
                "r": template.level_r,
                "g": template.level_g,
                "b": template.level_b,
            },
        }
        for i in range(n)
    )
    return (image_params for image_params in params if image_params is not None)


def create_pattern(width: int, height: int, weights: dict, levels: dict) -> np.ndarray:
    x = np.arange(width).reshape(-1, 1)
    y = np.arange(height).reshape(1, -1)

    r = (
        ((0.5 * x + y) % weights["r"]) * levels["r"]
        if weights["r"]
        else np.zeros_like(x + y)
    )
    g = (
        ((1 * x + 10 * y) % weights["g"]) * levels["g"]
        if weights["g"]
        else np.zeros_like(x + y)
    )
    b = (
        ((x + 3 * y) % weights["b"]) * levels["b"]
        if weights["b"]
        else np.zeros_like(x + y)
    )
    return np.stack([r, g, b], axis=-1).astype(np.uint8)


def create_image(image_array: np.ndarray):
    return Image.fromarray(image_array, "RGB")


def save_image(
    image: Image.Image,
    name: str = "generated_image",
    extension: str = "png",
):
    Path("images").mkdir(parents=True, exist_ok=True)
    path = f"images/{name}.{extension}"
    image.save(path)
    return path


def save_images(images: Iterable[Image.Image], extension="png") -> list[str]:
    paths = [
        save_image(image, f"image-{i}", extension=extension)
        for i, image in enumerate(images)
    ]
    return paths


def save_mp4(
    frames: Iterable[np.ndarray],
    filename: str = "result.mp4",
    fps=20,
    quality: int = 10,
):
    iio.imwrite(filename, list(frames), fps=fps, codec="libx264", quality=quality)


def save_gif(paths: Iterable[str]):
    print("saving gif")
    first = Image.open(paths[0])
    rest = (Image.open(f) for f in paths)
    first.save("result.gif", save_all=True, append_images=rest, duration=30, loop=0)


template = Template(
    width=608,
    height=608,
    initial_r=255,
    initial_g=1,
    initial_b=100,
    velocity_r=-0.5,
    velocity_g=0.7,
    velocity_b=-1,
    level_g=0.6,
    turn_back_r=True,
    turn_back_g=True,
    turn_back_b=True,
)
t1 = time.time()
params = get_parameters(200, template)
patterns = (
    create_pattern(
        image_params["width"],
        image_params["height"],
        image_params["weights"],
        image_params["levels"],
    )
    for image_params in params
)

save_mp4(patterns)
# save_images(create_image(pattern) for pattern in patterns[:2000])
print(len(list(patterns)))

t2 = time.time()
print(f"total time in seconds: {round(t2 - t1, 2)}")
