#!/bin/sh


python manage.py makemigrations --no-input
python manage.py migrate --no-input


python manage.py collectstatic --no-input
python manage.py collectstatic --no-input


gunicorn Baches_Web.wsgi:application --bind 0.0.0.0:8000


