"""Request bodies of the HTTP API."""

from pydantic import BaseModel

from app.core.operations import Operation


class PathRequest(BaseModel):
    path: str


class ApplyRequest(BaseModel):
    operation: Operation
