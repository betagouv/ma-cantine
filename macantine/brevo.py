import logging
import time

import requests
import sib_api_v3_sdk
from django.conf import settings

logger = logging.getLogger(__name__)

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
    dict_attributes = {
        "NOM": user.last_name,
        "PRENOM": user.first_name,
        "NOM_COMPLET": user.get_full_name(),
        "EMAIL": user.email,
        "MA_CANTINE_DATE_INSCRIPTION": user.date_joined.strftime("%Y-%m-%d"),
        "DERNIERE_CONNEXION": user.last_login.strftime("%Y-%m-%d") if user.last_login else "",
        "MA_CANTINE_COMPTE_DEV": user.is_dev,
        "MA_CANTINE_COMPTE_ELU_E": user.is_elected_official,
        "MA_CANTINE_GERE_UN_ETABLISSEMENT": user.has_canteens(),
        "MA_CANTINE_MANQUE_BILAN_DONNEES_2024": user.has_missing_diagnostic_for_year(2024),
        "MA_CANTINE_MANQUE_BILAN_DONNEES_2023": user.has_missing_diagnostic_for_year(2023),
        "MA_CANTINE_MANQUE_BILAN_DONNEES_2022": user.has_missing_diagnostic_for_year(2022),
        "MA_CANTINE_MANQUE_BILAN_DONNEES_2021": user.has_missing_diagnostic_for_year(2021),
        "MA_CANTINE_MANQUE_TD_DONNEES_2024": user.has_missing_teledeclaration_for_year(2024),
        "MA_CANTINE_MANQUE_TD_DONNEES_2023": user.has_missing_teledeclaration_for_year(2023),
        "MA_CANTINE_MANQUE_TD_DONNEES_2022": user.has_missing_teledeclaration_for_year(2022),
        "MA_CANTINE_MANQUE_TD_DONNEES_2021": user.has_missing_teledeclaration_for_year(2021),
    }

    if bulk:
        return sib_api_v3_sdk.UpdateBatchContactsContacts(email=user.email, attributes=dict_attributes)
    return sib_api_v3_sdk.CreateContact(email=user.email, attributes=dict_attributes, update_enabled=True)


def update_existing_brevo_contacts(users_to_update, today):
    for chunk in users_to_update:
        contacts = [user_to_brevo_payload(user) for user in chunk]
        update_object = sib_api_v3_sdk.UpdateBatchContacts(contacts)
        try:
            contacts_api_instance.update_batch_contacts(update_object)
            for user in chunk:
                user.last_brevo_update = today
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
            user.last_brevo_update = today
            user.save()
        except Exception as e:
            logger.exception(f"Error creating/updating an individual Brevo user {e}", stack_info=True)
        time.sleep(0.1)  # API rate limit is 10 req per second
