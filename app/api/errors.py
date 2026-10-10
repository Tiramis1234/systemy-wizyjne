"""Maps expected application errors to HTTP responses with a readable message.

The frontend shows the "detail" field to the user, so every error keeps the
interface informative instead of failing silently.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.errors import (
    ImageDecodeError,
    ImageEncodeError,
    ImageLoadError,
    ImageSaveError,
    VisionError,
)

# 404: the thing the user pointed to is not there; 400: it is there but invalid.
STATUS_CODES: dict[type[Exception], int] = {
    ImageLoadError: 404,
    ImageDecodeError: 400,
    ImageEncodeError: 400,
    ImageSaveError: 400,
}


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(VisionError)
    def handle_vision_error(request: Request, error: VisionError) -> JSONResponse:
        status_code = STATUS_CODES.get(type(error), 400)
        return JSONResponse(status_code=status_code, content={"detail": str(error)})

    @app.exception_handler(LookupError)
    def handle_missing_state(request: Request, error: LookupError) -> JSONResponse:
        # Raised when e.g. the result is requested before any image was loaded.
        return JSONResponse(status_code=404, content={"detail": str(error)})
