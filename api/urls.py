from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import (
    InquiryView,
    LoggedUserView,
    SubscribeBetaTester,
    SubscribeNewsletter,
    PurchaseListCreateView,
    PurchaseRetrieveUpdateDestroyView,
    CanteenPurchasesSummaryView,
    UsernameSuggestionView,
)
from api.views import UpdateUserView, PublishedCanteensView, UserCanteensView, CanteenStatisticsView
from api.views import DiagnosticCreateView, RetrieveUpdateUserCanteenView, DiagnosticUpdateView
from api.views import EmailDiagnosticImportFileView
from api.views import BlogPostsView, SectorListView, ChangePasswordView, BlogPostView
from api.views import AddManagerView, RemoveManagerView, PublishedCanteenSingleView
from api.views import ImportDiagnosticsView, TeledeclarationCreateView
from api.views import TeledeclarationCancelView, TeledeclarationPdfView
from api.views import PublishCanteenView, UnpublishCanteenView, SendCanteenNotFoundEmail
from api.views import UserCanteenPreviews, CanteenLocationsView
from api.views import ReservationExpeView, PurchaseListExportView, PurchaseOptionsView
from api.views import MessageCreateView, VegetarianExpeView, TeamJoinRequestView
from api.views import ReviewView
from api.views import CommunityEventsView


urlpatterns = {
    path("loggedUser/", LoggedUserView.as_view(), name="logged_user"),
    path("user/<int:pk>", UpdateUserView.as_view(), name="update_user"),
    path("publishedCanteens/", PublishedCanteensView.as_view(), name="published_canteens"),
    path(
        "publishedCanteens/<int:pk>",
        PublishedCanteenSingleView.as_view(),
        name="single_published_canteen",
    ),
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
    path("canteenStatistics/", CanteenStatisticsView.as_view(), name="canteen_statistics"),
    path("sectors/", SectorListView.as_view(), name="sectors_list"),
    path("blogPosts/", BlogPostsView.as_view(), name="blog_posts_list"),
    path("blogPosts/<int:pk>", BlogPostView.as_view(), name="single_blog_post"),
    path(
        "subscribeBetaTester/",
        SubscribeBetaTester.as_view(),
        name="subscribe_beta_tester",
    ),
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
    path("importDiagnostics/", ImportDiagnosticsView.as_view(), name="import_diagnostics"),
    path("emailDiagnosticImportFile/", EmailDiagnosticImportFileView.as_view(), name="email_diagnostic_file"),
    path(
        "createTeledeclaration/",
        TeledeclarationCreateView.as_view(),
        name="teledeclaration_create",
    ),
    path(
        "cancelTeledeclaration/",
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
    path("canteenLocations/", CanteenLocationsView.as_view(), name="canteen_locations"),
    path("canteen/<int:canteen_pk>/reservationExpe/", ReservationExpeView.as_view(), name="canteen_reservation_expe"),
    path("canteen/<int:canteen_pk>/vegetarianExpe/", VegetarianExpeView.as_view(), name="canteen_vegetarian_expe"),
    path("message/", MessageCreateView.as_view(), name="message_create"),
    path("teamJoinRequest/<int:pk>/", TeamJoinRequestView.as_view(), name="canteen_team_request"),
    path("usernameSuggestion/", UsernameSuggestionView.as_view(), name="username_suggestion"),
    path("reviews/", ReviewView.as_view(), name="create_review"),
    path("communityEvents/", CommunityEventsView.as_view(), name="community_event_list"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
