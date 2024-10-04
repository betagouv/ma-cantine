import factory

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Teledeclaration


class TeledeclarationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teledeclaration

    year = factory.Faker("year")
    canteen = factory.SubFactory(CanteenFactory)
    diagnostic = factory.SubFactory(DiagnosticFactory)
    applicant = factory.SubFactory(UserFactory)
    status = Teledeclaration.TeledeclarationStatus.SUBMITTED
    declared_data = {"foo": 1}
