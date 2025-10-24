#!/bin/bash
export PYTHONPATH=.
uv run pytest "$@"
