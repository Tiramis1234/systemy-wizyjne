"""Camera: open, serve the live frame for the preview, capture, close."""

from fastapi import APIRouter, Response

from app.api.dependencies import SourcesDep, WorkspaceDep
from app.api.routes_workspace import PREVIEW_FORMAT, png_response
from app.api.schemas import CameraInfo, CameraRequest
from app.core.image_info import ImageInfo, describe_image
from app.core.image_io import encode_image
from app.sources.camera_source import CameraSource

router = APIRouter(prefix="/api/camera", tags=["camera"])


@router.post("/open")
def open_camera(request: CameraRequest, sources: SourcesDep) -> CameraInfo:
    # Release the previous source first: if it is the same camera, it must be
    # free before it can be opened again.
    sources.close()
    camera = CameraSource(request.index)
    sources.switch(camera)
    return CameraInfo(width=camera.width, height=camera.height)


@router.get("/frame")
def get_frame(sources: SourcesDep) -> Response:
    frame = sources.require(CameraSource).read()
    return png_response(encode_image(frame, PREVIEW_FORMAT))


@router.post("/capture")
def capture_frame(sources: SourcesDep, workspace: WorkspaceDep) -> ImageInfo:
    """Use the current camera frame as the input image."""
    frame = sources.require(CameraSource).read()
    workspace.set_input(frame)
    return describe_image(frame)


@router.post("/close")
def close_camera(sources: SourcesDep) -> dict[str, str]:
    sources.close()
    return {"status": "closed"}
