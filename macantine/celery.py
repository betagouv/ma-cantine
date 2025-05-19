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

hourly = crontab(hour="*", minute=0, day_of_week="*")  # Every hour
midnights = crontab(hour=0, minute=0, day_of_week="*")  # Every day at midnight
daily_week = crontab(hour=10, minute=0, day_of_week="1-5")  # Monday to Friday 10AM
nightly_2 = crontab(hour=2, minute=0, day_of_week="*")  # Every day at 2AM
nightly_2_10 = crontab(hour=2, minute=10, day_of_week="*")  # Every day at 2:10AM
nightly_3_week = crontab(hour=3, minute=0, day_of_week="1-5")  # Monday to Friday 3AM
nightly_4 = crontab(hour=4, minute=0, day_of_week="*")  # Every day at 4AM
weekly = crontab(hour=4, minute=0, day_of_week=6)  # Saturday 4AM
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
    "fill_missing_geolocation_data_using_siret": {
        "task": "macantine.tasks.fill_missing_geolocation_data_using_siret",
        "schedule": hourly,
    },
    "fill_missing_geolocation_data_using_insee_code_or_postcode": {
        "task": "macantine.tasks.fill_missing_geolocation_data_using_insee_code_or_postcode",
        "schedule": nightly_2,
    },
    "fill_missing_geolocation_libelle_data": {
        "task": "macantine.tasks.fill_missing_geolocation_libelle_data",
        "schedule": nightly_2_10,
    },
    "delete_old_historical_records": {
        "task": "macantine.tasks.delete_old_historical_records",
        "schedule": nightly_4,
    },
    "export_datasets": {
        "task": "macantine.tasks.continous_datasets_export",
        "schedule": nightly_3_week,
    },
    "update_brevo_contacts": {
        "task": "macantine.tasks.update_brevo_contacts",
        "schedule": midnights,
    },
}

app.conf.timezone = "Europe/Paris"

if __name__ == "__main__":
    app.start()
