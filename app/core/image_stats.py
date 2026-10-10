"""Brightness statistics used to compare two lighting conditions.

All values are computed on the luminance (grayscale) image, because lighting
changes brightness; color is not compared in P01.
"""

from dataclasses import dataclass

import numpy as np

from app.core.errors import UnsupportedImageError
from app.core.operations import to_grayscale

# 32 bins of 8 gray levels each: enough to see the shape of the histogram
# (dark / bright / clipped) while staying readable as a small chart.
HISTOGRAM_BINS = 32

# Pixels this close to black or white are treated as clipped (detail lost).
# 5 levels (~2% of the 0-255 range) tolerates sensor noise around 0 and 255.
DARK_LIMIT = 5
BRIGHT_LIMIT = 250


@dataclass(frozen=True)
class BrightnessStats:
    mean: float  # overall brightness
    std: float  # global contrast: spread of gray levels around the mean
    min: int
    max: int
    dark_fraction: float  # share of pixels <= DARK_LIMIT (underexposed)
    bright_fraction: float  # share of pixels >= BRIGHT_LIMIT (overexposed)
    histogram: list[int]  # pixel counts in HISTOGRAM_BINS equal bins over 0-255


def brightness_stats(image: np.ndarray) -> BrightnessStats:
    if image.dtype != np.uint8:
        raise UnsupportedImageError(
            f"Brightness statistics need an 8-bit image, got {image.dtype}."
        )
    gray = to_grayscale(image)
    histogram, _ = np.histogram(gray, bins=HISTOGRAM_BINS, range=(0, 256))
    return BrightnessStats(
        mean=float(gray.mean()),
        std=float(gray.std()),
        min=int(gray.min()),
        max=int(gray.max()),
        dark_fraction=float(np.mean(gray <= DARK_LIMIT)),
        bright_fraction=float(np.mean(gray >= BRIGHT_LIMIT)),
        histogram=histogram.tolist(),
    )
