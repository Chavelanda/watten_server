#!/bin/bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

gunicorn --bind 0.0.0.0:$PORT wsgi:server