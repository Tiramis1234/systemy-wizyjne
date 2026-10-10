"""Keeps track of the one active video/camera source.

Switching to another source (or loading a still image) always releases the
previous one, so the camera is never left open and sources can be changed
without restarting the application.
"""

from typing import Protocol


class Source(Protocol):
    def release(self) -> None: ...


class SourceManager:
    def __init__(self) -> None:
        self.active: Source | None = None

    def switch(self, source: Source) -> None:
        self.close()
        self.active = source

    def close(self) -> None:
        if self.active is not None:
            self.active.release()
            self.active = None

    def require[S: Source](self, kind: type[S]) -> S:
        """Return the active source if it is of the given kind, e.g. VideoSource."""
        if not isinstance(self.active, kind):
            raise LookupError(f"No {kind.__name__} is open.")
        return self.active
