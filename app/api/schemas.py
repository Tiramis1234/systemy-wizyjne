"""Request bodies of the HTTP API."""

from pydantic import BaseModel

from app import settings
from app.core.image_stats import BrightnessStats
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


class CameraRequest(BaseModel):
    index: int = settings.CAMERA_INDEX


class CameraInfo(BaseModel):
    width: int
    height: int


class Comparison(BaseModel):
    A: BrightnessStats | None
    B: BrightnessStats | None
    mean_difference: float | None  # B.mean - A.mean; positive = B is brighter
