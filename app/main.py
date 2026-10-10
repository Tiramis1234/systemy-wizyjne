"""FastAPI application entry point: creates the app and registers routers."""

from fastapi import FastAPI

app = FastAPI(title="Machine Vision Systems")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
