#!/usr/bin/env bash
# =================================================================
# Script Name: update_analytics.sh
# Description: Daily update of the Portal's use figures, then a dated copy
#              of the whole use history.
# =================================================================
#
# 1. `flask update_analytics`: Matomo visits, pages, dataset views, downloads
#    and searches; GitHub traffic (views and clones of the dataset
#    repositories); visits by country; then rebuilds the Analytics page.
#    GitHub keeps only the last 14 days of traffic. Each run adds the days the
#    database does not have yet and never deletes any, so the database is our
#    long-term record, as long as this runs at least every 14 days with a
#    GITHUB_PAT that can read traffic (push access to the dataset repositories).
#
# 2. `flask backup_analytics`: copies that history (every Matomo and GitHub
#    table as CSV, the research-use files, countries.json) to
#    ANALYTICS_BACKUP_PATH/YYYY-MM-DD/; keeps 30 daily copies and the first
#    copy of every month. Set ANALYTICS_BACKUP_PATH in .flaskenv to a
#    backed-up folder (DATA_PATH is /data/not_backed_up/...). Runs even when
#    the update fails, so the copy is never skipped.
#
# Suggested crontab line (every day at 03:15):
#   15 3 * * * /home/conp-admin/conp-portal/bin/crons/update_analytics.sh >> /home/conp-admin/conp-portal/logs/update_analytics.log 2>&1

set -Eeuo pipefail

APP_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE}")/../../" &>/dev/null && pwd)
cd "$APP_DIR" || { echo "Error: Cannot enter $APP_DIR"; exit 1; }

VENV_DIR="venv"
VENV_PYTHON="$APP_DIR/$VENV_DIR/bin/python3"
source "$APP_DIR/$VENV_DIR/bin/activate" || { echo "Error: Cannot activate virtual environment"; exit 1; }

echo "----------------------------------------------------"
echo "Analytics update started: $(date)"
status=0
$VENV_PYTHON -m flask update_analytics || status=$?
echo "Analytics update finished (exit $status): $(date)"
$VENV_PYTHON -m flask backup_analytics || status=$?
echo "Analytics backup finished: $(date)"
echo "----------------------------------------------------"
exit $status
