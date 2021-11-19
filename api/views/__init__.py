from .user import LoggedUserView, UpdateUserView, ChangePasswordView  # noqa: F401
from .canteen import (  # noqa: F401
    PublishedCanteensView,
    PublishedCanteenSingleView,
    UserCanteensView,
    UpdateUserCanteenView,
    AddManagerView,
    RemoveManagerView,
    SendCanteenEmailView,
    PublishCanteenView,
    UnpublishCanteenView,
    SendCanteenNotFoundEmail,
    UserCanteenPreviews,
)
from .diagnostic import (  # noqa: F401
    DiagnosticCreateView,
    DiagnosticUpdateView,
    ImportDiagnosticsView,
)
from .sector import SectorListView  # noqa: F401
from .blog import BlogPostsView, BlogPostView  # noqa: F401
from .subscription import SubscribeBetaTester, SubscribeNewsletter  # noqa: F401
from .teledeclaration import (  # noqa: F401
    TeledeclarationCreateView,
    TeledeclarationCancelView,
    TeledeclarationPdfView,
)
