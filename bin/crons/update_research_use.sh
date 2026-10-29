#!/usr/bin/env bash
# =================================================================
# Script Name: update_research_use.sh
# Description: Weekly update of the papers that cite or name each CONP
#              dataset (OpenAlex, Europe PMC, DataCite), for dataset pages
#              and the Analytics page.
# =================================================================
#
# Writes DATA_PATH/research_use/latest.json, a dated snapshot in
# DATA_PATH/research_use/snapshots/, and an entry in
# DATA_PATH/research_use/CHANGES.md (also shown at
# /analytics/research-use/changes). Needs OPENALEX_API_KEY in .flaskenv for
# the OpenAlex citation and full-text searches. If a source fails, nothing
# is replaced and the script exits with an error; the next run catches up.
#
# Suggested crontab line (Mondays at 04:30):
#   30 4 * * 1 /home/conp-admin/conp-portal/bin/crons/update_research_use.sh >> /home/conp-admin/conp-portal/logs/update_research_use.log 2>&1

set -Eeuo pipefail

APP_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE}")/../../" &>/dev/null && pwd)
cd "$APP_DIR" || { echo "Error: Cannot enter $APP_DIR"; exit 1; }

VENV_DIR="venv"
VENV_PYTHON="$APP_DIR/$VENV_DIR/bin/python3"
source "$APP_DIR/$VENV_DIR/bin/activate" || { echo "Error: Cannot activate virtual environment"; exit 1; }

echo "----------------------------------------------------"
echo "Research use update started: $(date)"
$VENV_PYTHON -m flask update_research_use
echo "Research use update finished: $(date)"
echo "----------------------------------------------------"
