"""Request bodies of the HTTP API."""

from pydantic import BaseModel

from app.core.operations import Operation


class PathRequest(BaseModel):
    path: str


class ApplyRequest(BaseModel):
    operation: Operation


class SavedResponse(BaseModel):
    path: str


class FrameRequest(BaseModel):
    index: int


class VideoInfo(BaseModel):
    frame_count: int
    fps: float
    width: int
    height: int
