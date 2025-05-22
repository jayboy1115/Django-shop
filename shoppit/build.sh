#!/bin/bash
set -o errexit

# Install dependencies using Poetry
poetry install --no-interaction --no-ansi

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate