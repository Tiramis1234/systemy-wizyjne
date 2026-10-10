"""Application-wide defaults, kept in one place.

Paths are relative to the working directory: the repository root when run with
`uv run fastapi dev app/main.py`, and /app inside the Docker container.
"""

from pathlib import Path

# Starter data from the course package (images and videos for demos and tests).
SAMPLES_DIR = Path("data/samples")
