import numpy as np
import pytest

from app.core.errors import SourceReadError, SourceUnavailableError
from app.sources import camera_source
from app.sources.camera_source import CameraSource

# No machine has 100 cameras, so this index reliably simulates "no camera".
MISSING_CAMERA_INDEX = 99


class FakeCapture:
    """Replaces cv2.VideoCapture so camera logic is tested without hardware."""

    instances: list["FakeCapture"] = []

    def __init__(self, index: int, opened: bool = True, frames_ok: bool = True) -> None:
        self.index = index
        self.opened = opened
        self.frames_ok = frames_ok
        self.properties: dict[int, float] = {}
        FakeCapture.instances.append(self)

    def isOpened(self) -> bool:  # noqa: N802 - mirrors the OpenCV API
        return self.opened

    def read(self) -> tuple[bool, np.ndarray | None]:
        if not self.frames_ok:
            return False, None
        return True, np.full((48, 64, 3), 77, dtype=np.uint8)

    def set(self, prop: int, value: float) -> bool:
        self.properties[prop] = value
        return True

    def get(self, prop: int) -> float:
        return {3: 64.0, 4: 48.0}.get(prop, 0.0)  # 3/4 = CAP_PROP_FRAME_WIDTH/HEIGHT

    def release(self) -> None:
        self.opened = False


@pytest.fixture
def fake_capture(monkeypatch: pytest.MonkeyPatch) -> type[FakeCapture]:
    FakeCapture.instances = []
    monkeypatch.setattr(camera_source, "VideoCapture", FakeCapture)
    return FakeCapture


def test_missing_camera_raises_unavailable() -> None:
    with pytest.raises(SourceUnavailableError, match="Camera 99"):
        CameraSource(MISSING_CAMERA_INDEX)


def test_read_returns_frame(fake_capture: type[FakeCapture]) -> None:
    with CameraSource(0) as camera:
        frame = camera.read()

    assert frame.shape == (48, 64, 3)


def test_reports_frame_size(fake_capture: type[FakeCapture]) -> None:
    with CameraSource(0) as camera:
        assert (camera.width, camera.height) == (64, 48)


def test_failed_read_raises_read_error(
    fake_capture: type[FakeCapture], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        camera_source, "VideoCapture", lambda index: FakeCapture(index, frames_ok=False)
    )

    with CameraSource(0) as camera, pytest.raises(SourceReadError):
        camera.read()


def test_context_manager_releases_device(fake_capture: type[FakeCapture]) -> None:
    with CameraSource(0):
        pass

    assert not fake_capture.instances[0].opened
