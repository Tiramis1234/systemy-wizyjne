"""Video file source: open, read any frame by index, release."""

from pathlib import Path
from types import TracebackType
from typing import Self

import cv2
import numpy as np

from app.core.errors import FrameOutOfRangeError, SourceReadError, SourceUnavailableError


class VideoSource:
    def __init__(self, path: Path) -> None:
        if not path.is_file():
            raise SourceUnavailableError(f"Video file does not exist: {path}")
        self._capture = cv2.VideoCapture(str(path))
        if not self._capture.isOpened():
            raise SourceUnavailableError(f"Cannot open as video: {path}")

        self.frame_count = int(self._capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if self.frame_count <= 0:
            self._capture.release()
            raise SourceUnavailableError(f"Not a video or the video has no frames: {path}")
        self.fps = self._capture.get(cv2.CAP_PROP_FPS)
        self.width = int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Index of the frame the next capture.read() will return. During normal
        # playback frames are requested in order, so seeking can be skipped.
        self._next_index = 0

    @property
    def is_open(self) -> bool:
        return self._capture.isOpened()

    def read_frame(self, index: int) -> np.ndarray:
        if not 0 <= index < self.frame_count:
            raise FrameOutOfRangeError(
                f"Frame {index} is out of range (video has frames 0-{self.frame_count - 1})."
            )
        if index != self._next_index:
            self._capture.set(cv2.CAP_PROP_POS_FRAMES, index)
        success, frame = self._capture.read()
        if not success:
            raise SourceReadError(f"Could not read frame {index}.")
        self._next_index = index + 1
        return frame

    def release(self) -> None:
        self._capture.release()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.release()
