# Travel Booking System

A comprehensive travel booking web application built with Django that allows users to view available travel options, book tickets, and manage their bookings. The application features user authentication, search and filtering capabilities, and a responsive design.

## Features

- **User Management**: Registration, login, logout, and profile management
- **Travel Options**: View flights, trains, and buses with detailed information
- **Booking System**: Book travel options with seat selection and payment calculation
- **Booking Management**: View and cancel existing bookings
- **Search & Filter**: Advanced filtering by type, source, destination, and date
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Pagination**: Efficient browsing of travel options and bookings
- **MySQL Database**: Production-ready database configuration

## Technology Stack

- **Backend**: Django 4.2, Python 3.11
- **Database**: MySQL 8.0
- **Frontend**: Django Templates, Bootstrap 5, HTML5, CSS3
- **Package Management**: Poetry
- **WSGI Server**: Gunicorn
- **Containerization**: Docker, Docker Compose

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker** and **Docker Compose**
  - [Install Docker Desktop](https://www.docker.com/products/docker-desktop)
  - Or install separately:
    - [Docker Engine](https://docs.docker.com/engine/install/)
    - [Docker Compose](https://docs.docker.com/compose/install/)

- **Python 3.11** (for local development without Docker)
- **Poetry** (for dependency management)

## 📦 Installation & Setup

### Method 1: Using Docker (Recommended)

#### 1. Clone the Repository
```bash
git clone https://github.com/ankurjaiswalofficial/travel_booking_application.git
cd travel-booking-system
```

#### 2. Configure Environment Variables
Create a `.env` file in the project root:
```bash
# Django Settings
DJANGO_DEBUG=1
DJANGO_SECRET_KEY=your-secret-key-change-in-production

# Database Settings
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=travel_booking
MYSQL_USER=travel_user
MYSQL_PASSWORD=travel_password
MYSQL_ROOT_PASSWORD=root_password
```

#### 3. Build and Start Containers
```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up --build -d
```

#### 4. Access the Application
- **Main Application**: http://localhost:8002
- **Admin Panel**: http://localhost:8002/admin
- **Health Check**: http://localhost:8002/health
- **MySQL Database**: localhost:3306 (root/root_password)

#### 5. Useful Docker Commands
```bash
# View logs
docker-compose logs -f
docker-compose logs -f app  # App specific logs

# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Run specific commands
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py createsuperuser
docker-compose exec mysql mysql -u root -p

# Rebuild specific service
docker-compose up --build app
```

### Method 2: Local Development without Docker

#### 1. Install Python and Poetry
```bash
# Install Python 3.10 or greater
# Intall poetry
pip install poetry
```

#### 2. Clone and Setup Project
```bash
git clone https://github.com/ankurjaiswalofficial/travel_booking_application.git
cd travel-booking-application

# Install dependencies using Poetry
poetry install

# Activate virtual environment
poetry shell

# Alternatively, install dependencies without activating virtual environment
poetry install --no-root
```

#### 3. Configure MySQL Database

**Install MySQL locally:**
```bash
# On Ubuntu
sudo apt install mysql-server mysql-client

# Start MySQL service
sudo service mysql start
```

**Create Database and User:**
```sql
CREATE DATABASE travel_booking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'travel_user'@'localhost' IDENTIFIED BY 'travel_password';
GRANT ALL PRIVILEGES ON travel_booking.* TO 'travel_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 4. Configure Django Settings
Create a `local_settings.py` file in `travel_booking/` directory:
```python
# local_settings.py
import os

DEBUG = True
SECRET_KEY = 'your-local-secret-key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'travel_booking',
        'USER': 'travel_user',
        'PASSWORD': 'travel_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Add to INSTALLED_APPS if needed
# INSTALLED_APPS += ['debug_toolbar']
```

#### 5. Run Database Migrations
```bash
python manage.py migrate
```

#### 6. Create Superuser
```bash
python manage.py createsuperuser
```

#### 7. Collect Static Files
```bash
python manage.py collectstatic
```

#### 8. Run Development Server
```bash
# Run with default settings
python manage.py runserver

# Run on specific port
python manage.py runserver 8002

# Run with custom settings
python manage.py runserver --settings=travel_booking.local_settings
```

## Database Schema

### Key Models:

1. **TravelOption**
   - travel_id (CharField)
   - travel_type (Choice: flight/train/bus)
   - source (CharField)
   - destination (CharField)
   - departure_datetime (DateTimeField)
   - arrival_datetime (DateTimeField)
   - price (DecimalField)
   - available_seats (IntegerField)

2. **Booking**
   - booking_id (CharField)
   - user (ForeignKey to User)
   - travel_option (ForeignKey to TravelOption)
   - number_of_seats (IntegerField)
   - total_price (DecimalField)
   - booking_date (DateTimeField)
   - status (Choice: confirmed/cancelled)

## Usage Guide

### For Users:
1. **Register/Login**: Create an account or login to existing account
2. **Browse Travel Options**: Use search and filters to find travel options
3. **Book Travel**: Select seats and confirm booking
4. **Manage Bookings**: View and cancel bookings from dashboard

### For Administrators:
1. **Access Admin Panel**: `/admin` with superuser credentials
2. **Manage Travel Options**: Add/edit/delete travel options
3. **View Bookings**: Monitor all user bookings
4. **User Management**: Manage user accounts and permissions

## Configuration Options

### Environment Variables:
- `DJANGO_DEBUG`: Debug mode (1 for development, 0 for production)
- `DJANGO_SECRET_KEY`: Secret key for Django
- `MYSQL_*`: Database connection settings
- `DATABASE_URL`: Alternative database URL

### Gunicorn Settings (in Dockerfile):
- Workers: 2
- Timeout: 120 seconds
- Preload: Enabled for better performance

## Troubleshooting

### Common Issues:

1. **MySQL Connection Errors**
   - Check MySQL service is running
   - Verify database credentials in environment variables
   - Ensure MySQL port 3306 is available

2. **Docker Build Issues**
   - Clear Docker cache: `docker system prune`
   - Check Docker daemon is running

3. **Poetry Installation Issues**
   - Ensure Python 3.11 is installed
   - Check Poetry PATH: `poetry --version`

4. **Port Conflicts**
   - Change ports in docker-compose.yml if 8002 or 3307 are occupied

### Debug Commands:
```bash
# Check Docker containers status
docker-compose ps

# View application logs
docker-compose logs app

# Check MySQL connection
docker-compose exec mysql mysql -u root -p

# Run Django shell
docker-compose exec app python manage.py shell

# Test database connection
docker-compose exec app python manage.py check --database default
```

## Project Structure

```
travel-booking-system/
├── booking_app/          # Main Django application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # URL routes
│   ├── forms.py         # Django forms
│   ├── templates/       # HTML templates
│   └── tests.py         # Test cases
├── travel_booking/      # Django project settings
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── static/              # Static files (CSS, JS, images)
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile          # Docker build instructions
├── pyproject.toml      # Poetry dependencies
└── mysql-init.sql      # Database initialization script
```

## Testing

### Run Tests with Docker:
```bash
docker-compose exec app python manage.py test
```

### Run Tests Locally:
```bash
poetry run python manage.py test
```

### Test Coverage:
```bash
# Install coverage
poetry add coverage

# Run tests with coverage
coverage run manage.py test
coverage report
coverage html  # Generate HTML report
```

## Development Workflow

1. **Make Changes**: Edit code in your preferred IDE
2. **Test Locally**: Run tests to ensure functionality
3. **Build Docker**: Test with Docker environment
4. **Commit Changes**: Use descriptive commit messages
5. **Deploy**: Update production environment (if applicable)

## 🔗 Useful Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

---

**Note**: This is a development setup. For production deployment, ensure you:
- Set `DJANGO_DEBUG=0`
- Use a proper secret key
- Configure HTTPS
- Set up proper database backups
- Use a production-ready WSGI server configuration
- Implement monitoring and logging

