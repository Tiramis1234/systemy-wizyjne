"""Common part of video and camera sources: an OpenCV capture that must be released."""

import threading
from types import TracebackType
from typing import Self

import cv2


class CaptureSource:
    def __init__(self, capture: cv2.VideoCapture) -> None:
        self._capture = capture
        # The web server handles requests in several threads; the lock makes sure
        # two requests never read from (or seek) the same capture at once.
        self._lock = threading.Lock()

    @property
    def is_open(self) -> bool:
        return self._capture.isOpened()

    def release(self) -> None:
        with self._lock:
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
