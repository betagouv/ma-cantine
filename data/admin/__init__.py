from .user import UserAdmin  # noqa
from .canteen import CanteenAdmin  # noqa
from .diagnostic import DiagnosticAdmin  # noqa
from .sector import Sector  # noqa
from .blogpost import BlogPost  # noqa
from .provisionalmanager import ProvisionalManager  # noqa

from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

admin.site.site_header = "Ma Cantine EGALIM"
admin.site.index_title = ""
admin.site.site_title = "Ma Cantine EGALIM"
