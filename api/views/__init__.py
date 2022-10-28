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
    SendCanteenNotFoundEmail,
    UserCanteenPreviews,
    CanteenStatisticsView,
    CanteenLocationsView,
    TeamJoinRequestView,
    ClaimCanteenView,
    SatelliteListCreateView,
    CanteenActionsView,
    CanteenSummaryView,
)
from .diagnostic import (  # noqa: F401
    DiagnosticCreateView,
    DiagnosticUpdateView,
    EmailDiagnosticImportFileView,
)
from .diagnosticimport import (  # noqa: F401
    ImportSimpleDiagnosticsView,
    ImportCompleteDiagnosticsView,
)
from .sector import SectorListView  # noqa: F401
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
    ImportPurchasesView,
)
from .reservationexpe import ReservationExpeView  # noqa: F401
from .vegetarianexpe import VegetarianExpeView  # noqa: F401
from .message import MessageCreateView  # noqa: F401
from .review import ReviewView  # noqa: F401
from .communityevent import CommunityEventsView  # noqa: F401
from .partner import PartnersView, PartnerView  # noqa: F401
