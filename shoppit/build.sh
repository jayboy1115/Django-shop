#!/bin/bash
set -o errexit

# Install dependencies using pip
pip install -r ../requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate