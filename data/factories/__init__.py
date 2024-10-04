# isort: skip_file

import factory  # noqa

factory.Faker._DEFAULT_LOCALE = "fr-fr"  # noqa

from .user import UserFactory  # noqa
from .canteen import CanteenFactory  # noqa
from .diagnostic import CompleteDiagnosticFactory, DiagnosticFactory  # noqa
from .wastemeasurement import WasteMeasurementFactory  # noqa
from .sector import SectorFactory  # noqa
from .blogpost import BlogPostFactory  # noqa
from .blogtag import BlogTagFactory  # noqa
from .managerinvitation import ManagerInvitationFactory  # noqa
from .teledeclaration import TeledeclarationFactory  # noqa
from .purchase import PurchaseFactory  # noqa
from .reservationexpe import ReservationExpeFactory  # noqa
from .vegetarianexpe import VegetarianExpeFactory  # noqa
from .message import MessageFactory  # noqa
from .review import ReviewFactory  # noqa
from .communityevent import CommunityEventFactory  # noqa
from .partner import PartnerFactory  # noqa
from .partnertype import PartnerTypeFactory  # noqa
from .videotutorial import VideoTutorialFactory  # noqa
from .importfailure import ImportFailureFactory  # noqa
from .wasteaction import WasteActionFactory  # noqa
