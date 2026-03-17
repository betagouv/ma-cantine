import logging

from django.core.management.base import BaseCommand

from data.utils import read_csv, has_charfield_missing_query
from data.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Goal: List Django user IDs whose emails are missing from a Brevo CSV export, or the opposite (Brevo emails missing in Django).

    in_django_but_not_in_brevo
    - Some Django users may have been deleted from Brevo, or have an email that was modified in Django but not synced to Brevo

    in_brevo_but_not_in_django
    - filter only on contacts with 'MA_CANTINE_DATE_INSCRIPTION'
    - Some Brevo contacts may have been deleted from Django, or have an email that was since modified in Django

    Usage:
    - python manage.py user_brevo_contacts_sync path/to/brevo_export.csv
    - python manage.py user_brevo_contacts_sync path/to/brevo_export.csv --mode in_django_but_not_in_brevo
    - python manage.py user_brevo_contacts_sync path/to/brevo_export.csv --mode in_brevo_but_not_in_django
    """

    help = "List Django user IDs whose emails are missing from a Brevo CSV export"

    def add_arguments(self, parser):
        parser.add_argument(
            "brevo_contacts_csv_path",
            type=str,
            help="Path to a Brevo CSV file, or a folder containing Brevo CSV exports",
        )
        parser.add_argument(
            "--mode",
            choices=["in_django_but_not_in_brevo", "in_brevo_but_not_in_django"],
            help="List Django emails missing in Brevo (opposite: Brevo emails missing in Django)",
        )

    def handle(self, *args, **options):
        brevo_contacts_csv_path = options["brevo_contacts_csv_path"]

        # Brevo csv
        brevo_contacts = read_csv(brevo_contacts_csv_path, delimiter=";")
        logger.info(f"Reading Brevo contacts from {brevo_contacts_csv_path}")
        logger.info(f"Found {len(brevo_contacts)} contacts in Brevo CSV export")
        brevo_contacts_ma_cantine = [
            contact for contact in brevo_contacts if contact.get("MA_CANTINE_DATE_INSCRIPTION")
        ]
        logger.info(
            f"Found {len(brevo_contacts_ma_cantine)} contacts with MA_CANTINE_DATE_INSCRIPTION in Brevo CSV export"
        )
        brevo_contacts_ma_cantine_emails = [
            contact["EMAIL"].strip().lower() for contact in brevo_contacts_ma_cantine if contact.get("EMAIL")
        ]
        logger.info(f"Found {len(brevo_contacts_ma_cantine_emails)} contacts with an email in Brevo CSV export")

        # Django users
        django_users_qs = User.objects.exclude(has_charfield_missing_query("email"))
        django_users_emails = list(django_users_qs.values_list("email", flat=True))
        django_users_emails = [email.strip().lower() for email in django_users_emails if email]
        logger.info(f"Django users with an email: {len(django_users_emails)}")
        django_users_brevo_is_deleted_qs = django_users_qs.filter(brevo_is_deleted=True)
        logger.info(f"Django users flagged with brevo_is_deleted=True: {django_users_brevo_is_deleted_qs.count()}")

        if not options["mode"]:
            pass

        elif options["mode"] == "in_django_but_not_in_brevo":
            scanned_users = 0
            django_only_user_id_list = []

            for user_id, user_email in django_users_qs.values_list("id", "email").iterator(chunk_size=2000):
                scanned_users += 1
                normalized_email = user_email.strip().lower()
                if normalized_email not in brevo_contacts_ma_cantine_emails:
                    django_only_user_id_list.append(user_id)
                if scanned_users % 5000 == 0:
                    logger.info(f"Scanned {scanned_users} users")

            logger.info(
                f"Scanned {scanned_users} users against {len(brevo_contacts_ma_cantine_emails)} Brevo contacts"
            )
            logger.info(f"Django-only users: {len(django_only_user_id_list)}")

        elif options["mode"] == "in_brevo_but_not_in_django":
            scanned_users = 0
            brevo_only_contact_email_list = []

            for brevo_email in brevo_contacts_ma_cantine_emails:
                scanned_users += 1
                if brevo_email not in django_users_emails:
                    brevo_only_contact_email_list.append(brevo_email)
                if scanned_users % 5000 == 0:
                    logger.info(f"Scanned {scanned_users} users")

            logger.info(
                f"Scanned {len(brevo_contacts_ma_cantine_emails)} Brevo contacts against {len(django_users_emails)} Django users"
            )
            logger.info(f"Brevo-only users: {len(brevo_only_contact_email_list)}")
