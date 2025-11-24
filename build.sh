#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Initialize DB if needed (optional, but good for first run)
# flask db upgrade 