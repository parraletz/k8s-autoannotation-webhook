"""Application entry point"""

import os

import uvicorn

from app.api.server import app  # noqa: F401

if __name__ == "__main__":
    # Use environment variable for host, default to localhost for security
    # In production/container environments, set HOST=0.0.0.0
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))

    if os.getenv("ENVIRONMENT") == "local":
        uvicorn.run("main:app", host=host, port=port, reload=True)
    else:
        uvicorn.run("main:app", host=host, port=port)
