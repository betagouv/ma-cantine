import factory

from data.models import Canteen, Invitation

from .canteen import CanteenFactory
from .user import UserFactory


class InvitationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invitation

    category = Invitation.Category.ADD_SATELLITE
    creation_canteen = factory.SubFactory(CanteenFactory, production_type=Canteen.ProductionType.GROUPE)
    creation_user = factory.SubFactory(UserFactory)
    invited_canteen = factory.SubFactory(CanteenFactory, production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
