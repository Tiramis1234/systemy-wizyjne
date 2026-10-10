import numpy as np
import pytest

from app.core.errors import UnsupportedImageError
from app.core.image_stats import HISTOGRAM_BINS, brightness_stats


def test_uniform_image() -> None:
    stats = brightness_stats(np.full((10, 10), 100, dtype=np.uint8))

    assert stats.mean == pytest.approx(100)
    assert stats.std == pytest.approx(0)
    assert (stats.min, stats.max) == (100, 100)
    assert stats.dark_fraction == 0
    assert stats.bright_fraction == 0


def test_half_black_half_white() -> None:
    image = np.zeros((10, 10), dtype=np.uint8)
    image[:, 5:] = 255

    stats = brightness_stats(image)

    assert stats.mean == pytest.approx(127.5)
    assert stats.std == pytest.approx(127.5)
    assert stats.dark_fraction == pytest.approx(0.5)
    assert stats.bright_fraction == pytest.approx(0.5)


def test_histogram_counts_every_pixel_in_the_right_bin() -> None:
    image = np.zeros((4, 5), dtype=np.uint8)  # 20 pixels
    image[0, :] = 255

    histogram = brightness_stats(image).histogram

    assert len(histogram) == HISTOGRAM_BINS
    assert sum(histogram) == 20
    assert histogram[0] == 15
    assert histogram[-1] == 5


def test_color_image_uses_luminance() -> None:
    image = np.zeros((2, 2, 3), dtype=np.uint8)
    image[:, :] = (0, 255, 0)  # pure green -> luminance 150

    assert brightness_stats(image).mean == pytest.approx(150)


def test_non_8_bit_image_is_rejected() -> None:
    with pytest.raises(UnsupportedImageError, match="8-bit"):
        brightness_stats(np.zeros((2, 2), dtype=np.uint16))
