#!/bin/sh

# wait for PSQL server to start
sleep 10

# prepare init migration
sh -c "python manage.py makemigrations"

# migrate db, so we have the latest db schema
sh -c "python manage.py migrate" 

# createsuperuser
sh -c "django-admin createsuperuser --noinput --username admin --email 111@gogo.com"
 
# collect static files
sh -c "python manage.py collectstatic --no-input --clear"

sh -c "gunicorn model1.wsgi:application --bind 0.0.0.0:8000"