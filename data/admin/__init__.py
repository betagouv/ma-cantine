from .user import UserAdmin  # noqa
from .canteen import CanteenAdmin  # noqa
from .diagnostic import DiagnosticAdmin  # noqa
from .sector import Sector  # noqa
from .blogpost import BlogPost  # noqa
from .blogtag import BlogTag  # noqa
from .managerinvitation import ManagerInvitation  # noqa
from .teledeclaration import TeledeclarationAdmin  # noqa
from .reservationexpe import ReservationExpeAdmin  # noqa
from .vegetarianexpe import VegetarianExpeAdmin  # noqa
from .message import MessageAdmin  # noqa
from .purchase import PurchaseAdmin  # noqa
from .review import ReviewAdmin  # noqa
from .communityevent import CommunityEventAdmin  # noqa
from .partner import Partner  # noqa: F401
from .partnertype import PartnerType  # noqa: F401
from .videotutorial import VideoTutorial  # noqa: F401

from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)
