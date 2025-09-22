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

app = Celery("macantine", broker=os.getenv("REDIS_URL"), backend="django-db", include=["macantine.tasks"])
app.config_from_object(dict(worker_hijack_root_logger=False, result_extended=True))

every_minute = crontab(minute="*/1")  # For testing purposes
hourly = crontab(hour="*", minute=0, day_of_week="*")  # Every hour
daily_week = crontab(hour=10, minute=0, day_of_week="1-5")  # Monday to Friday 10AM
nightly_0 = crontab(hour=0, minute=0, day_of_week="*")  # Every day at midnight
nightly_4 = crontab(hour=4, minute=0, day_of_week="*")  # Every day at 4AM
nightly_5 = crontab(hour=5, minute=0, day_of_week="*")  # Every day at 5AM
weekly = crontab(hour=4, minute=0, day_of_week=6)  # Saturday 4AM

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
    "fill_missing_geolocation_data_using_insee_code": {
        "task": "macantine.tasks.fill_missing_geolocation_data_using_insee_code",
        "schedule": nightly_4,
    },
    "fill_missing_insee_code_using_siret": {
        "task": "macantine.tasks.fill_missing_insee_code_using_siret",
        "schedule": hourly,
    },
    "delete_old_historical_records": {
        "task": "macantine.tasks.delete_old_historical_records",
        "schedule": nightly_5,
    },
    "export_datasets": {
        "task": "macantine.tasks.continous_datasets_export",
        "schedule": nightly_5,
    },
    "update_brevo_contacts": {
        "task": "macantine.tasks.update_brevo_contacts",
        "schedule": nightly_0,
    },
}

app.conf.timezone = "Europe/Paris"

if __name__ == "__main__":
    app.start()
