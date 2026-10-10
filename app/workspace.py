"""In-memory state of the application: the input image and the result image.

The application has a single user, so one Workspace per running app is enough.
It holds no web logic, only the images the user is working on.
"""

import numpy as np

from app.core.operations import Operation, apply_operation


class Workspace:
    def __init__(self) -> None:
        self.input: np.ndarray | None = None
        self.result: np.ndarray | None = None

    def set_input(self, image: np.ndarray) -> None:
        # Copies, so later changes to the caller's array cannot affect the workspace.
        self.input = image.copy()
        self.result = image.copy()

    def require_input(self) -> np.ndarray:
        if self.input is None:
            raise LookupError("No input image. Load an image, a video frame or a camera frame.")
        return self.input

    def require_result(self) -> np.ndarray:
        if self.result is None:
            raise LookupError("No result image. Load an input image first.")
        return self.result

    def apply(self, operation: Operation) -> None:
        # Always computed from the input, so operations do not stack up.
        self.result = apply_operation(self.require_input(), operation)

    def reset(self) -> None:
        self.result = self.require_input().copy()
