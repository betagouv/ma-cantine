import factory  # noqa

factory.Faker._DEFAULT_LOCALE = "fr-fr"  # noqa

from .blogpost import BlogPostFactory  # noqa
from .blogtag import BlogTagFactory  # noqa
from .canteen import CanteenFactory  # noqa
from .communityevent import CommunityEventFactory  # noqa
from .diagnostic import CompleteDiagnosticFactory, DiagnosticFactory  # noqa
from .importfailure import ImportFailureFactory  # noqa
from .managerinvitation import ManagerInvitationFactory  # noqa
from .message import MessageFactory  # noqa
from .partner import PartnerFactory  # noqa
from .partnertype import PartnerTypeFactory  # noqa
from .purchase import PurchaseFactory  # noqa
from .reservationexpe import ReservationExpeFactory  # noqa
from .review import ReviewFactory  # noqa
from .sector import SectorFactory  # noqa
from .teledeclaration import TeledeclarationFactory  # noqa
from .user import UserFactory  # noqa
from .vegetarianexpe import VegetarianExpeFactory  # noqa
from .videotutorial import VideoTutorialFactory  # noqa
from .wasteaction import WasteActionFactory  # noqa
from .wastemeasurement import WasteMeasurementFactory  # noqa
