"""Access to the application state from route functions."""

from typing import Annotated

from fastapi import Depends, Request

from app.sources.manager import SourceManager
from app.workspace import Workspace


def get_workspace(request: Request) -> Workspace:
    return request.app.state.workspace


def get_sources(request: Request) -> SourceManager:
    return request.app.state.sources


WorkspaceDep = Annotated[Workspace, Depends(get_workspace)]
SourcesDep = Annotated[SourceManager, Depends(get_sources)]
