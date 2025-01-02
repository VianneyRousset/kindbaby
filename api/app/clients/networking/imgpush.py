import io

import requests

from app.config import Config
from app.schemas.networking.imgpush import ImgpushUploadResponse

TIMEOUT = 2

# TODO avoid hardcoding image format

# CREATE


def upload_image(config: Config, fp: io.IOBase) -> ImgpushUploadResponse:
    response = requests.post(
        url=config.imgpush_url,
        timeout=TIMEOUT,
        files={"file": ("file.jpg", fp, "image/jpeg")},
    )

    # TODO handler raised exceptions
    response.raise_for_status()

    return ImgpushUploadResponse(**response.json())


# READ


def get_image(config: Config, name: str) -> bytes:
    response = requests.get(
        url=f"{config.imgpush_url}/{name}.jpg",
        timeout=TIMEOUT,
    )

    # TODO handler raised exceptions
    response.raise_for_status()

    return response.content
