#!/bin/bash
# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
while ! nc -z mysql 3306; do
  sleep 1
done
echo "MySQL is ready!"

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Populating dummy data
echo "Creating superuser..."
python populate_data.py

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start application
echo "Starting Django application with Gunicorn..."
# exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120 --preload
exec python manage.py runserver 0.0.0.0:8000
exec "$@"
