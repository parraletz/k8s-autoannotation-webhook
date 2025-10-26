"""Application entry point"""

import tomllib
from pathlib import Path
from typing import Any, Dict


def get_version() -> str:
    """Get version from pyproject.toml"""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject_data: Dict[str, Any] = tomllib.load(f)
    return str(pyproject_data["project"]["version"])


def get_name() -> str:
    """Get name from pyproject.toml"""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject_data: Dict[str, Any] = tomllib.load(f)
    return str(pyproject_data["project"]["name"])


def get_description() -> str:
    """Get description from pyproject.toml"""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject_data: Dict[str, Any] = tomllib.load(f)
    return str(pyproject_data["project"]["description"])


__version__ = get_version()
__name__ = get_name()
__description__ = get_description()
