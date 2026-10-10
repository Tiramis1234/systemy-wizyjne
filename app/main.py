"""FastAPI application entry point: creates the app and registers routers."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import settings
from app.api import routes_camera, routes_image, routes_video, routes_workspace
from app.api.errors import register_error_handlers
from app.sources.manager import SourceManager
from app.workspace import Workspace


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    # On shutdown: release the open video/camera so the device is freed.
    app.state.sources.close()


def create_app() -> FastAPI:
    app = FastAPI(title="Machine Vision Systems", lifespan=lifespan)
    app.state.workspace = Workspace()
    app.state.sources = SourceManager()
    settings.OUTPUT_DIR.mkdir(exist_ok=True)

    register_error_handlers(app)
    app.include_router(routes_camera.router)
    app.include_router(routes_image.router)
    app.include_router(routes_video.router)
    app.include_router(routes_workspace.router)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
