#!/bin/bash -l
# Wrapper for the crons defined in clevercloud/cron.json (see docs/cron.md)
# Usage: $ROOT/clevercloud/cron.sh [--prod-only] <command> [<command options>]
# - runs "python manage.py <command> [<command options>] --trigger cron"
# - --prod-only: do nothing if ENVIRONMENT is not "prod"
# - "bash -l" (login shell) is needed to load the app environment variables
#   (calling this script with "/bin/bash ..." in cron.json would cancel it)

# crons are installed on every app deployed from this repo (web & cron apps): only run them where enabled
if [[ "$CRON_ENABLED" != "true" ]]; then
    exit 0
fi

# crons are installed on every instance of the app: only run them on the first one
if [[ "$INSTANCE_NUMBER" != "0" ]]; then
    echo "Instance number is ${INSTANCE_NUMBER}. Stop here."
    exit 0
fi

if [[ "$1" == "--prod-only" ]]; then
    shift
    if [[ "$ENVIRONMENT" != "prod" ]]; then
        echo "Skip command: $1 (prod only, ENVIRONMENT is ${ENVIRONMENT})"
        exit 0
    fi
fi

cd "${APP_HOME}" || exit 1
python manage.py "$@" --trigger cron
