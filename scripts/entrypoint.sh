#!/bin/bash

pyfiglet BULLETIN

echo "Running makemigrations and migrate..."
python3 manage.py makemigrations
python3 manage.py migrate

echo "Loading Fixtures..."
#python3 manage.py loaddata {}

echo "Creating Superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); print('Admin User Exists....') if User.objects.filter(username='admin').exists() else User.objects.create_superuser('admin', 'test@test.com', 'admin') " | python3 manage.py shell

echo "Collecting static.."
echo "yes" | python3 manage.py collectstatic

python3 -m core.tasks & disown

daphne -b 0.0.0.0 -p $PORT  -t 60 --application-close-timeout 60 core.asgi:application
