import logging
from collections import Counter, defaultdict

from oauth2_provider.models import get_access_token_model, get_refresh_token_model

from common.utils.commands import MaCantineBaseCommand
from data.models import Canteen
from data.models.creation_source import CreationSource
from data.utils import has_charfield_missing_query

logger = logging.getLogger(__name__)

FIELD_CHOICES = ["creation_user", "creation_source", "creation_source_api_oauth2_application"]
CHUNK_SIZE = 5000


class Command(MaCantineBaseCommand):
    """
    Usage:
    - python manage.py canteen_fill_creation_user_and_source --field creation_user
    - python manage.py canteen_fill_creation_user_and_source --field creation_source --apply
    - python manage.py canteen_fill_creation_user_and_source --field creation_source_api_oauth2_application --apply

    Note: run creation_user & creation_source first (creation_source_api_oauth2_application depends on them)
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--field",
            type=str,
            required=True,
            choices=FIELD_CHOICES,
            help=f"Field to fill: {', '.join(FIELD_CHOICES)}",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        field = options["field"]
        apply = options["apply"]
        logger.info(f"Start task: canteen_fill_creation_user_and_source ({field}) (apply={apply})")

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        if field == "creation_user":
            fill_creation_user(apply=apply)
        elif field == "creation_source":
            fill_creation_source(apply=apply)
        elif field == "creation_source_api_oauth2_application":
            fill_creation_source_api_oauth2_application(apply=apply)


def get_first_versions(canteen_ids):
    """
    Returns {canteen_id: first history version (dict)}, only if this first version is a creation ("+")
    (one query per chunk, instead of one query per canteen)
    """
    first_versions = {}
    canteen_ids = list(canteen_ids)
    for start in range(0, len(canteen_ids), CHUNK_SIZE):
        versions = (
            Canteen.history.filter(id__in=canteen_ids[start : start + CHUNK_SIZE])
            .order_by("id", "history_date", "history_id")
            .distinct("id")
            .values(
                "id",
                "history_type",
                "history_change_reason",
                "history_user_id",
                "history_user__is_staff",
                "history_source_api_oauth2_application_id",
            )
        )
        first_versions.update({version["id"]: version for version in versions if version["history_type"] == "+"})
    return first_versions


def update_canteens(field, values_by_canteen_id, apply, log_values=True):
    """
    values_by_canteen_id: {canteen_id: value}
    Grouped by value to limit the number of queries
    """
    logger.info(f"{'Filling' if apply else 'Would fill'} {len(values_by_canteen_id)} canteens")
    if log_values:
        logger.info(Counter(values_by_canteen_id.values()))
    if apply:
        canteen_ids_by_value = defaultdict(list)
        for canteen_id, value in values_by_canteen_id.items():
            canteen_ids_by_value[value].append(canteen_id)
        for value, canteen_ids in canteen_ids_by_value.items():
            for start in range(0, len(canteen_ids), CHUNK_SIZE):
                Canteen.all_objects.filter(id__in=canteen_ids[start : start + CHUNK_SIZE]).update(**{field: value})


def fill_creation_user(apply):
    """
    Rules:
    - if creation_user is null, then look at the first version of the canteen in the history:
        - set creation_user to history_user
    - else creation_user stays empty
    """
    canteen_ids = list(Canteen.all_objects.filter(creation_user__isnull=True).values_list("id", flat=True))
    logger.info(f"Found {len(canteen_ids)} canteens with missing creation_user")

    creation_user_by_canteen_id = {
        canteen_id: first_version["history_user_id"]
        for canteen_id, first_version in get_first_versions(canteen_ids).items()
        if first_version["history_user_id"]
    }
    update_canteens("creation_user_id", creation_user_by_canteen_id, apply=apply, log_values=False)

    logger.info(
        f"Done! {Canteen.all_objects.exclude(creation_user__isnull=True).count()} canteens with filled creation_user"
    )


def get_creation_source_from_first_version(first_version):
    if not first_version:
        return None
    change_reason = first_version["history_change_reason"]
    if change_reason is None:
        if first_version["history_user_id"] and first_version["history_user__is_staff"]:
            return CreationSource.ADMIN
    elif change_reason.startswith("Mass CSV import"):
        return CreationSource.IMPORT
    elif change_reason == "SessionAuthentication":
        return CreationSource.APP
    elif change_reason == "OAuth2Authentication":
        return CreationSource.API
    return None


def fill_creation_source(apply):
    """
    Rules:
    - if import_source starts with "Cuisine centrale : ", then creation_source = "APP"
    - else if import_source is not empty, then creation_source = "IMPORT"
    - else look at the first version of the canteen in the history:
        - if history_change_reason is null and history_user is staff, then creation_source = "ADMIN"
        - if history_change_reason starts with "Mass CSV import", then creation_source = "IMPORT"
        - if history_change_reason is "SessionAuthentication", then creation_source = "APP"
        - if history_change_reason is "OAuth2Authentication", then creation_source = "API"
    - else creation_source stays empty

    Note: moved from data/migrations/0183_canteen_creation_source_populate.py
    """
    canteens = list(
        Canteen.all_objects.filter(has_charfield_missing_query("creation_source")).values_list("id", "import_source")
    )
    logger.info(f"Found {len(canteens)} canteens with missing creation_source")
    logger.info(Counter(Canteen.all_objects.values_list("creation_source", flat=True)))

    creation_source_by_canteen_id = {}
    canteen_ids_without_import_source = []
    # first set of rules: import_source
    for canteen_id, import_source in canteens:
        if import_source and import_source.startswith("Cuisine centrale : "):
            creation_source_by_canteen_id[canteen_id] = CreationSource.APP
        elif import_source:
            creation_source_by_canteen_id[canteen_id] = CreationSource.IMPORT
        else:
            canteen_ids_without_import_source.append(canteen_id)
    # second set of rules: HistoricalCanteen
    first_versions = get_first_versions(canteen_ids_without_import_source)
    for canteen_id in canteen_ids_without_import_source:
        creation_source = get_creation_source_from_first_version(first_versions.get(canteen_id))
        if creation_source:
            creation_source_by_canteen_id[canteen_id] = creation_source

    update_canteens("creation_source", creation_source_by_canteen_id, apply=apply)

    canteen_qs_after = Canteen.all_objects.exclude(has_charfield_missing_query("creation_source"))
    logger.info(f"Done! {canteen_qs_after.count()} canteens with filled creation_source")
    logger.info(Counter(Canteen.all_objects.values_list("creation_source", flat=True)))


def get_user_token_periods(user_ids):
    """
    Returns {user_id: [(application_id, start, end)]} from the OAuth2 access & refresh tokens
    - access token: valid from created to expires
    - refresh token: valid from created to revoked (None if not revoked)
    Note: access tokens are deleted when refreshed, but refresh tokens are kept (revoked)
    """
    token_periods = defaultdict(list)
    for user_id, application_id, created, expires in (
        get_access_token_model()
        .objects.filter(user_id__in=user_ids, application__isnull=False)
        .values_list("user_id", "application_id", "created", "expires")
    ):
        token_periods[user_id].append((application_id, created, expires))
    for user_id, application_id, created, revoked in (
        get_refresh_token_model()
        .objects.filter(user_id__in=user_ids, application__isnull=False)
        .values_list("user_id", "application_id", "created", "revoked")
    ):
        token_periods[user_id].append((application_id, created, revoked))
    return token_periods


def get_application_from_token_periods(token_periods, date):
    """
    Rules:
    - if only one application had a valid token at the given date, then return it
    - else if the user only ever used one application, then return it
    - else return None (ambiguous or unknown)
    """
    applications_at_date = {
        application_id
        for application_id, start, end in token_periods
        if start <= date and (end is None or date <= end)
    }
    if len(applications_at_date) == 1:
        return applications_at_date.pop(), "token valid at creation date"
    if len(applications_at_date) > 1:
        return None, "ambiguous: several tokens valid at creation date"
    applications = {application_id for application_id, _, _ in token_periods}
    if len(applications) == 1:
        return applications.pop(), "only application used by the creation_user"
    if len(applications) > 1:
        return None, "ambiguous: several applications used by the creation_user"
    return None, "unknown: no token for the creation_user"


def fill_creation_source_api_oauth2_application(apply):
    """
    Only for canteens with creation_source = "API" (and creation_source_api_oauth2_application empty)

    Rules:
    - if the first version of the canteen in the history has a history_source_api_oauth2_application, then use it
    - else look at the OAuth2 tokens of the creation_user (see get_application_from_token_periods)
    - else creation_source_api_oauth2_application stays empty
    """
    canteens = list(
        Canteen.all_objects.filter(
            creation_source=CreationSource.API, creation_source_api_oauth2_application__isnull=True
        ).values_list("id", "creation_user_id", "creation_date")
    )
    logger.info(f"Found {len(canteens)} API canteens with missing creation_source_api_oauth2_application")

    first_versions = get_first_versions([canteen_id for canteen_id, _, _ in canteens])
    token_periods_by_user_id = get_user_token_periods({user_id for _, user_id, _ in canteens if user_id})

    application_by_canteen_id = {}
    reasons = Counter()
    for canteen_id, creation_user_id, creation_date in canteens:
        first_version = first_versions.get(canteen_id)
        if first_version and first_version["history_source_api_oauth2_application_id"]:
            application_by_canteen_id[canteen_id] = first_version["history_source_api_oauth2_application_id"]
            reasons["history_source_api_oauth2_application"] += 1
        elif not creation_user_id:
            reasons["unknown: no creation_user"] += 1
        else:
            application_id, reason = get_application_from_token_periods(
                token_periods_by_user_id.get(creation_user_id, []), creation_date
            )
            if application_id:
                application_by_canteen_id[canteen_id] = application_id
            reasons[reason] += 1
    logger.info(reasons)

    update_canteens("creation_source_api_oauth2_application_id", application_by_canteen_id, apply=apply)

    canteen_qs_after = Canteen.all_objects.filter(
        creation_source=CreationSource.API, creation_source_api_oauth2_application__isnull=False
    )
    logger.info(f"Done! {canteen_qs_after.count()} API canteens with filled creation_source_api_oauth2_application")
