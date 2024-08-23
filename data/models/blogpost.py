from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
from .blogtag import BlogTag
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from django.contrib.contenttypes.fields import GenericRelation
from wagtail.models import RevisionMixin


class BlogPost(RevisionMixin, models.Model):
    class Meta:
        verbose_name = "article de blog"
        verbose_name_plural = "articles de blog"
        ordering = ["-display_date"]

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    title = models.TextField(verbose_name="titre")
    tagline = models.TextField(null=True, blank=True, verbose_name="description courte")
    display_date = models.DateField(default=timezone.now, verbose_name="date affichée")
    body = RichTextUploadingField(null=True, blank=True, verbose_name="contenu")
    published = models.BooleanField(default=False, verbose_name="publié")
    author = models.ForeignKey(
        get_user_model(),
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        verbose_name="auteur",
        related_name="blog_posts",
    )
    # TODO: update to support revisions : https://docs.wagtail.org/en/v6.2.1/topics/snippets/features.html#saving-revisions-of-snippets
    tags = models.ManyToManyField(BlogTag, blank=True, verbose_name="étiquettes")

    # don't use revisions directly, in case custom logic is required in the future
    _revisions = GenericRelation("wagtailcore.Revision", related_query_name="blogpost")

    @property
    def url_path(self):
        return f"/blog/{self.id}"

    def __str__(self):
        return f'Blog post "{self.title}"'

    @property
    def revisions(self):
        # Some custom logic here if necessary
        return self._revisions


class BlogPage(Page):
    body = RichTextUploadingField()
    date = models.DateField("Post date")

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("body"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]
