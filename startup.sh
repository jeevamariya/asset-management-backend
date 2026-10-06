#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput

python manage.py shell -c "
import os
from django.contrib.auth.models import User

employee_password = os.getenv('EMPLOYEE_PASSWORD')

if employee_password:
    user, created = User.objects.get_or_create(
        username='employee1',
        defaults={'is_staff': False}
    )
    user.is_staff = False
    user.set_password(employee_password)
    user.save()
    print('employee1 user ready')

admin_password = os.getenv('ADMIN_PASSWORD')

if admin_password:
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True}
    )
    user.is_staff = True
    user.is_superuser = True
    user.set_password(admin_password)
    user.save()
    print('admin user ready')
"

exec gunicorn asset_management.wsgi:application --bind 0.0.0.0:8000