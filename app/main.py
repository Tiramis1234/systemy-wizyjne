"""FastAPI application entry point: creates the app and registers routers."""

from fastapi import FastAPI

from app.api import routes_image, routes_workspace
from app.api.errors import register_error_handlers
from app.workspace import Workspace


def create_app() -> FastAPI:
    app = FastAPI(title="Machine Vision Systems")
    app.state.workspace = Workspace()

    register_error_handlers(app)
    app.include_router(routes_image.router)
    app.include_router(routes_workspace.router)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
