from pathlib import Path

import cv2
import numpy as np
from fastapi.testclient import TestClient


def test_load_sample_by_path_returns_info(client: TestClient, sample_image_path: Path) -> None:
    response = client.post("/api/image/load", json={"path": str(sample_image_path)})

    assert response.status_code == 200
    assert response.json() == {"width": 640, "height": 420, "channels": 3, "dtype": "uint8"}


def test_loaded_image_is_served_as_png(client: TestClient, sample_image_path: Path) -> None:
    client.post("/api/image/load", json={"path": str(sample_image_path)})

    response = client.get("/api/workspace/input")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    decoded = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_UNCHANGED)
    assert decoded.shape == (420, 640, 3)


def test_load_wrong_path_returns_404_with_message(client: TestClient) -> None:
    response = client.post("/api/image/load", json={"path": "no/such/file.png"})

    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"]


def test_upload_png_returns_info(client: TestClient) -> None:
    image = np.zeros((30, 40, 3), dtype=np.uint8)
    png = cv2.imencode(".png", image)[1].tobytes()

    response = client.post("/api/image/upload", files={"file": ("x.png", png, "image/png")})

    assert response.status_code == 200
    assert response.json()["width"] == 40


def test_upload_corrupted_file_returns_400(client: TestClient) -> None:
    response = client.post("/api/image/upload", files={"file": ("x.png", b"garbage", "image/png")})

    assert response.status_code == 400
    assert "corrupted" in response.json()["detail"]


def test_input_before_loading_returns_404(client: TestClient) -> None:
    response = client.get("/api/workspace/input")

    assert response.status_code == 404


def test_samples_lists_starter_files(client: TestClient) -> None:
    response = client.get("/api/samples")

    assert response.status_code == 200
    names = [Path(path).name for path in response.json()]
    assert "obraz_testowy.png" in names
    assert "ruch_testowy.avi" in names
