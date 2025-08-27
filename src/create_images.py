import json
from collections.abc import Generator, Iterable, Iterator
from pathlib import Path

from PIL import Image

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
    return [
        int(r % 256 if ((not turn_back_r) or ((r // 256) % 2 == 0)) else 256 - r % 256),
        int(g % 256 if ((not turn_back_g) or ((g // 256) % 2 == 0)) else 256 - g % 256),
        int(b % 256 if ((not turn_back_b) or ((b // 256) % 2 == 0)) else 256 - b % 256),
    ]


def get_parameters(n: int, template: Template) -> Generator:
    params = (
        {
            "width": template.width,
            "height": template.height,
            "weights": get_weights(
                template.initial_r + i * template.velocity_r,
                template.initial_g + i * template.velocity_g,
                template.initial_b + i * template.velocity_g,
            ),
        }
        for i in range(n)
    )
    return (image_params for image_params in params if image_params is not None)


def save_image(
    image,
    name="generated_image",
    extension="png",
):
    Path("images").mkdir(parents=True, exist_ok=True)
    path = f"images/{name}.{extension}"
    image.save(path)
    return path


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


def save_gif(paths: Iterable[str]):
    print("saving gif")
    first = Image.open(paths[0])
    rest = (Image.open(f) for f in paths)
    first.save("result.gif", save_all=True, append_images=rest, duration=20, loop=0)


# def save_h5(images: list):

template = Template(
    width=500,
    height=500,
    initial_r=255,
    initial_g=1,
    initial_b=100,
    velocity_r=-0.2,
    velocity_g=1,
    velocity_b=-1,
)
params = get_parameters(2000, template)
paths = []
for i, image_params in enumerate(params):
    image = create_pattern(
        image_params["width"], image_params["height"], image_params["weights"]
    )
    paths.append(save_image(image, name=f"image-{i}", extension="png"))
print(len(paths))
save_gif(paths)
