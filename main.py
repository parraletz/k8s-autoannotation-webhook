import os

import uvicorn

from app.api.server import app  # noqa: F401

if __name__ == "__main__":
    if os.getenv("ENVIRONMENT") == "local":
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8000)
