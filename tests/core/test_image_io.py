from pathlib import Path

import cv2
import numpy as np
import pytest

from app.core.errors import ImageDecodeError, ImageLoadError
from app.core.image_io import decode_image, encode_image, load_image


def make_color_image() -> np.ndarray:
    """4x6 BGR image: left half pure red, right half pure blue."""
    image = np.zeros((4, 6, 3), dtype=np.uint8)
    image[:, :3] = (0, 0, 255)  # red in BGR
    image[:, 3:] = (255, 0, 0)  # blue in BGR
    return image


def test_load_png_returns_identical_pixels(tmp_path: Path) -> None:
    path = tmp_path / "image.png"
    original = make_color_image()
    cv2.imwrite(str(path), original)

    loaded = load_image(path)

    np.testing.assert_array_equal(loaded, original)


def test_load_jpg_returns_image_of_same_shape(tmp_path: Path) -> None:
    path = tmp_path / "image.jpg"
    cv2.imwrite(str(path), make_color_image())

    loaded = load_image(path)

    # JPG is lossy, so only the shape and type are compared.
    assert loaded.shape == (4, 6, 3)
    assert loaded.dtype == np.uint8


def test_load_keeps_grayscale_png_single_channel(tmp_path: Path) -> None:
    path = tmp_path / "gray.png"
    cv2.imwrite(str(path), np.full((5, 5), 128, dtype=np.uint8))

    loaded = load_image(path)

    assert loaded.shape == (5, 5)


def test_load_missing_file_raises_load_error(tmp_path: Path) -> None:
    with pytest.raises(ImageLoadError, match="does not exist"):
        load_image(tmp_path / "missing.png")


def test_load_unsupported_extension_raises_load_error(tmp_path: Path) -> None:
    path = tmp_path / "image.bmp"
    cv2.imwrite(str(path), make_color_image())

    with pytest.raises(ImageLoadError, match="Unsupported"):
        load_image(path)


def test_load_corrupted_file_raises_decode_error(tmp_path: Path) -> None:
    path = tmp_path / "broken.png"
    path.write_bytes(b"this is not an image")

    with pytest.raises(ImageDecodeError):
        load_image(path)


def test_decode_empty_bytes_raises_decode_error() -> None:
    with pytest.raises(ImageDecodeError):
        decode_image(b"")


def test_encode_then_decode_png_is_lossless() -> None:
    original = make_color_image()

    decoded = decode_image(encode_image(original, ".png"))

    np.testing.assert_array_equal(decoded, original)


def test_sample_image_red_square_stays_red(sample_image_path: Path) -> None:
    """Guards against swapped channels: the red square must have R >> B after loading."""
    image = load_image(sample_image_path)
    blue, green, red = image[100, 100]  # inside the red square (BGR order)

    assert red > 150
    assert blue < 100
    assert green < 100
