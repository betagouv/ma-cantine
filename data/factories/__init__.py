import factory  # noqa

factory.Faker._DEFAULT_LOCALE = "fr-fr"  # noqa

from .user import UserFactory  # noqa
from .canteen import CanteenFactory  # noqa
from .diagnostic import DiagnosticFactory  # noqa
from .sector import SectorFactory  # noqa
from .blogpost import BlogPostFactory  # noqa
from .blogtag import BlogTagFactory  # noqa
from .managerinvitation import ManagerInvitationFactory  # noqa
from .teledeclaration import TeledeclarationFactory  # noqa
from .purchase import PurchaseFactory  # noqa
from .reservationexpe import ReservationExpeFactory  # noqa
from .vegetarianexpe import VegetarianExpeFactory  # noqa
from .message import MessageFactory  # noqa
