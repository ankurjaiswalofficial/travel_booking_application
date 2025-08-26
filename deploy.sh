#!/bin/bash

# Build and start containers
docker-compose up --build -d

# View logs
docker-compose logs -f

# Run migrations (if not done by entrypoint)
docker-compose exec app python manage.py migrate

# Create superuser (if not done by entrypoint)
docker-compose exec app python manage.py createsuperuser

# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Run tests
docker-compose exec app python manage.py test

# Access MySQL
docker-compose exec mysql mysql -u root -p
