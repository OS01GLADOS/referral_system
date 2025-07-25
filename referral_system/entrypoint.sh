#!/bin/sh

python manage.py migrate

export DJANGO_SUPERUSER_PASSWORD=test_root_password
python manage.py createsuperuser --no-input --username taro --email example@example.com
python manage.py collectstatic --no-input

python manage.py runserver 0.0.0.0:8000
