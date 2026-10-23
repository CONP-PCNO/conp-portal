#!/bin/bash

# =================================================================
# Script Name: update_datasets.sh
# Description: Professional update for CONP portal. Handles Git,
#              encodings (UTF-8/Latin-1), and Flask synchronization.
# =================================================================

# --- 1. Configuration ---

# Set the dataset directory
DATASET_DIR="/data/not_backed_up/conp-portal/data/conp-dataset"

# Set the Flask application directory
APP_DIR="/home/conp-admin/conp-portal"

# Set the virtual environment Python executable
VENV_PYTHON="$APP_DIR/venv/bin/python3"

echo "----------------------------------------------------"
echo "Full Update Process started: $(date)"

# --- 2. Update Git Repositories ---
echo "Step 1: Fetching latest data from Git..."

# Ensure the dataset directory exists
cd "$DATASET_DIR" || { echo "Error: Cannot enter $DATASET_DIR"; exit 1; }

# Force main repo to be clean and up-to-date
git fetch origin
git checkout master
git pull origin master

# Synchronize submodule URLs and force update all dataset folders
git submodule sync --recursive
git submodule update --init --recursive --force
git submodule update --remote --recursive

# --- 3. Data Sanitization (Encoding Fixes) ---
echo "Step 2: Fixing DATS.json encoding issues..."

# A. Convert files from Latin-1 to UTF-8 if they fail the UTF-8 check
# This fixes the 'invalid continuation byte' error (e.g., Mendonça Filho)
find projects/ -name "DATS.json" -type f -exec sh -c '
    iconv -f utf-8 -t utf-8 "{}" >/dev/null 2>&1 || \
    (iconv -f latin1 -t utf-8 "{}" > "{}.tmp" && mv "{}.tmp" "{}")
' \;

# B. Replace Greek characters with ASCII equivalents
# This fixes the MySQL 'Incorrect string value' error (e.g., α -> alpha)
find projects/ -name "DATS.json" -type f -writable -exec sed -i 's/\xCE\xB1/alpha/g' {} + 2>/dev/null

# --- 4. Trigger Flask Application Update ---
echo "Step 3: Triggering Flask portal update..."
cd "$APP_DIR" || { echo "Error: Cannot enter $APP_DIR"; exit 1; }

# Run the metadata update command
$VENV_PYTHON -m flask update_datasets

# Final Status Check
if [ $? -eq 0 ]; then
    echo "SUCCESS: Git updated, encodings fixed, and DB synced."
else
    echo "ERROR: Flask task failed. Check /home/conp-admin/conp-portal/logs (if any)."
    exit 1
fi

echo "Process completed successfully at: $(date)"
echo "----------------------------------------------------"
