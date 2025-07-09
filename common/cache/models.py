from django.db import models


class Cache(models.Model):
    """
    https://docs.djangoproject.com/fr/4.2/topics/cache/#database-caching
    """

    cache_key = models.CharField(primary_key=True, max_length=255)
    value = models.TextField()  # pickled data
    expires = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "cache"
