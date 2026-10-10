"""Video files: open, serve frames for playback, capture a frame as input.

Play/pause and the frame slider live in the frontend: it asks for frame
after frame at the video's fps. The backend only reads the requested frame.
"""

from pathlib import Path

from fastapi import APIRouter, Response

from app.api.dependencies import SourcesDep, WorkspaceDep
from app.api.routes_workspace import PREVIEW_FORMAT, png_response
from app.api.schemas import FrameRequest, PathRequest, VideoInfo
from app.core.image_info import ImageInfo, describe_image
from app.core.image_io import encode_image
from app.sources.video_source import VideoSource

router = APIRouter(prefix="/api/video", tags=["video"])


@router.post("/open")
def open_video(request: PathRequest, sources: SourcesDep) -> VideoInfo:
    video = VideoSource(Path(request.path))
    sources.switch(video)
    return VideoInfo(
        frame_count=video.frame_count, fps=video.fps, width=video.width, height=video.height
    )


@router.get("/frame")
def get_frame(index: int, sources: SourcesDep) -> Response:
    frame = sources.require(VideoSource).read_frame(index)
    return png_response(encode_image(frame, PREVIEW_FORMAT))


@router.post("/capture")
def capture_frame(request: FrameRequest, sources: SourcesDep, workspace: WorkspaceDep) -> ImageInfo:
    """Use the chosen frame as the input image (and so as the base of the result)."""
    frame = sources.require(VideoSource).read_frame(request.index)
    workspace.set_input(frame)
    return describe_image(frame)
