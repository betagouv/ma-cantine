from .blog import BlogPostsView, BlogPostView  # noqa: F401
from .canteen import (  # noqa: F401
    ActionableCanteenRetrieveView,
    ActionableCanteensListView,
    AddManagerView,
    CanteenMinistriesView,
    CanteenStatusBySirenView,
    CanteenStatusBySiretView,
    ClaimCanteenView,
    PublicCanteenPreviewView,
    PublishedCanteenSingleView,
    PublishedCanteensView,
    RemoveManagerView,
    RetrieveUpdateUserCanteenView,
    SendCanteenNotFoundEmail,
    TeamJoinRequestView,
    TerritoryCanteensListView,
    UndoClaimCanteenView,
    UserCanteenActions,
    UserCanteenPreviews,
    UserCanteenSummaries,
    UserCanteensView,
)
from .canteen_export import UserCanteenListExportView  # noqa: F401
from .canteen_groupe import (  # noqa: F401
    CanteenGroupeSatellitesListView,
    CanteenGroupeSatelliteLinkView,
    CanteenGroupeSatelliteUnlinkView,
)  # noqa: F401
from .canteen_import import CanteensImportView  # noqa: F401
from .communityevent import CommunityEventsView  # noqa: F401
from .diagnostic import (  # noqa: F401
    DiagnosticCreateView,
    DiagnosticsToTeledeclareListView,
    DiagnosticUpdateView,
    EmailDiagnosticImportFileView,
)

# from .diagnostic_import_old import (  # noqa: F401
#     ImportCompleteCentralKitchenView,
#     ImportCompleteDiagnosticsView,
#     ImportSimpleCentralKitchenView,
#     ImportSimpleDiagnosticsView,
# )
from .diagnostic_import import DiagnosticsSimpleImportView  # noqa: F401
from .diagnostic_teledeclaration import (  # noqa: F401
    DiagnosticTeledeclarationCancelView,
    DiagnosticTeledeclarationCreateView,
    DiagnosticTeledeclarationPdfView,
)
from .initial import InitialDataView  # noqa: F401
from .inquiry import InquiryView  # noqa: F401
from .message import MessageCreateView  # noqa: F401
from .partner import PartnersView, PartnerView  # noqa: F401
from .partnertype import PartnerTypeListView  # noqa: F401
from .purchase import (  # noqa: F401
    CanteenPurchasesPercentageSummaryView,
    CanteenPurchasesSummaryView,
    DiagnosticsFromPurchasesView,
    PurchaseListCreateView,
    PurchaseListExportView,
    PurchaseOptionsView,
    PurchaseRetrieveUpdateDestroyView,
    PurchasesDeleteView,
    PurchasesRestoreView,
)
from .purchase_import import PurchasesImportView  # noqa: F401
from .reservationexpe import ReservationExpeView  # noqa: F401
from .resourceaction import ResourceActionView  # noqa: F401
from .review import ReviewView  # noqa: F401
from .sector import SectorListView  # noqa: F401
from .statistics import CanteenStatisticsView  # noqa: F401
from .subscription import SubscribeNewsletter  # noqa: F401
from .teledeclaration import (  # noqa: F401
    TeledeclarationCampaignDatesListView,
    TeledeclarationCampaignDatesRetrieveView,
)
from .user import (  # noqa: F401
    ChangePasswordView,
    LoggedUserView,
    UpdateUserView,
    UserInfoView,
    UsernameSuggestionView,
)
from .vegetarianexpe import VegetarianExpeView  # noqa: F401
from .videotutorial import VideoTutorialListView  # noqa: F401
from .wasteaction import WasteActionsView, WasteActionView  # noqa: F401
from .wastemeasurement import (  # noqa: F401
    CanteenWasteMeasurementsView,
    CanteenWasteMeasurementView,
)
