"""Kubernetes Webhook Mutator Package.

This package provides a FastAPI-based Kubernetes admission webhook
for mutating pod resources with custom annotations.
"""

import tomllib
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

__all__ = ["__version__", "__name__", "__description__"]


@lru_cache(maxsize=1)
def _load_project_metadata() -> Dict[str, Any]:
    """Load and cache project metadata from pyproject.toml.

    Returns:
        Dict containing the project metadata.

    Raises:
        FileNotFoundError: If pyproject.toml is not found.
        KeyError: If required project fields are missing.
    """
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

    try:
        with open(pyproject_path, "rb") as f:
            data: Dict[str, Any] = tomllib.load(f)
        project_data: Dict[str, Any] = data["project"]
        return project_data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"pyproject.toml not found at {pyproject_path}") from e
    except KeyError as e:
        raise KeyError("Missing 'project' section in pyproject.toml") from e


def get_version() -> str:
    """Get version from pyproject.toml.

    Returns:
        The project version string.
    """
    return str(_load_project_metadata()["version"])


def get_name() -> str:
    """Get name from pyproject.toml.

    Returns:
        The project name string.
    """
    return str(_load_project_metadata()["name"])


def get_description() -> str:
    """Get description from pyproject.toml.

    Returns:
        The project description string.
    """
    return str(_load_project_metadata()["description"])


# Package metadata - loaded once at import time
__version__ = get_version()
__name__ = get_name()
__description__ = get_description()
