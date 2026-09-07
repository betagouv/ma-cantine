import os
import subprocess

from django.core.management.base import BaseCommand

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class Command(BaseCommand):
    help = "Fetches npm dependencies and makes a prod build of the frontend application"

    def handle(self, *args, **options):
        os.chdir(os.path.join(BASE_DIR, "2024-frontend"))
        subprocess.run(["npm", "ci", "--ignore-scripts"], check=True)
        subprocess.run(["npm", "run", "build"], check=True)
        os.chdir(os.path.join(BASE_DIR))
