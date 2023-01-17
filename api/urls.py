from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import (
    InquiryView,
    LoggedUserView,
    UserInfoView,
    SubscribeNewsletter,
    PurchaseListCreateView,
    PurchaseRetrieveUpdateDestroyView,
    CanteenPurchasesSummaryView,
    UsernameSuggestionView,
)
from api.views import UpdateUserView, UserCanteensView, CanteenStatisticsView
from api.views import PublishedCanteensView, PublishManyCanteensView, PublishedCanteenSingleView
from api.views import DiagnosticCreateView, RetrieveUpdateUserCanteenView, DiagnosticUpdateView
from api.views import EmailDiagnosticImportFileView
from api.views import BlogPostsView, SectorListView, ChangePasswordView, BlogPostView
from api.views import AddManagerView, RemoveManagerView
from api.views import ImportSimpleDiagnosticsView, ImportCompleteDiagnosticsView
from api.views import TeledeclarationCreateView, TeledeclarationCancelView, TeledeclarationPdfView
from api.views import PublishCanteenView, UnpublishCanteenView, SendCanteenNotFoundEmail
from api.views import UserCanteenPreviews, CanteenLocationsView, PartnerView, PartnersView
from api.views import ReservationExpeView, PurchaseListExportView, PurchaseOptionsView, ImportPurchasesView
from api.views import MessageCreateView, VegetarianExpeView, TeamJoinRequestView
from api.views import ReviewView, CommunityEventsView, ClaimCanteenView, SatelliteListCreateView
from api.views import ActionableCanteensListView, ActionableCanteenRetrieveView
from api.views import SiretCheckView


urlpatterns = {
    path("loggedUser/", LoggedUserView.as_view(), name="logged_user"),
    path("userInfo/", UserInfoView.as_view(), name="user_info"),
    path("user/<int:pk>", UpdateUserView.as_view(), name="update_user"),
    path("publishedCanteens/", PublishedCanteensView.as_view(), name="published_canteens"),
    path(
        "publishedCanteens/<int:pk>",
        PublishedCanteenSingleView.as_view(),
        name="single_published_canteen",
    ),
    path("publish/", PublishManyCanteensView.as_view(), name="publish_canteens"),
    path("canteenPreviews/", UserCanteenPreviews.as_view(), name="user_canteen_previews"),
    path("canteens/", UserCanteensView.as_view(), name="user_canteens"),
    path("canteens/<int:pk>", RetrieveUpdateUserCanteenView.as_view(), name="single_canteen"),
    path(
        "canteens/<int:pk>/publish",
        PublishCanteenView.as_view(),
        name="publish_canteen",
    ),
    path(
        "canteens/<int:pk>/unpublish",
        UnpublishCanteenView.as_view(),
        name="unpublish_canteen",
    ),
    path(
        "canteens/<int:canteen_pk>/diagnostics/",
        DiagnosticCreateView.as_view(),
        name="diagnostic_creation",
    ),
    path(
        "canteens/<int:canteen_pk>/diagnostics/<int:pk>",
        DiagnosticUpdateView.as_view(),
        name="diagnostic_edition",
    ),
    path(
        "canteens/<int:canteen_pk>/satellites/",
        SatelliteListCreateView.as_view(),
        name="list_create_update_satellite",
    ),
    path("canteenStatistics/", CanteenStatisticsView.as_view(), name="canteen_statistics"),
    path("sectors/", SectorListView.as_view(), name="sectors_list"),
    path("blogPosts/", BlogPostsView.as_view(), name="blog_posts_list"),
    path("blogPosts/<int:pk>", BlogPostView.as_view(), name="single_blog_post"),
    path("partners/", PartnersView.as_view(), name="partners_list"),
    path("partners/<int:pk>", PartnerView.as_view(), name="single_partner"),
    path(
        "subscribeNewsletter/",
        SubscribeNewsletter.as_view(),
        name="subscribe_newsletter",
    ),
    path("passwordChange/", ChangePasswordView.as_view(), name="change_password"),
    path(
        "addManager/",
        AddManagerView.as_view(),
        name="add_manager",
    ),
    path(
        "canteenNotFoundMessage/",
        SendCanteenNotFoundEmail.as_view(),
        name="canteen_not_found",
    ),
    path(
        "removeManager/",
        RemoveManagerView.as_view(),
        name="remove_manager",
    ),
    path("importDiagnostics/simple/", ImportSimpleDiagnosticsView.as_view(), name="import_diagnostics"),
    path("importDiagnostics/complete/", ImportCompleteDiagnosticsView.as_view(), name="import_complete_diagnostics"),
    path("emailDiagnosticImportFile/", EmailDiagnosticImportFileView.as_view(), name="email_diagnostic_file"),
    path(
        "teledeclaration/",
        TeledeclarationCreateView.as_view(),
        name="teledeclaration_create",
    ),
    path(
        "teledeclaration/<int:pk>/cancel/",
        TeledeclarationCancelView.as_view(),
        name="teledeclaration_cancel",
    ),
    path(
        "teledeclaration/<int:pk>/document.pdf",
        TeledeclarationPdfView.as_view(),
        name="teledeclaration_pdf",
    ),
    path("inquiry/", InquiryView.as_view(), name="inquiry"),
    path(
        "purchases/",
        PurchaseListCreateView.as_view(),
        name="purchase_list_create",
    ),
    path(
        "export-achats.xlsx",  # breaking from URL conventions for nicer filename
        PurchaseListExportView.as_view(),
        name="purchase_list_export",
    ),
    path(
        "purchases/<int:pk>",
        PurchaseRetrieveUpdateDestroyView.as_view(),
        name="purchase_retrieve_update_destroy",
    ),
    path(
        "canteenPurchasesSummary/<int:canteen_pk>",
        CanteenPurchasesSummaryView.as_view(),
        name="canteen_purchases_summary",
    ),
    path("purchaseOptions/", PurchaseOptionsView.as_view(), name="purchase_options"),
    path("importPurchases/", ImportPurchasesView.as_view(), name="import_purchases"),
    path("canteenLocations/", CanteenLocationsView.as_view(), name="canteen_locations"),
    path("canteen/<int:canteen_pk>/reservationExpe/", ReservationExpeView.as_view(), name="canteen_reservation_expe"),
    path("canteen/<int:canteen_pk>/vegetarianExpe/", VegetarianExpeView.as_view(), name="canteen_vegetarian_expe"),
    path("message/", MessageCreateView.as_view(), name="message_create"),
    path("teamJoinRequest/<int:pk>/", TeamJoinRequestView.as_view(), name="canteen_team_request"),
    path("usernameSuggestion/", UsernameSuggestionView.as_view(), name="username_suggestion"),
    path("reviews/", ReviewView.as_view(), name="create_review"),
    path("communityEvents/", CommunityEventsView.as_view(), name="community_event_list"),
    path("canteens/<int:canteen_pk>/claim/", ClaimCanteenView.as_view(), name="claim_canteen"),
    path("actionableCanteens/<int:year>", ActionableCanteensListView.as_view(), name="list_actionable_canteens"),
    path(
        "actionableCanteens/<int:pk>/<int:year>",
        ActionableCanteenRetrieveView.as_view(),
        name="retrieve_actionable_canteen",
    ),
    path("siret/<str:siret>", SiretCheckView.as_view(), name="siret_check"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
