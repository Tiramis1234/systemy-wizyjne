from pathlib import Path

import cv2
import numpy as np
from fastapi.testclient import TestClient


def open_video(client: TestClient, path: Path):
    return client.post("/api/video/open", json={"path": str(path)})


def test_open_sample_video_returns_info(client: TestClient, sample_video_path: Path) -> None:
    response = open_video(client, sample_video_path)

    assert response.status_code == 200
    assert response.json() == {"frame_count": 195, "fps": 15.0, "width": 640, "height": 360}


def test_frame_is_served_as_png(client: TestClient, sample_video_path: Path) -> None:
    open_video(client, sample_video_path)

    response = client.get("/api/video/frame", params={"index": 100})

    assert response.status_code == 200
    frame = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_UNCHANGED)
    assert frame.shape == (360, 640, 3)


def test_frame_out_of_range_returns_400(client: TestClient, sample_video_path: Path) -> None:
    open_video(client, sample_video_path)

    response = client.get("/api/video/frame", params={"index": 195})

    assert response.status_code == 400
    assert "out of range" in response.json()["detail"]


def test_capture_frame_sets_workspace_input(client: TestClient, sample_video_path: Path) -> None:
    open_video(client, sample_video_path)

    response = client.post("/api/video/capture", json={"index": 50})

    assert response.json() == {"width": 640, "height": 360, "channels": 3, "dtype": "uint8"}
    assert client.get("/api/workspace/input").status_code == 200


def test_open_missing_video_returns_404(client: TestClient) -> None:
    response = client.post("/api/video/open", json={"path": "no/such/video.avi"})

    assert response.status_code == 404


def test_frame_without_open_video_returns_404(client: TestClient) -> None:
    response = client.get("/api/video/frame", params={"index": 0})

    assert response.status_code == 404


def test_loading_an_image_closes_the_video(
    client: TestClient, sample_video_path: Path, sample_image_path: Path
) -> None:
    open_video(client, sample_video_path)

    client.post("/api/image/load", json={"path": str(sample_image_path)})

    assert client.get("/api/video/frame", params={"index": 0}).status_code == 404
