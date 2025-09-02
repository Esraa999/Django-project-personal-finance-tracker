#!/bin/sh

# Wait for database
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

# Only run migrations and create superuser from web container, not cron
if [ "$1" = "python" ] && [ "$2" = "manage.py" ] && [ "$3" = "runserver" ]; then
    echo "Running migrations from web container..."
    python manage.py makemigrations accounts
    python manage.py makemigrations transactions
    python manage.py migrate

    echo "Creating superuser from web container..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF
fi

# Start cron daemon for cron container
if [ "$1" = "cron" ]; then
    echo "Starting cron daemon..."
    service cron start
fi

exec "$@"