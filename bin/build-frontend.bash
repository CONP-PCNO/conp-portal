#!/usr/bin/env bash

# Ensure `fnm` is installed and available in the PATH
if ! command -v fnm &> /dev/null; then
    echo "fnm is not installed or not in PATH."
    echo "Please install Fast Node Manager (fnm) and ensure it's available in your PATH."
    echo "Installation instructions: "
    echo "curl -fsSL https://fnm.vercel.app/install | bash"
    echo "After installation, restart your terminal or run 'source ~/.bashrc' (or equivalent) to load fnm."
    exit 1
fi

# set -euo pipefail
ROOT_DIR=$(dirname "$0")/../  # Adjust this path as necessary to point to the root of your project
cd "$ROOT_DIR" || exit 1
ROOT_DIR="$(pwd)"  # Get the absolute path of the root directory

echo "Current working directory: $ROOT_DIR"


PROJECT_DIRS=(
    "app/static/lib/conp-react/" 
    "app/static/v2/"
)

for dir in "${PROJECT_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        cd "$dir" || exit 1
        echo "Building frontend in: $(pwd)"

        # Load the Node.js version specified in .node-version using fnm
        if [ -f ".node-version" ]; then
            NODE_VERSION=$(cat .node-version)
            fnm install "$NODE_VERSION"
            fnm use "$NODE_VERSION"
        else
            echo ".node-version file not found. Please create one with the desired Node.js version"
            exit 1
        fi

        npm install
        npm run build
        cd "$ROOT_DIR" || exit 1
    else
        echo "Directory $dir does not exist. Skipping."
    fi
done
