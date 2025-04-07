from .blog import BlogPostsView, BlogPostView  # noqa: F401
from .canteen import (  # noqa: F401
    ActionableCanteenRetrieveView,
    ActionableCanteensListView,
    AddManagerView,
    CanteenLocationsView,
    CanteenMinistriesView,
    CanteenStatusBySirenView,
    CanteenStatusBySiretView,
    ClaimCanteenView,
    PublicCanteenPreviewView,
    PublishCanteenView,
    PublishedCanteenSingleView,
    PublishedCanteensView,
    PublishManyCanteensView,
    RemoveManagerView,
    RetrieveUpdateUserCanteenView,
    SatelliteListCreateView,
    SendCanteenNotFoundEmail,
    TeamJoinRequestView,
    TerritoryCanteensListView,
    UndoClaimCanteenView,
    UnlinkSatelliteView,
    UnpublishCanteenView,
    UserCanteenPreviews,
    UserCanteenSummaries,
    UserCanteensView,
)
from .canteenimport import ImportCanteensView  # noqa: F401
from .communityevent import CommunityEventsView  # noqa: F401
from .diagnostic import (  # noqa: F401
    DiagnosticCreateView,
    DiagnosticsToTeledeclareListView,
    DiagnosticUpdateView,
    EmailDiagnosticImportFileView,
)
from .diagnosticimport import (  # noqa: F401
    ImportCompleteCentralKitchenView,
    ImportCompleteDiagnosticsView,
    ImportSimpleCentralKitchenView,
    ImportSimpleDiagnosticsView,
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
from .purchaseimport import ImportPurchasesView  # noqa: F401
from .reservationexpe import ReservationExpeView  # noqa: F401
from .resourceaction import ResourceActionView  # noqa: F401
from .review import ReviewView  # noqa: F401
from .sector import SectorListView  # noqa: F401
from .statistics import CanteenStatisticsView  # noqa: F401
from .subscription import SubscribeNewsletter  # noqa: F401
from .teledeclaration import (  # noqa: F401
    TeledeclarationCampaignDatesListView,
    TeledeclarationCampaignDatesRetrieveView,
    TeledeclarationCancelView,
    TeledeclarationCreateView,
    TeledeclarationPdfView,
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
