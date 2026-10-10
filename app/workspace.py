"""In-memory state of the application: the current input image.

The application has a single user, so one Workspace per running app is enough.
It holds no web or OpenCV logic, only the images the user is working on.
"""

import numpy as np


class Workspace:
    def __init__(self) -> None:
        self.input: np.ndarray | None = None

    def set_input(self, image: np.ndarray) -> None:
        # A copy, so later changes to the caller's array cannot affect the workspace.
        self.input = image.copy()

    def require_input(self) -> np.ndarray:
        if self.input is None:
            raise LookupError("No input image. Load an image, a video frame or a camera frame.")
        return self.input
