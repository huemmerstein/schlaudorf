#!/bin/bash
# Install dependencies and prepare the Django project on Ubuntu.
# This script creates a virtual environment, installs Python requirements,
# and performs the initial database migration.
set -e

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate

echo "Installation complete. Activate the environment with 'source venv/bin/activate' and start the server with 'python manage.py runserver'."
