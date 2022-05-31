#!/bin/sh

# wait for PSQL server to start
sleep 10

# prepare init migration
sh -c "python manage.py makemigrations"

# migrate db, so we have the latest db schema
sh -c "python manage.py migrate" 

# createsuperuser
sh -c "django-admin createsuperuser --noinput --username admin --email 111@gogo.com"
 
# start development server on public ip interface, on port 8000
sh -c "python manage.py runserver 0.0.0.0:8000"  