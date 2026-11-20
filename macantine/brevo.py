import json
import logging
import re
import time

import sib_api_v3_sdk
from django.conf import settings
from sib_api_v3_sdk.rest import ApiException

logger = logging.getLogger(__name__)

CONTACT_BULK_UPDATE_SIZE = 100
# hours (not 1 day): robust to the cron start time varying slightly from one night to the next
CONTACT_BULK_UPDATE_LAST_UPDATED_THRESHOLD_HOURS = 12
# a batch fails if one of its contacts doesn't exist in Brevo: retry it without the missing contacts
CONTACT_BULK_UPDATE_MAX_RETRIES = 2

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = settings.ANYMAIL.get("SENDINBLUE_API_KEY")
api_client = sib_api_v3_sdk.ApiClient(configuration)
email_api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)
contacts_api_instance = sib_api_v3_sdk.ContactsApi(api_client)


def send_sib_template(template_id, parameters, to_email, to_name):
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email, "name": to_name}],
        params=parameters,
        sender={"email": settings.CONTACT_EMAIL, "name": "ma cantine"},
        reply_to={"email": settings.CONTACT_EMAIL, "name": "ma cantine"},
        template_id=template_id,
    )
    email_api_instance.send_transac_email(send_smtp_email)


def create_newsletter_contact(email):
    create_contact = sib_api_v3_sdk.CreateContact(email=email, update_enabled=True)
    create_contact.list_ids = [int(settings.NEWSLETTER_SENDINBLUE_LIST_ID)]
    contacts_api_instance.create_contact(create_contact)


def user_to_brevo_payload(user, bulk=True):
    """
    The user payload for Brevo API.
    - defined in the User model method `get_brevo_data()`
    - bulk: whether the payload is for bulk update (True) or individual create/update (False)
        - we then use CONTACT_BULK_UPDATE_SIZE

    How to add a new field:
    1. Create the field in Brevo
        - https://my.brevo.com/lists/add-attributes
        - prefix with "MA_CANTINE_"
    2. Add the field in the User model method `get_brevo_data()`
        - you might need to update the corresponding QuerySet
    """
    if bulk:
        return sib_api_v3_sdk.UpdateBatchContactsContacts(email=user.email, attributes=user.get_brevo_data())
    return sib_api_v3_sdk.CreateContact(email=user.email, attributes=user.get_brevo_data(), update_enabled=True)


def _brevo_contact_exists(email):
    try:
        contacts_api_instance.get_contact_info(email)
        return True
    except ApiException as e:
        if e.status == 404:
            return False
        raise
    finally:
        time.sleep(0.1)  # API rate limit is 10 req per second


def get_batch_missing_contact_users(chunk, error):
    """
    If contacts of a batch don't exist in Brevo, the whole batch fails:
    404 {"code": "document_not_found", "message": "No contact found for indexes 43"}
    Return the users of the batch confirmed missing in Brevo,
    or an empty list if the error can't be parsed or confirmed (then nobody should be flagged)
    - indexes: position of the contact in the batch (0-based, checked on prod)
    - each missing contact is confirmed with get_contact_info (in case the indexes don't match the batch)
    """
    if error.status != 404:
        return []
    try:
        body = json.loads(error.body)
    except (TypeError, ValueError):
        return []
    if body.get("code") != "document_not_found":
        return []
    match = re.search(r"indexes\s+([\d,\s]+)", body.get("message", ""))
    if not match:
        return []
    missing_users = []
    for index in [int(index) for index in re.findall(r"\d+", match.group(1))]:
        if index >= len(chunk):
            return []
        user = chunk[index]
        try:
            if _brevo_contact_exists(user.email):
                logger.warning(f"Bulk updating Brevo users: contact of index {index} exists in Brevo (user {user.id})")
                return []
        except ApiException as e:
            logger.warning(f"Bulk updating Brevo users: could not check the contact of index {index}: {e.status}")
            return []
        missing_users.append(user)
    return missing_users


def update_existing_brevo_contacts(users_to_update, today):
    from data.models import User

    flagged_user_ids = []
    for chunk in users_to_update:
        chunk = list(chunk)
        for _ in range(1 + CONTACT_BULK_UPDATE_MAX_RETRIES):
            contacts = [user_to_brevo_payload(user) for user in chunk]
            update_object = sib_api_v3_sdk.UpdateBatchContacts(contacts)
            try:
                contacts_api_instance.update_batch_contacts(update_object)
                # direct update: skips User.save() (validations, avatar optimization...)
                User.objects.filter(id__in=[user.id for user in chunk]).update(brevo_last_update_date=today)
                break
            except ApiException as e:
                missing_users = get_batch_missing_contact_users(chunk, e)
                if not missing_users:
                    logger.exception(f"Bulk updating Brevo users: Error updating Brevo users {e}", stack_info=True)
                    break
                # same as flagging the user in the admin: excluded from the next syncs (see brevo_to_update)
                missing_user_ids = [user.id for user in missing_users]
                User.objects.filter(id__in=missing_user_ids).update(brevo_is_deleted=True)
                flagged_user_ids += missing_user_ids
                logger.warning(f"Bulk updating Brevo users: users missing in Brevo, flagged: {missing_user_ids}")
                chunk = [user for user in chunk if user.id not in missing_user_ids]
                if not chunk:
                    break
            except Exception as e:
                logger.exception(f"Bulk updating Brevo users: Error updating Brevo users {e}", stack_info=True)
                break
            finally:
                time.sleep(0.1)  # API rate limit is 10 req per second
    if flagged_user_ids:
        logger.info(f"Bulk updating Brevo users: {len(flagged_user_ids)} users flagged with brevo_is_deleted=True")
    return flagged_user_ids


def create_new_brevo_contacts(users_to_create, today):
    from data.models import User

    for user in users_to_create:
        try:
            contact = user_to_brevo_payload(user, bulk=False)
            contacts_api_instance.create_contact(contact)
            # direct update: skips User.save() (validations, avatar optimization...)
            User.objects.filter(id=user.id).update(brevo_last_update_date=today)
        except Exception as e:
            logger.exception(f"Error creating/updating an individual Brevo user {e}", stack_info=True)
        time.sleep(0.1)  # API rate limit is 10 req per second
