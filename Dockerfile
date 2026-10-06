FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py shell -c \"import os; from django.contrib.auth.models import User; u=User.objects.filter(username='employee1').first(); p=os.getenv('EMPLOYEE_PASSWORD'); u.set_password(p); u.save() if u and p else None\" && gunicorn asset_management.wsgi:application --bind 0.0.0.0:8000"]