"""Loading still images (by server path or by upload)."""

from pathlib import Path

from fastapi import APIRouter, UploadFile

from app.api.dependencies import SourcesDep, WorkspaceDep
from app.api.schemas import PathRequest
from app.core.image_info import ImageInfo, describe_image
from app.core.image_io import check_extension, decode_image, load_image

router = APIRouter(prefix="/api/image", tags=["image"])


@router.post("/load")
def load_from_path(request: PathRequest, workspace: WorkspaceDep, sources: SourcesDep) -> ImageInfo:
    image = load_image(Path(request.path))
    sources.close()  # a still image replaces any open video or camera
    workspace.set_input(image)
    return describe_image(image)


@router.post("/upload")
def load_from_upload(file: UploadFile, workspace: WorkspaceDep, sources: SourcesDep) -> ImageInfo:
    check_extension(file.filename or "")
    image = decode_image(file.file.read())
    sources.close()  # a still image replaces any open video or camera
    workspace.set_input(image)
    return describe_image(image)
