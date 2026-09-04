#!/bin/bash

rm -rf static/
rm -rf build/
bash ./clevercloud/pre-build-hook.sh
# the following should mirror the tasks in CC_PYTHON_MANAGE_TASKS env config
python manage.py buildnpm
python manage.py buildnpmvue3
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py compilemessages
# use the following command to run the server when testing locally. Need --insecure flag to serve local static assets
# python manage.py runserver --insecure
