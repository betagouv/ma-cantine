import factory

from data.models import EventLog

from .user import UserFactory


class EventLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventLog

    category = EventLog.Category.IMPORT
    name = "PURCHASE_SIRET"
    status = EventLog.Status.SUCCESS
    user = factory.SubFactory(UserFactory)
    data = factory.LazyFunction(dict)
