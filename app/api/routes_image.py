"""Loading still images (by server path or by upload)."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from app.api.dependencies import get_workspace
from app.api.schemas import PathRequest
from app.core.image_info import ImageInfo, describe_image
from app.core.image_io import check_extension, decode_image, load_image
from app.workspace import Workspace

router = APIRouter(prefix="/api/image", tags=["image"])

WorkspaceDep = Annotated[Workspace, Depends(get_workspace)]


@router.post("/load")
def load_from_path(request: PathRequest, workspace: WorkspaceDep) -> ImageInfo:
    image = load_image(Path(request.path))
    workspace.set_input(image)
    return describe_image(image)


@router.post("/upload")
def load_from_upload(file: UploadFile, workspace: WorkspaceDep) -> ImageInfo:
    check_extension(file.filename or "")
    image = decode_image(file.file.read())
    workspace.set_input(image)
    return describe_image(image)
