import os

import dotenv
from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging


@setup_logging.connect
def void(*args, **kwargs):
    """Override celery's logging setup to prevent it from altering our settings.
    github.com/celery/celery/issues/1867

    :return void:
    """
    pass


dotenv.load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macantine.settings")

app = Celery("macantine", broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"), include=["macantine.tasks"])
app.worker_hijack_root_logger = False

# At 10:00 on every day from Monday through Friday.
daily_week = crontab(hour=10, minute=0, day_of_week="1-5")
nightly = crontab(hour=4, minute=0, day_of_week="*")
midnights = crontab(hour=0, minute=0, day_of_week="*")
weekly = crontab(hour=4, minute=0, day_of_week=6)
every_minute = crontab(minute="*/1")  # For testing purposes

app.conf.beat_schedule = {
    "no_canteen_first_reminder": {
        "task": "macantine.tasks.no_canteen_first_reminder",
        "schedule": daily_week,
    },
    "no_canteen_second_reminder": {
        "task": "macantine.tasks.no_canteen_second_reminder",
        "schedule": daily_week,
    },
    "no_diagnostic_first_reminder": {
        "task": "macantine.tasks.no_diagnostic_first_reminder",
        "schedule": daily_week,
    },
    "fill_missing_geolocation_data_using_insee_code_or_postcode": {
        "task": "macantine.tasks.fill_missing_geolocation_data_using_insee_code_or_postcode",
        "schedule": nightly,
    },
    "delete_old_historical_records": {
        "task": "macantine.tasks.delete_old_historical_records",
        "schedule": nightly,
    },
    "export_datasets": {
        "task": "macantine.tasks.export_datasets",
        "schedule": weekly,
    },
    "update_brevo_contacts": {
        "task": "macantine.tasks.update_brevo_contacts",
        "schedule": midnights,
    },
}

app.conf.timezone = "Europe/Paris"

if __name__ == "__main__":
    app.start()
