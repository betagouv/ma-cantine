import logging
import time

import requests
import sib_api_v3_sdk
from django.conf import settings

logger = logging.getLogger(__name__)

CONTACT_BULK_UPDATE_SIZE = 100
CONTACT_BULK_UPDATE_LAST_UPDATED_THRESHOLD_DAYS = 1

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


def update_existing_brevo_contacts(users_to_update, today):
    for chunk in users_to_update:
        contacts = [user_to_brevo_payload(user) for user in chunk]
        update_object = sib_api_v3_sdk.UpdateBatchContacts(contacts)
        try:
            contacts_api_instance.update_batch_contacts(update_object)
            for user in chunk:
                user.brevo_last_update_date = today
                user.save()
        except requests.exceptions.HTTPError as e:
            logger.warning(f"Bulk updating Brevo users: One or more of the users don't exist. {e}")
        except Exception as e:
            logger.exception(f"Bulk updating Brevo users: Error updating Brevo users {e}", stack_info=True)
        time.sleep(0.1)  # API rate limit is 10 req per second


def create_new_brevo_contacts(users_to_create, today):
    for user in users_to_create:
        try:
            contact = user_to_brevo_payload(user, bulk=False)
            contacts_api_instance.create_contact(contact)
            user.brevo_last_update_date = today
            user.save()
        except Exception as e:
            logger.exception(f"Error creating/updating an individual Brevo user {e}", stack_info=True)
        time.sleep(0.1)  # API rate limit is 10 req per second
