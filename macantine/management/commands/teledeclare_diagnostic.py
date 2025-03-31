from django.core.management.base import BaseCommand, CommandError

from api.views.teledeclaration import TeledeclarationCreateView
from data.models import Diagnostic, User


class Command(BaseCommand):
    help = "Teledeclare a diagnostic and create a Teledeclaration"

    def add_arguments(self, parser):
        parser.add_argument(
            "--diagnostic_id",
            type=int,
            help="The ID of the diagnostic to teledeclare",
        )
        parser.add_argument(
            "--user-id",
            type=int,
            required=True,
            help="The ID of the user performing the teledeclaration",
        )

    def handle(self, *args, **options):
        diagnostic_id = options["diagnostic_id"]
        user_id = options["user_id"]

        # Fetch the user
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise CommandError(f"User with ID {user_id} does not exist.")

        # Use the TeledeclarationCreateView to teledeclare the diagnostic
        try:
            teledeclaration = TeledeclarationCreateView._teledeclare_diagnostic(diagnostic_id, user)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Teledeclaration created with ID {teledeclaration.id} for Diagnostic {diagnostic_id}."
                )
            )
        except Diagnostic.DoesNotExist:
            raise CommandError(f"Diagnostic with ID {diagnostic_id} does not exist.")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")
