#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput

python manage.py shell -c "
import os
from django.contrib.auth.models import User

username = 'employee1'
password = os.getenv('EMPLOYEE_PASSWORD')

if password:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'is_staff': False}
    )
    user.set_password(password)
    user.save()
    print('employee1 user ready')
"

exec gunicorn asset_management.wsgi:application --bind 0.0.0.0:8000