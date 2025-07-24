#!/bin/sh

export DJANGO_SUPERUSER_PASSWORD=test_root_password
python manage.py createsuperuser --no-input --username taro
python manage.py collectstatic --no-input

python manage.py runserver 0.0.0.0:8000
