"""Comparing two inputs (e.g. the same scene under two lightings) by brightness."""

from typing import Literal

from fastapi import APIRouter, Response

from app.api.dependencies import WorkspaceDep
from app.api.routes_workspace import PREVIEW_FORMAT, png_response
from app.api.schemas import Comparison
from app.core.image_io import encode_image
from app.core.image_stats import BrightnessStats, brightness_stats

router = APIRouter(prefix="/api/compare", tags=["compare"])

Slot = Literal["A", "B"]


@router.post("/{slot}")
def store_input(slot: Slot, workspace: WorkspaceDep) -> BrightnessStats:
    """Remember the current input as A or B and return its statistics."""
    return brightness_stats(workspace.store_snapshot(slot))


@router.get("/{slot}/image")
def get_snapshot(slot: Slot, workspace: WorkspaceDep) -> Response:
    return png_response(encode_image(workspace.require_snapshot(slot), PREVIEW_FORMAT))


@router.get("")
def compare(workspace: WorkspaceDep) -> Comparison:
    stats = {name: brightness_stats(image) for name, image in workspace.snapshots.items()}
    a, b = stats.get("A"), stats.get("B")
    difference = b.mean - a.mean if a and b else None
    return Comparison(A=a, B=b, mean_difference=difference)
