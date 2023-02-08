from .user import LoggedUserSerializer, UserInfoSerializer  # noqa: F401
from .canteen import (  # noqa: F401
    PublicCanteenSerializer,
    FullCanteenSerializer,
    ManagingTeamSerializer,
    CanteenPreviewSerializer,
    SatelliteCanteenSerializer,
    CanteenActionsSerializer,
    CanteenStatusSerializer,
    CanteenTeledeclarationSerializer,
    SatelliteTeledeclarationSerializer,
)
from .diagnostic import (  # noqa: F401
    PublicDiagnosticSerializer,
    FullDiagnosticSerializer,
    CentralKitchenDiagnosticSerializer,
    SimpleTeledeclarationDiagnosticSerializer,
    CompleteTeledeclarationDiagnosticSerializer,
    ApproDeferredTeledeclarationDiagnosticSerializer,
    SimpleApproOnlyTeledeclarationDiagnosticSerializer,
    CompleteApproOnlyTeledeclarationDiagnosticSerializer,
)
from .sector import SectorSerializer  # noqa: F401
from .blogpost import BlogPostSerializer  # noqa: F401
from .password import PasswordSerializer  # noqa: F401
from .managerinvitation import ManagerInvitationSerializer  # noqa: F401
from .teledeclaration import ShortTeledeclarationSerializer  # noqa: F401
from .purchase import PurchaseSerializer, PurchaseSummarySerializer, PurchaseExportSerializer  # noqa: F401
from .reservationexpe import ReservationExpeSerializer  # noqa: F401
from .vegetarianexpe import VegetarianExpeSerializer  # noqa: F401
from .message import MessageSerializer  # noqa: F401
from .review import ReviewSerializer  # noqa: F401
from .communityevent import CommunityEventSerializer  # noqa: F401
from .partner import PartnerSerializer, PartnerShortSerializer  # noqa: F401
