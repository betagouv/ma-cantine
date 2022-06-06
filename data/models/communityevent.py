from django.utils import timezone
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class CommunityEvent(models.Model):
    class Meta:
        verbose_name = "événement"
        ordering = ["date"]

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    title = models.TextField(verbose_name="titre")
    date = models.DateField(default=timezone.now, verbose_name="date de l'événement")
    description = RichTextUploadingField(null=True, blank=True, verbose_name="description")
    link = models.TextField(null=True, blank=True, verbose_name="lien")
