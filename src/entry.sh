#!/bin/sh


python manage.py makemigrations --no-input
python manage.py migrate --no-input


python manage.py collectstatic --no-input
python manage.py collectstatic --no-input






echo "Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="${DJANGO_SUPERUSER_EMAIL}").exists():
    User.objects.create_superuser(
        email="${DJANGO_SUPERUSER_EMAIL}",
        password="${DJANGO_SUPERUSER_PASSWORD}"
    )
EOF










gunicorn Baches_Web.wsgi:application --bind 0.0.0.0:8000


