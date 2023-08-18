from .user import (  # noqa: F401
    LoggedUserView,
    UpdateUserView,
    ChangePasswordView,
    UsernameSuggestionView,
    UserInfoView,
)
from .canteen import (  # noqa: F401
    PublishedCanteensView,
    PublishedCanteenSingleView,
    UserCanteensView,
    RetrieveUpdateUserCanteenView,
    AddManagerView,
    RemoveManagerView,
    PublishCanteenView,
    UnpublishCanteenView,
    PublishManyCanteensView,
    SendCanteenNotFoundEmail,
    UserCanteenPreviews,
    CanteenStatisticsView,
    CanteenLocationsView,
    TeamJoinRequestView,
    ClaimCanteenView,
    UndoClaimCanteenView,
    SatelliteListCreateView,
    ActionableCanteensListView,
    ActionableCanteenRetrieveView,
    CanteenStatusView,
    TerritoryCanteensListView,
)
from .diagnostic import (  # noqa: F401
    DiagnosticCreateView,
    DiagnosticUpdateView,
    EmailDiagnosticImportFileView,
    DiagnosticsToTeledeclareListView,
)
from .diagnosticimport import (  # noqa: F401
    ImportSimpleDiagnosticsView,
    ImportCompleteDiagnosticsView,
    ImportSimpleCentralKitchenView,
    ImportCompleteCentralKitchenView,
)
from .sector import SectorListView  # noqa: F401
from .partnertype import PartnerTypeListView  # noqa: F401
from .blog import BlogPostsView, BlogPostView  # noqa: F401
from .subscription import SubscribeNewsletter  # noqa: F401
from .teledeclaration import (  # noqa: F401
    TeledeclarationCreateView,
    TeledeclarationCancelView,
    TeledeclarationPdfView,
)
from .inquiry import InquiryView  # noqa: F401
from .purchase import (  # noqa: F401
    PurchaseListCreateView,
    PurchaseRetrieveUpdateDestroyView,
    CanteenPurchasesSummaryView,
    PurchaseListExportView,
    PurchaseOptionsView,
    PurchasesDeleteView,
    PurchasesRestoreView,
    DiagnosticsFromPurchasesView,
)
from .purchaseimport import ImportPurchasesView  # noqa: F401
from .reservationexpe import ReservationExpeView  # noqa: F401
from .vegetarianexpe import VegetarianExpeView  # noqa: F401
from .message import MessageCreateView  # noqa: F401
from .review import ReviewView  # noqa: F401
from .communityevent import CommunityEventsView  # noqa: F401
from .partner import PartnersView, PartnerView  # noqa: F401
from .videotutorial import VideoTutorialListView  # noqa: F401
from .initial import InitialDataView  # noqa: F401
