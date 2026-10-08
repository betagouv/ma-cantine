from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate


def sync_schedules_after_migrate(sender, **kwargs):
    from macantine.schedules import sync_schedules

    sync_schedules()


class MacantineConfig(AppConfig):
    name = "macantine"

    def ready(self):
        # runs after `migrate` (i.e. on every deploy)
        # post_migrate is only sent for apps with models, hence django_q as the sender
        post_migrate.connect(sync_schedules_after_migrate, sender=apps.get_app_config("django_q"))
