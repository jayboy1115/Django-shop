#!/bin/bash
set -o errexit

pip install -r requirements.txt  # ← Fixed (added 's')

python manage.py collectstatic --no-input
python manage.py migrate