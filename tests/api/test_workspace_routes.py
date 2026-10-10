from pathlib import Path

from fastapi.testclient import TestClient


def load_sample(client: TestClient, path: Path) -> None:
    client.post("/api/image/load", json={"path": str(path)})


def test_result_equals_input_after_loading(client: TestClient, sample_image_path: Path) -> None:
    load_sample(client, sample_image_path)

    response = client.get("/api/workspace/result/info")

    assert response.json()["channels"] == 3


def test_apply_grayscale_returns_single_channel_info(
    client: TestClient, sample_image_path: Path
) -> None:
    load_sample(client, sample_image_path)

    response = client.post("/api/workspace/apply", json={"operation": "grayscale"})

    assert response.status_code == 200
    assert response.json()["channels"] == 1
    assert client.get("/api/workspace/result").headers["content-type"] == "image/png"


def test_reset_restores_three_channels(client: TestClient, sample_image_path: Path) -> None:
    load_sample(client, sample_image_path)
    client.post("/api/workspace/apply", json={"operation": "grayscale"})

    response = client.post("/api/workspace/reset")

    assert response.json()["channels"] == 3


def test_apply_unknown_operation_returns_422(client: TestClient, sample_image_path: Path) -> None:
    load_sample(client, sample_image_path)

    response = client.post("/api/workspace/apply", json={"operation": "magic"})

    assert response.status_code == 422


def test_apply_without_input_returns_404(client: TestClient) -> None:
    response = client.post("/api/workspace/apply", json={"operation": "grayscale"})

    assert response.status_code == 404


def test_save_result_writes_file(
    client: TestClient, sample_image_path: Path, tmp_path: Path
) -> None:
    load_sample(client, sample_image_path)
    target = tmp_path / "result.jpg"

    response = client.post("/api/workspace/save", json={"path": str(target)})

    assert response.status_code == 200
    assert target.is_file()


def test_save_to_missing_directory_returns_400(
    client: TestClient, sample_image_path: Path, tmp_path: Path
) -> None:
    load_sample(client, sample_image_path)

    response = client.post(
        "/api/workspace/save", json={"path": str(tmp_path / "nope" / "result.png")}
    )

    assert response.status_code == 400
    assert "Directory does not exist" in response.json()["detail"]


def test_download_result_as_jpg(client: TestClient, sample_image_path: Path) -> None:
    load_sample(client, sample_image_path)

    response = client.get("/api/workspace/result/download", params={"format": "jpg"})

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    assert "attachment" in response.headers["content-disposition"]
