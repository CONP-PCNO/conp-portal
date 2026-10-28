#!/usr/bin/env bash

REPO_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE}")/../" &>/dev/null && pwd)
echo "Project Repo Directory: $REPO_DIR"
cd "$REPO_DIR" || { echo "Error: Cannot enter $REPO_DIR"; exit 1; }

export UV_PROJECT_ENVIRONMENT="venv"
uv sync
