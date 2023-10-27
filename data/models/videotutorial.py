from django.db import models
from data.fields import ChoiceArrayField


class VideoTutorialCategory(models.TextChoices):
    TECHNICAL = "technical", "Technique"
    TRANSITION = "transition", "Transition alimentaire"
    PROFILE = "profile", "Je suis..."


class VideoTutorial(models.Model):
    class Meta:
        verbose_name = "tutoriel vidéo"
        verbose_name_plural = "tutoriels vidéo"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    title = models.TextField(verbose_name="titre")
    description = models.TextField(verbose_name="description")
    published = models.BooleanField(default=False, verbose_name="publié")
    video = models.FileField(verbose_name="vidéo", upload_to="videos/")
    subtitles = models.FileField(null=True, blank=True, verbose_name="sous-titres", upload_to="subtitles/")
    categories = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=VideoTutorialCategory.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="catégorie",
    )
    thumbnail = models.ImageField(null=True, blank=True, verbose_name="aperçu")

    def __str__(self):
        return self.title

    @property
    def sous_titré(self):
        return "✅ oui" if self.subtitles else "❌ non"
