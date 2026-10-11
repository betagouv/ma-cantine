from datetime import datetime

from croniter import croniter
from django.conf import settings
from django.db import transaction
from django.utils import timezone

# Cron expressions (evaluated in settings.TIME_ZONE)
every_6_hours_10 = "10 */6 * * *"  # Every 6 hours at :10
every_6_hours_20 = "20 */6 * * *"  # Every 6 hours at :20
every_6_hours_0 = "0 */6 * * *"  # Every 6 hours
nightly_0_20 = "20 0 * * *"  # Every day at 12:20AM
nightly_0_30 = "30 0 * * *"  # Every day at 12:30AM
nightly_1 = "0 1 * * *"  # Every day at 1AM
nightly_1_30 = "30 1 * * *"  # Every day at 1:30AM
nightly_2 = "0 2 * * *"  # Every day at 2AM
nightly_3 = "0 3 * * *"  # Every day at 3AM

# Periodic tasks (key = function name in macantine/tasks.py)
# Synced into django-q2 Schedule objects after each `migrate` (see macantine/apps.py)
PERIODIC_TASKS = {
    #########################################################
    # Canteen data (needed for User data task, analysis & opendata)
    "canteen_fill_declaration_donnees_year_field": {"cron": every_6_hours_10},  # Campaign-related
    #########################################################
    # User data (needed for Brevo)
    "update_user_data": {"cron": nightly_0_20},
    #########################################################
    # Brevo
    "update_brevo_contacts": {"cron": nightly_0_30, "prod_only": True},
    #########################################################
    # Dataset exports
    "export_dataset_raw_analysis": {"cron": nightly_1, "prod_only": True},
    "export_dataset_canteen_analysis": {"cron": nightly_2, "prod_only": True},  # every_6_hours_20 during campaigns
    # Campaign-related (commented out outside of campaigns)
    # "export_dataset_td_analysis": {"cron": every_6_hours_0},
    "export_dataset_canteen_opendata": {"cron": nightly_2, "prod_only": True},  # every_6_hours_20 during campaigns
    #########################################################
    # DBT (Metabase) — depends on export_dataset_raw_analysis (nightly_1)
    "dbt_run": {"cron": nightly_1_30, "prod_only": True},
    #########################################################
    # History cleanup
    "delete_old_historical_records": {"cron": nightly_3},
}

TASKS_MODULE = "macantine.tasks"


def get_enabled_periodic_tasks():
    is_prod = settings.ENVIRONMENT == "prod"
    return {name: config for name, config in PERIODIC_TASKS.items() if is_prod or not config.get("prod_only")}


def get_next_run(cron):
    return croniter(cron, timezone.localtime()).get_next(datetime)


@transaction.atomic
def sync_schedules():
    """
    Make the django-q2 Schedule objects match PERIODIC_TASKS:
    - create the missing ones, update the cron of the existing ones
    - delete the ones of macantine.tasks that are not (or no longer) enabled
    Schedules of other functions (e.g. created manually in the admin) are left untouched.
    """
    from django_q.models import Schedule

    enabled_tasks = get_enabled_periodic_tasks()

    for name, config in enabled_tasks.items():
        schedule = Schedule.objects.filter(name=name).first() or Schedule(name=name)
        if schedule.pk and schedule.cron == config["cron"] and schedule.func == f"{TASKS_MODULE}.{name}":
            continue
        schedule.func = f"{TASKS_MODULE}.{name}"
        schedule.schedule_type = Schedule.CRON
        schedule.cron = config["cron"]
        schedule.repeats = -1
        # Schedule.next_run defaults to now: without this, a new schedule would run right away
        schedule.next_run = get_next_run(config["cron"])
        schedule.save()

    Schedule.objects.filter(func__startswith=f"{TASKS_MODULE}.").exclude(name__in=enabled_tasks.keys()).delete()
