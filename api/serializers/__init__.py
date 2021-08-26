from .user import LoggedUserSerializer  # noqa: F401
from .canteen import (  # noqa: F401
    PublicCanteenSerializer,
    FullCanteenSerializer,
    ManagingTeamSerializer,
)
from .diagnostic import (  # noqa: F401
    PublicDiagnosticSerializer,
    FullDiagnosticSerializer,
)
from .sector import SectorSerializer  # noqa: F401
from .blogpost import BlogPostSerializer  # noqa: F401
from .password import PasswordSerializer  # noqa: F401
from .managerinvitation import ManagerInvitationSerializer  # noqa: F401
from .teledeclaration import ShortTeledeclarationSerializer  # noqa: F401
