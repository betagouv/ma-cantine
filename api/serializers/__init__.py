# isort: skip_file

from .user import LoggedUserSerializer, UserInfoSerializer  # noqa: F401
from .canteen import (  # noqa: F401
    PublicCanteenSerializer,
    PublicCanteenPreviewSerializer,
    FullCanteenSerializer,
    ManagingTeamSerializer,
    CanteenPreviewSerializer,
    SatelliteCanteenSerializer,
    CanteenActionsSerializer,
    CanteenActionsLightSerializer,
    CanteenStatusSerializer,
    CanteenTeledeclarationSerializer,
    SatelliteTeledeclarationSerializer,
    ElectedCanteenSerializer,
    MinimalCanteenSerializer,
    CanteenSummarySerializer,
    CanteenAnalysisSerializer,
    CanteenOpenDataSerializer,
    CanteenMinistriesSerializer,
)
from .diagnostic import (  # noqa: F401
    ManagerDiagnosticSerializer,
    PublicDiagnosticSerializer,
    FullDiagnosticSerializer,
    ApproDiagnosticSerializer,
    CentralKitchenDiagnosticSerializer,
    SimpleTeledeclarationDiagnosticSerializer,
    CompleteTeledeclarationDiagnosticSerializer,
    ApproDeferredTeledeclarationDiagnosticSerializer,
    SimpleApproOnlyTeledeclarationDiagnosticSerializer,
    CompleteApproOnlyTeledeclarationDiagnosticSerializer,
    DiagnosticAndCanteenSerializer,
    PublicApproDiagnosticSerializer,
    PublicServiceDiagnosticSerializer,
)
from .diagnostic_teledeclaration import (  # noqa: F401
    DiagnosticTeledeclaredAnalysisSerializer,
    DiagnosticTeledeclaredOpenDataSerializer,
)
from .wastemeasurement import WasteMeasurementSerializer  # noqa: F401
from .sector import SectorM2MSerializer  # noqa: F401
from .partnertype import PartnerTypeSerializer  # noqa: F401
from .blogpost import BlogPostSerializer  # noqa: F401
from .password import PasswordSerializer  # noqa: F401
from .managerinvitation import ManagerInvitationSerializer  # noqa: F401
from .teledeclaration import (  # noqa: F401
    CampaignDatesSerializer,
    CampaignDatesFullSerializer,
)
from .purchase import (  # noqa: F401
    PurchaseSerializer,
    PurchaseSummarySerializer,
    PurchasePercentageSummarySerializer,
    PurchaseExportSerializer,
)
from .reservationexpe import ReservationExpeSerializer  # noqa: F401
from .vegetarianexpe import VegetarianExpeSerializer  # noqa: F401
from .message import MessageSerializer  # noqa: F401
from .review import ReviewSerializer  # noqa: F401
from .communityevent import CommunityEventSerializer  # noqa: F401
from .partner import PartnerSerializer, PartnerShortSerializer, PartnerContactSerializer  # noqa: F401
from .videotutorial import VideoTutorialSerializer  # noqa: F401
from .wasteaction import WasteActionSerializer, WasteActionWithActionsSerializer  # noqa: F401
from .resourceaction import ResourceActionSerializer, ResourceActionFullSerializer  # noqa: F401
from .statistics import CanteenStatisticsSerializer  # noqa: F401
