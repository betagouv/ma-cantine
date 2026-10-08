"""
Shared helpers for the *_fill_creation_user_and_source management commands
(fill creation_user, creation_source & creation_source_api_oauth2_application from the history & OAuth2 tokens)
"""

import logging
from collections import Counter, defaultdict

from oauth2_provider.models import get_access_token_model, get_refresh_token_model

from data.models.creation_source import CreationSource

logger = logging.getLogger(__name__)

CHUNK_SIZE = 5000


def get_first_versions(history_manager, object_ids):
    """
    Returns {object_id: first history version (dict)}, only if this first version is a creation ("+")
    (one query per chunk, instead of one query per object)
    """
    first_versions = {}
    object_ids = list(object_ids)
    for start in range(0, len(object_ids), CHUNK_SIZE):
        versions = (
            history_manager.filter(id__in=object_ids[start : start + CHUNK_SIZE])
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


def update_objects(manager, field, values_by_object_id, apply, log_values=True):
    """
    values_by_object_id: {object_id: value}
    Grouped by value to limit the number of queries
    """
    logger.info(f"{'Filling' if apply else 'Would fill'} {len(values_by_object_id)} {manager.model.__name__}")
    if log_values:
        logger.info(Counter(values_by_object_id.values()))
    if apply:
        object_ids_by_value = defaultdict(list)
        for object_id, value in values_by_object_id.items():
            object_ids_by_value[value].append(object_id)
        for value, object_ids in object_ids_by_value.items():
            for start in range(0, len(object_ids), CHUNK_SIZE):
                manager.filter(id__in=object_ids[start : start + CHUNK_SIZE]).update(**{field: value})


def fill_creation_user(manager, history_manager, apply):
    """
    Rules:
    - if creation_user is null, then look at the first version of the object in the history:
        - set creation_user to history_user
    - else creation_user stays empty
    """
    object_ids = list(manager.filter(creation_user__isnull=True).values_list("id", flat=True))
    logger.info(f"Found {len(object_ids)} {manager.model.__name__} with missing creation_user")

    creation_user_by_object_id = {
        object_id: first_version["history_user_id"]
        for object_id, first_version in get_first_versions(history_manager, object_ids).items()
        if first_version["history_user_id"]
    }
    update_objects(manager, "creation_user_id", creation_user_by_object_id, apply=apply, log_values=False)

    filled_count = manager.exclude(creation_user__isnull=True).count()
    logger.info(f"Done! {filled_count} {manager.model.__name__} with filled creation_user")


def get_creation_source_from_first_version(first_version):
    """
    Rules (on the first version of the object in the history):
    - if history_change_reason is null and history_user is staff, then creation_source = "ADMIN"
    - if history_change_reason starts with "Mass CSV import", then creation_source = "IMPORT"
    - if history_change_reason is "SessionAuthentication", then creation_source = "APP"
    - if history_change_reason is "OAuth2Authentication", then creation_source = "API"
    - else None
    """
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
        return applications_at_date.pop()
    if len(applications_at_date) > 1:
        return None
    applications = {application_id for application_id, _, _ in token_periods}
    if len(applications) == 1:
        return applications.pop()
    return None


def fill_creation_source_api_oauth2_application(manager, history_manager, apply):
    """
    Only for objects with creation_source = "API" (and creation_source_api_oauth2_application empty)
    history_manager: None if the model has no history (e.g. Purchase)

    Rules:
    - if the first version of the object in the history has a history_source_api_oauth2_application, then use it
    - else look at the OAuth2 tokens of the creation_user (see get_application_from_token_periods)
    - else creation_source_api_oauth2_application stays empty
    """
    objects = list(
        manager.filter(
            creation_source=CreationSource.API, creation_source_api_oauth2_application__isnull=True
        ).values_list("id", "creation_user_id", "creation_date")
    )
    logger.info(
        f"Found {len(objects)} API {manager.model.__name__} with missing creation_source_api_oauth2_application"
    )

    first_versions = (
        get_first_versions(history_manager, [object_id for object_id, _, _ in objects]) if history_manager else {}
    )
    token_periods_by_user_id = get_user_token_periods({user_id for _, user_id, _ in objects if user_id})

    application_by_object_id = {}
    for object_id, creation_user_id, creation_date in objects:
        first_version = first_versions.get(object_id)
        if first_version and first_version["history_source_api_oauth2_application_id"]:
            application_by_object_id[object_id] = first_version["history_source_api_oauth2_application_id"]
        elif creation_user_id:
            application_id = get_application_from_token_periods(
                token_periods_by_user_id.get(creation_user_id, []), creation_date
            )
            if application_id:
                application_by_object_id[object_id] = application_id

    update_objects(manager, "creation_source_api_oauth2_application_id", application_by_object_id, apply=apply)

    filled_count = manager.filter(
        creation_source=CreationSource.API, creation_source_api_oauth2_application__isnull=False
    ).count()
    logger.info(
        f"Done! {filled_count} API {manager.model.__name__} with filled creation_source_api_oauth2_application"
    )
