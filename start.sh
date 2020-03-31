#!/usr/bin/env bash

echo "=================================="
echo "=       RUNNING SERVER           ="
echo "=================================="
#Initialize database
python manage.py db init

# Run database migrations
python manage.py db migrate
python manage.py db upgrade

# Run server

python manage.py runserver