"""Image operations available in P01.

P01 does not require any processing yet; grayscale is a single demonstration
operation that makes the input/result panels, reset and saving meaningful.
Later stages add their methods here.
"""

from enum import StrEnum

import cv2
import numpy as np


class Operation(StrEnum):
    NONE = "none"
    GRAYSCALE = "grayscale"


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert to one channel with OpenCV's luminance weights.

    Y = 0.299 R + 0.587 G + 0.114 B (ITU-R BT.601), the standard weighting that
    matches how bright the human eye perceives each color.
    """
    if image.ndim == 2:
        return image.copy()
    if image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_operation(image: np.ndarray, operation: Operation) -> np.ndarray:
    """Return a new image; the input is never modified."""
    if operation == Operation.GRAYSCALE:
        return to_grayscale(image)
    return image.copy()
