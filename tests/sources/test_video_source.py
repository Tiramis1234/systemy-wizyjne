from pathlib import Path

import pytest

from app.core.errors import FrameOutOfRangeError, SourceUnavailableError
from app.sources.video_source import VideoSource
from tests.conftest import BRIGHTNESS_STEP, SYNTHETIC_FRAME_COUNT

# MJPEG is lossy; a flat gray frame comes back within a few gray levels.
JPEG_TOLERANCE = 3


def test_open_reports_frame_count_fps_and_size(synthetic_video_path: Path) -> None:
    with VideoSource(synthetic_video_path) as video:
        assert video.frame_count == SYNTHETIC_FRAME_COUNT
        assert video.fps == pytest.approx(10.0)
        assert (video.width, video.height) == (32, 24)


def test_read_frame_by_index_returns_that_frame(synthetic_video_path: Path) -> None:
    with VideoSource(synthetic_video_path) as video:
        frame = video.read_frame(7)

    assert abs(frame.mean() - 7 * BRIGHTNESS_STEP) <= JPEG_TOLERANCE


def test_sequential_and_random_reads_agree(synthetic_video_path: Path) -> None:
    with VideoSource(synthetic_video_path) as video:
        sequential = [video.read_frame(index).mean() for index in range(SYNTHETIC_FRAME_COUNT)]
        backwards = video.read_frame(2).mean()  # jump back, like "replay" or the slider

    assert backwards == pytest.approx(sequential[2])
    for index, mean in enumerate(sequential):
        assert abs(mean - index * BRIGHTNESS_STEP) <= JPEG_TOLERANCE


@pytest.mark.parametrize("index", [-1, SYNTHETIC_FRAME_COUNT])
def test_read_frame_out_of_range_raises(synthetic_video_path: Path, index: int) -> None:
    with VideoSource(synthetic_video_path) as video, pytest.raises(FrameOutOfRangeError):
        video.read_frame(index)


def test_missing_file_raises_unavailable(tmp_path: Path) -> None:
    with pytest.raises(SourceUnavailableError, match="does not exist"):
        VideoSource(tmp_path / "missing.avi")


def test_non_video_file_raises_unavailable(tmp_path: Path) -> None:
    path = tmp_path / "fake.avi"
    path.write_text("not a video")

    with pytest.raises(SourceUnavailableError):
        VideoSource(path)


def test_context_manager_releases_capture(synthetic_video_path: Path) -> None:
    with VideoSource(synthetic_video_path) as video:
        assert video.is_open

    assert not video.is_open


def test_sample_video_matches_description(sample_video_path: Path) -> None:
    with VideoSource(sample_video_path) as video:
        assert video.frame_count == 195
        assert video.fps == pytest.approx(15.0)
        assert (video.width, video.height) == (640, 360)
        assert video.read_frame(194).shape == (360, 640, 3)
