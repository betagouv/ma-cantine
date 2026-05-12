from django.db import models


class BlogTag(models.Model):
    name = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "étiquette de blog"
        verbose_name_plural = "étiquettes de blog"

    @classmethod
    def choices(self):
        return [(x.id, x.__str__()) for x in self.objects.all()]

    def __str__(self):
        return self.name
