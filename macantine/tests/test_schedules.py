from datetime import datetime
from zoneinfo import ZoneInfo

from django.test import TestCase, override_settings
from django_q.models import Schedule
from freezegun import freeze_time

from macantine import tasks
from macantine.schedules import PERIODIC_TASKS, sync_schedules

PARIS_TZ = ZoneInfo("Europe/Paris")


class SyncSchedulesTest(TestCase):
    def setUp(self):
        # schedules are also synced by the post_migrate signal when the test database is created
        Schedule.objects.all().delete()

    def test_periodic_tasks_exist_in_tasks_module(self):
        for name in PERIODIC_TASKS:
            self.assertTrue(callable(getattr(tasks, name, None)), name)

    @override_settings(ENVIRONMENT="prod")
    def test_prod_creates_all_schedules(self):
        sync_schedules()

        self.assertEqual(set(Schedule.objects.values_list("name", flat=True)), set(PERIODIC_TASKS))
        schedule = Schedule.objects.get(name="dbt_run")
        self.assertEqual(schedule.func, "macantine.tasks.dbt_run")
        self.assertEqual(schedule.schedule_type, Schedule.CRON)
        self.assertEqual(schedule.cron, PERIODIC_TASKS["dbt_run"]["cron"])

    @override_settings(ENVIRONMENT="staging")
    def test_non_prod_skips_prod_only_schedules(self):
        sync_schedules()

        expected = {name for name, config in PERIODIC_TASKS.items() if not config.get("prod_only")}
        self.assertEqual(set(Schedule.objects.values_list("name", flat=True)), expected)
        self.assertFalse(Schedule.objects.filter(name="dbt_run").exists())

    @override_settings(ENVIRONMENT="prod")
    @freeze_time("2026-10-08 12:00:00+02:00")
    def test_next_run_is_computed_from_cron(self):
        sync_schedules()

        # not "now" (Schedule.next_run default), which would run all the tasks right after a deploy
        dbt_run_schedule = Schedule.objects.get(name="dbt_run")  # 1:30AM
        self.assertEqual(dbt_run_schedule.next_run, datetime(2026, 10, 9, 1, 30, tzinfo=PARIS_TZ))

    @override_settings(ENVIRONMENT="prod")
    def test_sync_is_idempotent_and_keeps_next_run(self):
        sync_schedules()
        schedule = Schedule.objects.get(name="dbt_run")
        next_run = datetime(2030, 1, 1, tzinfo=PARIS_TZ)
        Schedule.objects.filter(pk=schedule.pk).update(next_run=next_run)

        sync_schedules()

        self.assertEqual(Schedule.objects.filter(name="dbt_run").count(), 1)
        self.assertEqual(Schedule.objects.get(name="dbt_run").next_run, next_run)

    @override_settings(ENVIRONMENT="prod")
    def test_sync_updates_changed_cron(self):
        sync_schedules()
        Schedule.objects.filter(name="dbt_run").update(cron="0 0 1 1 *")

        sync_schedules()

        self.assertEqual(Schedule.objects.get(name="dbt_run").cron, PERIODIC_TASKS["dbt_run"]["cron"])

    def test_sync_removes_obsolete_task_schedules_only(self):
        Schedule.objects.create(name="old_task", func="macantine.tasks.old_task", schedule_type=Schedule.DAILY)
        Schedule.objects.create(name="manual", func="other.module.func", schedule_type=Schedule.DAILY)

        with override_settings(ENVIRONMENT="prod"):
            sync_schedules()
        with override_settings(ENVIRONMENT="staging"):
            sync_schedules()

        self.assertFalse(Schedule.objects.filter(name="old_task").exists())
        self.assertFalse(Schedule.objects.filter(name="dbt_run").exists())
        self.assertTrue(Schedule.objects.filter(name="manual").exists())
