import factory
from data.models import BlogPost
from .user import UserFactory


class BlogPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlogPost

    title = factory.Faker("catch_phrase")
    body = factory.Faker("paragraph")
    published = factory.Faker("boolean")
    author = factory.SubFactory(UserFactory)
