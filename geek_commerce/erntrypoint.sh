#!/bin/sh

echo "Running database migrations..."
python manage.py migrate

echo "Starting the Django development server..."
python manage.py runserver 0.0.0:8000