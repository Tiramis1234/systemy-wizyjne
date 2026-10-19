"""Video file source: open, read any frame by index, release."""

from pathlib import Path

import cv2
import numpy as np

from app.core.errors import FrameOutOfRangeError, SourceReadError, SourceUnavailableError
from app.sources.capture_source import CaptureSource


class VideoSource(CaptureSource):
    def __init__(self, path: Path) -> None:
        if not path.is_file():
            raise SourceUnavailableError(f"Video file does not exist: {path}")
        capture = cv2.VideoCapture(str(path))
        if not capture.isOpened():
            raise SourceUnavailableError(f"Cannot open as video: {path}")
        super().__init__(capture)

        self.frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if self.frame_count <= 0:
            self.release()
            raise SourceUnavailableError(f"Not a video or the video has no frames: {path}")
        self.fps = capture.get(cv2.CAP_PROP_FPS)
        self.width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Index of the frame the next capture.read() will return. During normal
        # playback frames are requested in order, so seeking can be skipped.
        self._next_index = 0

    def read_frame(self, index: int) -> np.ndarray:
        if not 0 <= index < self.frame_count:
            raise FrameOutOfRangeError(
                f"Frame {index} is out of range (video has frames 0-{self.frame_count - 1})."
            )
        with self._lock:
            if index != self._next_index:
                self._capture.set(cv2.CAP_PROP_POS_FRAMES, index)
            success, frame = self._capture.read()
            if not success:
                raise SourceReadError(f"Could not read frame {index}.")
            self._next_index = index + 1
        return frame
