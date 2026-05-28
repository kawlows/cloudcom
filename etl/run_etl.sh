#!/usr/bin/env bash
set -e

# Move to the ETL directory
cd "$(dirname "$0")"

echo "Starting CloudCom ETL at $(date)"

# Use system Python, ensure PYTHONPATH includes project root
# Adjust path if needed; here we assume this script is in cloudcom/etl
export PYTHONPATH="$(cd .. && pwd)"

python -m etl.transform_load_reporting

echo "CloudCom ETL finished at $(date)"