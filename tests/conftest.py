"""Shared test fixtures."""

from pathlib import Path

import pytest

SAMPLES_DIR = Path(__file__).parent.parent / "data" / "samples"


@pytest.fixture
def sample_image_path() -> Path:
    """Course starter image: 640x420 RGB PNG with a red square in the top-left corner."""
    return SAMPLES_DIR / "obraz_testowy.png"
