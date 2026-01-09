from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super().update(deletion_date=timezone.now())

    def hard_delete(self):
        return super().delete()


class SoftDeletionManager(models.Manager):
    queryset_model = SoftDeletionQuerySet

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return self.queryset_model(self.model).filter(deletion_date=None)
        return self.queryset_model(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    deletion_date = models.DateTimeField(blank=True, null=True, verbose_name="Date de suppression par l'utilisateur")
    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deletion_date = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()

    @property
    def is_deleted(self):
        return self.deletion_date is not None
