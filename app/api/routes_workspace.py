"""Input and result images: serving, applying an operation, reset; sample files."""

from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Response

from app import settings
from app.api.dependencies import WorkspaceDep
from app.api.schemas import ApplyRequest, PathRequest, SavedResponse
from app.core.image_info import ImageInfo, describe_image
from app.core.image_io import encode_image, save_image

router = APIRouter(prefix="/api", tags=["workspace"])

# PNG is lossless, so the preview shows exactly the pixels being processed.
PREVIEW_FORMAT = ".png"


def png_response(data: bytes) -> Response:
    # no-store: the same URL returns a different image after every load.
    return Response(content=data, media_type="image/png", headers={"Cache-Control": "no-store"})


@router.get("/workspace/input")
def get_input(workspace: WorkspaceDep) -> Response:
    return png_response(encode_image(workspace.require_input(), PREVIEW_FORMAT))


@router.get("/workspace/input/info")
def get_input_info(workspace: WorkspaceDep) -> ImageInfo:
    return describe_image(workspace.require_input())


@router.get("/workspace/result")
def get_result(workspace: WorkspaceDep) -> Response:
    return png_response(encode_image(workspace.require_result(), PREVIEW_FORMAT))


@router.get("/workspace/result/info")
def get_result_info(workspace: WorkspaceDep) -> ImageInfo:
    return describe_image(workspace.require_result())


@router.post("/workspace/apply")
def apply_operation(request: ApplyRequest, workspace: WorkspaceDep) -> ImageInfo:
    workspace.apply(request.operation)
    return describe_image(workspace.require_result())


@router.post("/workspace/reset")
def reset_result(workspace: WorkspaceDep) -> ImageInfo:
    workspace.reset()
    return describe_image(workspace.require_result())


@router.post("/workspace/save")
def save_result(request: PathRequest, workspace: WorkspaceDep) -> SavedResponse:
    """Save the result on the server; PNG or JPG is chosen by the extension."""
    path = Path(request.path)
    save_image(workspace.require_result(), path)
    return SavedResponse(path=str(path))


@router.get("/workspace/result/download")
def download_result(workspace: WorkspaceDep, format: Literal["png", "jpg"] = "png") -> Response:
    """Send the result to the browser as a file to save."""
    data = encode_image(workspace.require_result(), f".{format}")
    media_type = "image/png" if format == "png" else "image/jpeg"
    return Response(
        content=data,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="result.{format}"'},
    )


@router.get("/samples")
def list_samples() -> list[str]:
    """Sample files the user can open by path (images and videos)."""
    return sorted(str(path) for path in settings.SAMPLES_DIR.iterdir() if path.is_file())
