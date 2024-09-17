from django.contrib import admin
from django.contrib.auth.models import Group

from .blogpost import BlogPost  # noqa
from .blogtag import BlogTag  # noqa
from .canteen import CanteenAdmin  # noqa
from .communityevent import CommunityEventAdmin  # noqa
from .diagnostic import DiagnosticAdmin  # noqa
from .importfailure import ImportFailureAdmin  # noqa: F401
from .managerinvitation import ManagerInvitation  # noqa
from .message import MessageAdmin  # noqa
from .partner import Partner  # noqa: F401
from .partnertype import PartnerType  # noqa: F401
from .purchase import PurchaseAdmin  # noqa
from .reservationexpe import ReservationExpeAdmin  # noqa
from .review import ReviewAdmin  # noqa
from .sector import Sector  # noqa
from .teledeclaration import TeledeclarationAdmin  # noqa
from .user import UserAdmin  # noqa
from .vegetarianexpe import VegetarianExpeAdmin  # noqa
from .videotutorial import VideoTutorial  # noqa: F401
from .wasteaction import WasteActionAdmin  # noqa: F401
from .wastemeasurement import WasteMeasurementAdmin  # noqa

admin.site.unregister(Group)
