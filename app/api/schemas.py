"""Request bodies of the HTTP API."""

from pydantic import BaseModel


class PathRequest(BaseModel):
    path: str
