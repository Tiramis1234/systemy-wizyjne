from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.sources import camera_source
from tests.sources.test_camera_source import MISSING_CAMERA_INDEX, FakeCapture


@pytest.fixture
def fake_camera(monkeypatch: pytest.MonkeyPatch) -> type[FakeCapture]:
    FakeCapture.instances = []
    monkeypatch.setattr(camera_source, "VideoCapture", FakeCapture)
    return FakeCapture


def test_open_missing_camera_returns_404_with_message(client: TestClient) -> None:
    response = client.post("/api/camera/open", json={"index": MISSING_CAMERA_INDEX})

    assert response.status_code == 404
    assert "Camera 99" in response.json()["detail"]


def test_open_and_read_frame(client: TestClient, fake_camera: type[FakeCapture]) -> None:
    opened = client.post("/api/camera/open", json={"index": 0})
    frame = client.get("/api/camera/frame")

    assert opened.json() == {"width": 64, "height": 48}
    assert frame.status_code == 200
    assert frame.headers["content-type"] == "image/png"


def test_capture_sets_input(client: TestClient, fake_camera: type[FakeCapture]) -> None:
    client.post("/api/camera/open", json={"index": 0})

    response = client.post("/api/camera/capture")

    assert response.json() == {"width": 64, "height": 48, "channels": 3, "dtype": "uint8"}
    assert client.get("/api/workspace/input").status_code == 200


def test_close_releases_camera(client: TestClient, fake_camera: type[FakeCapture]) -> None:
    client.post("/api/camera/open", json={"index": 0})

    client.post("/api/camera/close")

    assert not fake_camera.instances[0].opened
    assert client.get("/api/camera/frame").status_code == 404


def test_opening_video_releases_camera(
    client: TestClient, fake_camera: type[FakeCapture], sample_video_path: Path
) -> None:
    client.post("/api/camera/open", json={"index": 0})

    client.post("/api/video/open", json={"path": str(sample_video_path)})

    assert not fake_camera.instances[0].opened
