from .blogpost import BlogPostSerializer  # noqa: F401
from .canteen import (  # noqa: F401
    CanteenActionsLightSerializer,
    CanteenActionsSerializer,
    CanteenAnalysisSerializer,
    CanteenCheckSerializer,
    CanteenExportSerializer,
    CanteenMinistriesSerializer,
    CanteenOpenDataSerializer,
    CanteenPreviewSerializer,
    CanteenStatusSerializer,
    CanteenSummarySerializer,
    CanteenTeledeclarationSerializer,
    ElectedCanteenSerializer,
    FullCanteenSerializer,
    MinimalCanteenSerializer,
    PublicCanteenPreviewSerializer,
    PublicCanteenSerializer,
    SatelliteCanteenSerializer,
    SatelliteTeledeclarationSerializer,
)
from .canteen_managers import (  # noqa: F401
    CanteenManagerInvitationSerializer,
    CanteenManagerSerializer,
    ManagingTeamSerializer,
)
from .communityevent import CommunityEventSerializer  # noqa: F401
from .diagnostic import (  # noqa: F401
    ApproDeferredTeledeclarationDiagnosticSerializer,
    ApproDiagnosticSerializer,
    CentralKitchenDiagnosticSerializer,
    CompleteApproOnlyTeledeclarationDiagnosticSerializer,
    CompleteTeledeclarationDiagnosticSerializer,
    DiagnosticAndCanteenSerializer,
    DiagnosticCheckSerializer,
    DiagnosticRecapSerializer,
    FullDiagnosticSerializer,
    ManagerDiagnosticSerializer,
    PublicApproDiagnosticSerializer,
    PublicDiagnosticSerializer,
    PublicServiceDiagnosticSerializer,
    SimpleApproOnlyTeledeclarationDiagnosticSerializer,
    SimpleTeledeclarationDiagnosticSerializer,
)
from .diagnostic_teledeclaration import (  # noqa: F401
    DiagnosticTeledeclaredAnalysisSerializer,
    DiagnosticTeledeclaredOpenDataSerializer,
)
from .diagnostic_teledeclaration_dates import (  # noqa: F401
    CampaignDatesFullSerializer,
    CampaignDatesSerializer,
)
from .message import MessageSerializer  # noqa: F401
from .partner import PartnerContactSerializer, PartnerSerializer, PartnerShortSerializer  # noqa: F401
from .partnertype import PartnerTypeSerializer  # noqa: F401
from .password import PasswordSerializer  # noqa: F401
from .purchase import (  # noqa: F401
    PurchaseExportSerializer,
    PurchaseFactureSerializer,
    PurchaseOldSerializer,
    PurchasePercentageSummarySerializer,
    PurchaseSerializer,
    PurchaseSummarySerializer,
)
from .reservationexpe import ReservationExpeSerializer  # noqa: F401
from .resourceaction import ResourceActionFullSerializer, ResourceActionSerializer  # noqa: F401
from .review import ReviewSerializer  # noqa: F401
from .sector import SectorM2MSerializer  # noqa: F401
from .statistics import CanteenStatisticsSerializer  # noqa: F401
from .teledeclaration import ShortTeledeclarationSerializer  # noqa: F401
from .user import LoggedUserSerializer, UserInfoSerializer  # noqa: F401
from .vegetarianexpe import VegetarianExpeSerializer  # noqa: F401
from .videotutorial import VideoTutorialSerializer  # noqa: F401
from .wasteaction import WasteActionSerializer, WasteActionWithActionsSerializer  # noqa: F401
from .wastemeasurement import WasteMeasurementSerializer  # noqa: F401
