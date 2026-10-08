#!/bin/bash -l
# Wrapper for the crons defined in clevercloud/cron.json (see docs/cron.md)
# Usage: $ROOT/clevercloud/cron.sh <task_name> [--prod-only]
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

cd "${APP_HOME}" || exit 1
python manage.py run_task "$@"
