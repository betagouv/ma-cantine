from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import (
    InquiryView,
    LoggedUserView,
    SubscribeBetaTester,
    SubscribeNewsletter,
    SendCanteenEmailView,
    PurchaseListCreateView,
    PurchaseRetrieveUpdateView,
)
from api.views import UpdateUserView, PublishedCanteensView, UserCanteensView, CanteenStatisticsView
from api.views import DiagnosticCreateView, RetrieveUpdateUserCanteenView, DiagnosticUpdateView
from api.views import BlogPostsView, SectorListView, ChangePasswordView, BlogPostView
from api.views import AddManagerView, RemoveManagerView, PublishedCanteenSingleView
from api.views import ImportDiagnosticsView, TeledeclarationCreateView
from api.views import TeledeclarationCancelView, TeledeclarationPdfView
from api.views import PublishCanteenView, UnpublishCanteenView, SendCanteenNotFoundEmail
from api.views import UserCanteenPreviews, CanteenLocationsView


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
    path("contactCanteen/", SendCanteenEmailView.as_view(), name="contact_canteen"),
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
        "purchases/<int:pk>",
        PurchaseRetrieveUpdateView.as_view(),
        name="purchase_retrieve_update",
    ),
    path("canteenLocations/", CanteenLocationsView.as_view(), name="canteen_locations"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
