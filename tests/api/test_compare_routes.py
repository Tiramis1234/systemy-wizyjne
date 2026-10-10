from pathlib import Path

from fastapi.testclient import TestClient


def test_store_input_as_slot_returns_stats(client: TestClient, sample_image_path: Path) -> None:
    client.post("/api/image/load", json={"path": str(sample_image_path)})

    response = client.post("/api/compare/A")

    assert response.status_code == 200
    assert 0 < response.json()["mean"] < 255
    assert client.get("/api/compare/A/image").headers["content-type"] == "image/png"


def test_comparison_reports_difference_of_means(
    client: TestClient, sample_image_path: Path
) -> None:
    client.post("/api/image/load", json={"path": str(sample_image_path)})
    client.post("/api/compare/A")
    client.post("/api/compare/B")

    response = client.get("/api/compare")

    body = response.json()
    assert body["A"]["mean"] == body["B"]["mean"]
    assert body["mean_difference"] == 0


def test_comparison_with_one_slot_has_no_difference(
    client: TestClient, sample_image_path: Path
) -> None:
    client.post("/api/image/load", json={"path": str(sample_image_path)})
    client.post("/api/compare/A")

    body = client.get("/api/compare").json()

    assert body["B"] is None
    assert body["mean_difference"] is None


def test_unknown_slot_returns_422(client: TestClient, sample_image_path: Path) -> None:
    client.post("/api/image/load", json={"path": str(sample_image_path)})

    assert client.post("/api/compare/C").status_code == 422


def test_store_without_input_returns_404(client: TestClient) -> None:
    assert client.post("/api/compare/A").status_code == 404
