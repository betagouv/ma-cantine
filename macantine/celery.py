import os
import dotenv
from celery import Celery
from celery.schedules import crontab

dotenv.load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macantine.settings")

app = Celery("macantine", broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"), include=["macantine.tasks"])

# At 10:00 on every day from Monday through Friday.
daily_week = crontab(hour=10, minute=0, day_of_week="1-5")
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
}

app.conf.timezone = "Europe/Paris"

if __name__ == "__main__":
    app.start()
