"""Reading, decoding and encoding images.

Images are kept exactly as OpenCV gives them: BGR channel order, original bit depth
and original number of channels (IMREAD_UNCHANGED), so the info panel shows the
real properties of the file.
"""

from pathlib import Path

import cv2
import numpy as np

from app.core.errors import ImageDecodeError, ImageEncodeError, ImageLoadError, ImageSaveError

# Formats required by the P01 brief. ".jpeg" is the same format as ".jpg".
SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg")

# JPEG quality 0-100. 95 is OpenCV's own default: visually lossless for
# inspection images while still much smaller than PNG.
JPEG_QUALITY = 95


def load_image(path: Path) -> np.ndarray:
    """Load a PNG/JPG file from disk."""
    if not path.is_file():
        raise ImageLoadError(f"File does not exist: {path}")
    check_extension(path.name)
    # Reading bytes ourselves instead of cv2.imread: imread silently returns None
    # for every problem, while here a missing file and a corrupted file are
    # reported as different errors.
    return decode_image(path.read_bytes())


def check_extension(file_name: str) -> None:
    """Reject files that are not PNG/JPG, judged by the file name."""
    suffix = Path(file_name).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ImageLoadError(
            f"Unsupported file type '{suffix}'. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
        )


def decode_image(data: bytes) -> np.ndarray:
    """Decode an encoded image (PNG/JPG bytes) into a numpy array."""
    if not data:
        raise ImageDecodeError("The file is empty.")
    buffer = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ImageDecodeError("The file is not a valid image or is corrupted.")
    return image


def encode_image(image: np.ndarray, extension: str = ".png") -> bytes:
    """Encode an image to PNG/JPG bytes.

    cv2.imencode expects BGR input and writes a standard RGB file, so this is the
    point where OpenCV's BGR order is converted for the browser.
    """
    params = [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY] if extension in (".jpg", ".jpeg") else []
    success, buffer = cv2.imencode(extension, image, params)
    if not success:
        raise ImageEncodeError(f"Could not encode the image as {extension}.")
    return buffer.tobytes()


def save_image(image: np.ndarray, path: Path) -> None:
    """Save an image as PNG/JPG; the format is chosen by the file extension."""
    extension = path.suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ImageSaveError(
            f"Unsupported file type '{extension}'. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
        )
    if not path.parent.is_dir():
        raise ImageSaveError(f"Directory does not exist: {path.parent}")
    try:
        data = encode_image(image, extension)
        # Writing bytes ourselves instead of cv2.imwrite: imwrite only returns
        # False, while OSError says why (permissions, target is a directory, ...).
        path.write_bytes(data)
    except (ImageEncodeError, OSError) as error:
        raise ImageSaveError(f"Could not save {path}: {error}") from error
