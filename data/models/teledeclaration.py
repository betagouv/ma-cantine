from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from data.models import Canteen, Diagnostic


class Teledeclaration(models.Model):
    class Meta:
        verbose_name = "télédéclaration"
        verbose_name_plural = "télédéclarations"

    class TeledeclarationStatus(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Télédéclaré"
        CANCELLED = "CANCELLED", "Annulé"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    applicant = models.ForeignKey(
        get_user_model(),
        verbose_name="demandeur",
        on_delete=models.PROTECT,
    )

    year = models.IntegerField(
        verbose_name="année",
    )

    canteen = models.ForeignKey(
        Canteen,
        verbose_name="cantine",
        on_delete=models.PROTECT,
    )

    status = models.CharField(
        max_length=255,
        choices=TeledeclarationStatus.choices,
        verbose_name="status",
    )

    source = models.ForeignKey(
        Diagnostic, verbose_name="diagnostic source", on_delete=models.PROTECT
    )

    def clean(self):
        """
        Verify there is only one submitted declaration per year/canteen
        at any given time.
        """
        if self.status == self.TeledeclarationStatus.SUBMITTED:
            if (
                Teledeclaration.objects.filter(
                    canteen=self.canteen, year=self.year, status=self.status
                ).count()
                > 0
            ):
                raise ValidationError(
                    {
                        "year": "Il existe déjà une télédéclaration en cours pour cette année"
                    }
                )
        return super().clean()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
