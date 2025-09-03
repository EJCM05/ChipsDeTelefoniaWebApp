#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install setuptools
pip install -r requirements.txt

python manage.py collectstatic --no-input
