"""Errors raised by the processing and source layers.

Each error carries a human-readable message that the interface shows to the user.
The web layer maps these classes to HTTP status codes (see app/api/errors.py).
"""


class VisionError(Exception):
    """Base class for all expected, user-facing errors of the application."""


class ImageLoadError(VisionError):
    """The file cannot be read: wrong path or unsupported format."""


class ImageDecodeError(VisionError):
    """The data was read but is not a valid image (e.g. a corrupted file)."""


class ImageEncodeError(VisionError):
    """The image cannot be encoded to the requested format."""
