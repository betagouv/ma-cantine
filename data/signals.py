from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, ProvisionalManager


@receiver(post_save, sender=User)
def update_canteen_managers(sender, instance, created, **kwargs):
    if created:
        canteen_links = ProvisionalManager.objects.filter(email=instance.email)
        for link in canteen_links:
            link.canteen.managers.add(instance)
            link.delete()

