import os
import subprocess
from django.core.management.base import BaseCommand

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class Command(BaseCommand):
    help = "Fetches npm dependencies and makes a prod build of the frontend application"

    def handle(self, *args, **options):
        print(BASE_DIR)

        os.chdir(os.path.join(BASE_DIR, "frontend"))
        subprocess.run(["npm", "install"])
        subprocess.run(["npm", "run", "build"])
        os.chdir(os.path.join(BASE_DIR))
