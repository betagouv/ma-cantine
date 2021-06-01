#!/bin/bash
python manage.py buildnpm
python manage.py collectstatic
gunicorn macantine.wsgi
