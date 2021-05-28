import factory  # noqa

factory.Faker._DEFAULT_LOCALE = "fr-fr"  # noqa

from .user import UserFactory  # noqa
from .canteen import CanteenFactory  # noqa
from .diagnosis import DiagnosisFactory  # noqa
from .sector import SectorFactory  # noqa
from .blogpost import BlogPostFactory  # noqa
