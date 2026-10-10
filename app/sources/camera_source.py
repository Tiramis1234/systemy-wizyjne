"""Camera source: open a device by index, read the current frame, release."""

import cv2
import numpy as np

# Imported by name so tests can replace only the camera's capture with a fake.
from cv2 import VideoCapture

from app.core.errors import SourceReadError, SourceUnavailableError
from app.sources.capture_source import CaptureSource

# The camera driver keeps a queue of frames. With a queue of 1 every read
# returns (almost) the newest frame instead of one captured a while ago,
# because the preview reads frames slower than the camera produces them.
BUFFER_SIZE = 1


class CameraSource(CaptureSource):
    def __init__(self, index: int) -> None:
        capture = VideoCapture(index)
        if not capture.isOpened():
            capture.release()
            raise SourceUnavailableError(
                f"Camera {index} not found or busy. Check that it is connected "
                "and not used by another program."
            )
        super().__init__(capture)
        capture.set(cv2.CAP_PROP_BUFFERSIZE, BUFFER_SIZE)
        self.index = index
        self.width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def read(self) -> np.ndarray:
        with self._lock:
            success, frame = self._capture.read()
        if not success:
            raise SourceReadError(f"Camera {self.index} did not return a frame (disconnected?).")
        return frame
