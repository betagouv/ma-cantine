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

from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)
