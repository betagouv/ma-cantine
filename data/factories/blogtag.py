import factory
from data.models import BlogTag


class BlogTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlogTag

    name = factory.Faker("text", max_nb_chars=20)
