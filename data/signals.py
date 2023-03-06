import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, ManagerInvitation, Canteen

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
        siret_has_changed = obj.siret != instance.siret
        if siret_has_changed:
            logger.info(
                f"SIRET change. Central kitchen {instance.id} ({instance.name}) changed its SIRET from {obj.siret} to {instance.siret}"
            )
            satellites = Canteen.objects.filter(central_producer_siret=obj.siret).only("id")
            for satellite in satellites:
                logger.info(
                    f"SIRET change. Satellite cantine {satellite.id} had its central_producer_siret changed automatically from {obj.siret} to {instance.siret}"
                )
            satellites.update(central_producer_siret=instance.siret)

    except sender.DoesNotExist:
        pass  # Object is new
