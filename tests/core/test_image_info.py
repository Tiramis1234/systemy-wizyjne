import numpy as np

from app.core.image_info import ImageInfo, describe_image


def test_describe_color_image() -> None:
    image = np.zeros((420, 640, 3), dtype=np.uint8)

    assert describe_image(image) == ImageInfo(width=640, height=420, channels=3, dtype="uint8")


def test_describe_grayscale_image_has_one_channel() -> None:
    image = np.zeros((10, 20), dtype=np.uint8)

    assert describe_image(image).channels == 1


def test_describe_reports_16_bit_dtype() -> None:
    image = np.zeros((10, 20, 4), dtype=np.uint16)

    info = describe_image(image)

    assert info.channels == 4
    assert info.dtype == "uint16"
