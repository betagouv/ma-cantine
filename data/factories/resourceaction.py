import factory

from data.models import ResourceAction


class ResourceActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourceAction
