from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, ManagerInvitation, Canteen


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
            Canteen.objects.filter(central_producer_siret=obj.siret).update(central_producer_siret=instance.siret)
    except sender.DoesNotExist:
        pass  # Object is new
