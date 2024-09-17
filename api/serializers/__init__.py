from .blogpost import BlogPostSerializer  # noqa: F401
from .canteen import (  # noqa: F401
    CanteenActionsSerializer,
    CanteenPreviewSerializer,
    CanteenStatusSerializer,
    CanteenSummarySerializer,
    CanteenTeledeclarationSerializer,
    ElectedCanteenSerializer,
    FullCanteenSerializer,
    ManagingTeamSerializer,
    MinimalCanteenSerializer,
    PublicCanteenPreviewSerializer,
    PublicCanteenSerializer,
    SatelliteCanteenSerializer,
    SatelliteTeledeclarationSerializer,
)
from .communityevent import CommunityEventSerializer  # noqa: F401
from .diagnostic import (  # noqa: F401
    ApproDeferredTeledeclarationDiagnosticSerializer,
    ApproDiagnosticSerializer,
    CentralKitchenDiagnosticSerializer,
    CompleteApproOnlyTeledeclarationDiagnosticSerializer,
    CompleteTeledeclarationDiagnosticSerializer,
    DiagnosticAndCanteenSerializer,
    FullDiagnosticSerializer,
    ManagerDiagnosticSerializer,
    PublicApproDiagnosticSerializer,
    PublicDiagnosticSerializer,
    PublicServiceDiagnosticSerializer,
    SimpleApproOnlyTeledeclarationDiagnosticSerializer,
    SimpleTeledeclarationDiagnosticSerializer,
)
from .managerinvitation import ManagerInvitationSerializer  # noqa: F401
from .message import MessageSerializer  # noqa: F401
from .partner import (  # noqa: F401
    PartnerContactSerializer,
    PartnerSerializer,
    PartnerShortSerializer,
)
from .partnertype import PartnerTypeSerializer  # noqa: F401
from .password import PasswordSerializer  # noqa: F401
from .purchase import (  # noqa: F401
    PurchaseExportSerializer,
    PurchasePercentageSummarySerializer,
    PurchaseSerializer,
    PurchaseSummarySerializer,
)
from .reservationexpe import ReservationExpeSerializer  # noqa: F401
from .review import ReviewSerializer  # noqa: F401
from .sector import SectorSerializer  # noqa: F401
from .teledeclaration import ShortTeledeclarationSerializer  # noqa: F401
from .user import LoggedUserSerializer, UserInfoSerializer  # noqa: F401
from .vegetarianexpe import VegetarianExpeSerializer  # noqa: F401
from .videotutorial import VideoTutorialSerializer  # noqa: F401
from .wasteaction import WasteActionSerializer  # noqa: F401
from .wastemeasurement import WasteMeasurementSerializer  # noqa: F401
