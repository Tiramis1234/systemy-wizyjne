"""Shared test fixtures."""

from pathlib import Path

import cv2
import numpy as np
import pytest

SAMPLES_DIR = Path(__file__).parent.parent / "data" / "samples"


@pytest.fixture
def sample_image_path() -> Path:
    """Course starter image: 640x420 RGB PNG with a red square in the top-left corner."""
    return SAMPLES_DIR / "obraz_testowy.png"


@pytest.fixture
def sample_video_path() -> Path:
    """Course starter video: MJPEG AVI, 640x360, 15 fps, 195 frames."""
    return SAMPLES_DIR / "ruch_testowy.avi"


# Frame i of the synthetic video is filled with gray level i * BRIGHTNESS_STEP,
# so every frame can be recognized after (lossy) MJPEG compression.
SYNTHETIC_FRAME_COUNT = 10
BRIGHTNESS_STEP = 20


@pytest.fixture
def synthetic_video_path(tmp_path: Path) -> Path:
    path = tmp_path / "synthetic.avi"
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"MJPG"), 10.0, (32, 24))
    for index in range(SYNTHETIC_FRAME_COUNT):
        writer.write(np.full((24, 32, 3), index * BRIGHTNESS_STEP, dtype=np.uint8))
    writer.release()
    return path
