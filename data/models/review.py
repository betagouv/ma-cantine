from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    class Meta:
        verbose_name = "évaluation du site"
        verbose_name_plural = "évaluations du site"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="utilisateur")
    rating = models.PositiveSmallIntegerField(
        verbose_name="score",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    suggestion = models.TextField(blank=True, null=True, verbose_name="suggestion")
    page = models.CharField(max_length=100, verbose_name="page")
    hasCanteen = models.BooleanField(default=False, verbose_name="eu une cantine au moment de l'évaluation")
    hasDiagnostic = models.BooleanField(default=False, verbose_name="eu un diagnostic au moment de l'évaluation")
