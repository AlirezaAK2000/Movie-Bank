#!/bin/sh

set -e

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

gunicorn --env DJANGO_SETTINGS_MODULE=movieBank.settings movieBank.wsgi:application --bind 0.0.0.0:8000
