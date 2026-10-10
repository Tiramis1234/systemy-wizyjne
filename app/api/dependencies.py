"""Access to the application state from route functions."""

from fastapi import Request

from app.workspace import Workspace


def get_workspace(request: Request) -> Workspace:
    return request.app.state.workspace
