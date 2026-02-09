from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class CommunityEventQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter(end_date__gt=timezone.now())


class CommunityEvent(models.Model):
    class Meta:
        verbose_name = "événement"
        ordering = ["start_date"]

    objects = CommunityEventQuerySet.as_manager()

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    title = models.TextField(verbose_name="titre")
    start_date = models.DateTimeField(verbose_name="date de début")
    end_date = models.DateTimeField(verbose_name="date de fin")
    tagline = models.TextField(null=True, blank=True, verbose_name="description courte")
    link = models.TextField(verbose_name="lien pour s'inscrire")

    def clean(self):
        self.validate_dates()
        return super().clean()

    def validate_dates(self):
        if self.start_date is None or self.end_date is None:
            return
        if self.end_date < self.start_date:
            raise ValidationError({"end_date": "La date de fin ne peut pas être avant la date de début"})
