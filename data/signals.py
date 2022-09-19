from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, ManagerInvitation


@receiver(post_save, sender=User)
def update_canteen_managers(sender, instance, created, **kwargs):
    if created:
        canteen_links = ManagerInvitation.objects.filter(email__iexact=instance.email)
        for link in canteen_links:
            link.canteen.managers.add(instance)
            link.delete()
