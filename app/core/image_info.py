"""Basic properties of an image shown in the info panel."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ImageInfo:
    width: int
    height: int
    channels: int
    dtype: str


def describe_image(image: np.ndarray) -> ImageInfo:
    height, width = image.shape[:2]
    # A grayscale image is a 2D array: (height, width) with no channel axis.
    channels = 1 if image.ndim == 2 else image.shape[2]
    return ImageInfo(width=width, height=height, channels=channels, dtype=str(image.dtype))
