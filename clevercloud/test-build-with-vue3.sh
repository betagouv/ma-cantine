#!/bin/bash

rm -rf static/
rm -rf build/
rm -rf 2024-frontend/build/
bash ./clevercloud/pre-build-hook.sh
# the following should mirror the hooks in clevercloud/python.json["deploy"]["managetasks"]
python manage.py buildnpm
python manage.py buildnpmvue3
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py compilemessages
# use the following command to run the server when testing locally. Need --insecure flag to serve local static assets
# python manage.py runserver --insecure
