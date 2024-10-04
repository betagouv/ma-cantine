import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
from simple_history.signals import pre_create_historical_record

from .models import Canteen, ManagerInvitation, User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def update_canteen_managers(sender, instance, created, **kwargs):
    if created:
        canteen_links = ManagerInvitation.objects.filter(email__iexact=instance.email)
        for link in canteen_links:
            link.canteen.managers.add(instance)
            link.delete()


@receiver(pre_save, sender=Canteen)
def update_satellites_siret(sender, instance, raw, using, update_fields, **kwargs):
    if raw or not instance.is_central_cuisine:
        return
    try:
        obj = sender.objects.get(pk=instance.pk)
        if not obj.siret or not instance.siret:
            return
        siret_has_changed = obj.siret != instance.siret
        if siret_has_changed:
            logger.info(
                f"SIRET change. Central kitchen {instance.id} ({instance.name}) changed its SIRET from {obj.siret} to {instance.siret}"
            )
            satellites = Canteen.objects.filter(
                central_producer_siret=obj.siret,
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            ).only("id")
            for satellite in satellites:
                logger.info(
                    f"SIRET change. Satellite cantine {satellite.id} had its central_producer_siret changed automatically from {obj.siret} to {instance.siret}"
                )
            satellites.update(central_producer_siret=instance.siret)

    except sender.DoesNotExist:
        pass  # Object is new


def historical_record_add_auth_method(history_instance):
    if not hasattr(history_instance, "authentication_method"):
        return

    if not hasattr(HistoricalRecords, "context") or not hasattr(HistoricalRecords.context, "request"):
        history_instance.authentication_method = "AUTO"
        return

    metadata = HistoricalRecords.context.request.META

    path_info = metadata["PATH_INFO"]
    path_parts = path_info.split("/")
    path_root = path_parts[1] if len(path_parts) > 1 else path_parts[0]
    if path_root == "admin":
        history_instance.authentication_method = "ADMIN"
        return

    if "HTTP_AUTHORIZATION" in metadata:
        history_instance.authentication_method = "API"
        # save hostname to track usage of specific integrations?
    else:
        history_instance.authentication_method = "WEBSITE"


@receiver(pre_create_historical_record)
def pre_historical_record_save(sender, **kwargs):
    try:
        history_instance = kwargs["history_instance"]
        historical_record_add_auth_method(history_instance)
    except Exception as e:
        logger.error("Error when attempting to set authentication method on a history object", e)
