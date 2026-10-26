import logging
import time

from django.conf import settings

from common.utils.commands import MaCantineBaseCommand

logger = logging.getLogger(__name__)


def invoke_dbt(command: str, dbt_project_dir: str):
    # imported here: dbt is heavy, and importing it at module level slows down every command
    from dbt.cli.main import dbtRunner

    target = "prod" if settings.ENVIRONMENT == "prod" else "dev"
    result = dbtRunner().invoke(
        [
            command,
            "--target",
            target,
            "--project-dir",
            dbt_project_dir,
            "--profiles-dir",
            dbt_project_dir,
        ]
    )
    if not result.success:
        raise result.exception or RuntimeError(f"dbt {command} failed")


class Command(MaCantineBaseCommand):
    """
    Run the dbt models against the analytics data warehouse (Metabase)
    - target: prod in prod, dev elsewhere
    - depends on the *_raw source tables (see: export_dataset --model Raw --destination analysis)

    Usage:
    - python manage.py dbt_run
    """

    help = "Run the dbt models against the analytics data warehouse"

    def handle(self, *args, **options):
        logger.info("Start task: dbt_run")
        start = time.time()

        dbt_project_dir = str(settings.BASE_DIR / "dbt")
        # dbt_packages/ isn't committed (see dbt/.gitignore), so packages must be (re)installed before every run
        invoke_dbt("deps", dbt_project_dir)
        invoke_dbt("run", dbt_project_dir)

        end = time.time()
        logger.info(f"dbt run completed in {end - start:.2f} seconds")
