import factory  # noqa

factory.Faker._DEFAULT_LOCALE = "fr-fr"  # noqa

from .user import UserFactory  # noqa
from .canteen import CanteenFactory  # noqa
from .diagnostic import DiagnosticFactory  # noqa
from .sector import SectorFactory  # noqa
from .blogpost import BlogPostFactory  # noqa
