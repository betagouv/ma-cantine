import factory
from data.models import Teledeclaration
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory


class TeledeclarationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teledeclaration

    year = factory.Faker("year")
    canteen = factory.SubFactory(CanteenFactory)
    diagnostic = factory.SubFactory(DiagnosticFactory)
    applicant = factory.SubFactory(UserFactory)
