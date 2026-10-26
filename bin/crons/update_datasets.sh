#!/usr/bin/env bash
# =================================================================
# Script Name: update_datasets.sh
# Description: Professional update for CONP portal.
# =================================================================

# This script is used to update the datasets in the CONP portal. It performs the following steps:
# 1. Updates the Git repositories for the datasets.
# 2. Fixes any encoding issues in the DATS.json files.
# 3. Triggers the Flask application to update the database with the new dataset information.

# --- 1. Configuration ---

# Set strict mode for the script;
# exit on any error, treat unset variables as an error
# and any command in a pipeline that fails will cause the entire pipeline to fail.
set -Eeuo pipefail

# Set the Flask application directory
# SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
APP_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE}")/../../" &>/dev/null && pwd)
echo "Flask App Directory: $APP_DIR"
# APP_DIR=/home/conp-admin/conp-portal
cd "$APP_DIR" || { echo "Error: Cannot enter $APP_DIR"; exit 1; }

# Set the virtual environment Python executable
VENV_DIR="venv"
VENV_PYTHON="$APP_DIR/$VENV_DIR/bin/python3"
source "$APP_DIR/$VENV_DIR/bin/activate" || { echo "Error: Cannot activate virtual environment"; exit 1; }

echo "----------------------------------------------------"
echo "Full Update Process started: $(date)"

# --- Trigger Flask Application Update ---
echo "Triggering Flask portal update..."

# @todo: we do not have flock, yet
# LOCK=/var/lock/conp-update-datasets.lock
# exec flock -n "$LOCK" \
#   "$APP_DIR/$VENV_DIR/bin/python3" -m flask --app "$APP_DIR/conp.py" update_datasets

# Run the metadata update command
$VENV_PYTHON -m flask update_datasets

# Final Status Check
if [ $? -eq 0 ]; then
    echo "SUCCESS: Git updated, encodings fixed, and DB synced."
else
    echo "ERROR: Flask task failed. Check $APP_DIR/logs (if any)."
    exit 1
fi

echo "Process completed successfully at: $(date)"
echo "----------------------------------------------------"
