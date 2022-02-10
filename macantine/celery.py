import os
import dotenv
from celery import Celery

# from celery.schedules import crontab

dotenv.load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macantine.settings")

app = Celery("macantine", broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"), include=["macantine.tasks"])

# Exemple task configuration
# app.conf.beat_schedule = {"hello_world": {"task": "macantine.tasks.hello_world", "schedule": crontab(minute="*/1")}}

app.conf.beat_schedule = {}
app.conf.timezone = "Europe/Paris"

if __name__ == "__main__":
    app.start()
