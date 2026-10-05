from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Oauth2ProviderApplicationExtra(models.Model):
    """
    Extra fields for the django-oauth-toolkit Application model
    """

    application = models.OneToOneField(
        settings.OAUTH2_PROVIDER_APPLICATION_MODEL,
        on_delete=models.CASCADE,
        related_name="extra",
        verbose_name="Application Oauth2 (API)",
    )
    company_name = models.CharField(max_length=255, blank=True, verbose_name="nom de l'entreprise")

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Application Oauth2 (API) : informations complémentaires"
        verbose_name_plural = "Applications Oauth2 (API) : informations complémentaires"

    def __str__(self):
        return f"{self.application} ({self.company_name})" if self.company_name else str(self.application)


@receiver(post_save, sender=settings.OAUTH2_PROVIDER_APPLICATION_MODEL)
def create_oauth2_provider_application_extra(sender, instance, created, raw=False, **kwargs):
    """
    On application creation, create its (empty) extra
    """
    if created and not raw:
        Oauth2ProviderApplicationExtra.objects.get_or_create(application=instance)
