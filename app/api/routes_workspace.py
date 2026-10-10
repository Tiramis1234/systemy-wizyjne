"""Input and result images: serving, applying an operation, reset; sample files."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app import settings
from app.api.dependencies import get_workspace
from app.api.schemas import ApplyRequest
from app.core.image_info import ImageInfo, describe_image
from app.core.image_io import encode_image
from app.workspace import Workspace

router = APIRouter(prefix="/api", tags=["workspace"])

WorkspaceDep = Annotated[Workspace, Depends(get_workspace)]

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


@router.get("/samples")
def list_samples() -> list[str]:
    """Sample files the user can open by path (images and videos)."""
    return sorted(str(path) for path in settings.SAMPLES_DIR.iterdir() if path.is_file())
