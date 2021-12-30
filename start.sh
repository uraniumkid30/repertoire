#!/bin/bash
python manage.py migrate
python manage.py parse_files_to_db
python manage.py runserver 0.0.0.0:8000