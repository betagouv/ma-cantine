from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import LoggedUserView, SubscribeBetaTester, SubscribeNewsletter
from api.views import UpdateUserView, PublishedCanteensView, UserCanteensView
from api.views import DiagnosticCreateView, UpdateUserCanteenView, DiagnosticUpdateView
from api.views import BlogPostsView, SectorListView
from api.views import AddManagerView, ManagerInvitationsView


urlpatterns = {
    path("loggedUser/", LoggedUserView.as_view(), name="logged_user"),
    path("user/<int:pk>", UpdateUserView.as_view(), name="update_user"),
    path(
        "publishedCanteens/", PublishedCanteensView.as_view(), name="published_canteens"
    ),
    path("canteens/", UserCanteensView.as_view(), name="user_canteens"),
    path("canteens/<int:pk>", UpdateUserCanteenView.as_view(), name="single_canteen"),
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
    path("sectors/", SectorListView.as_view(), name="sectors_list"),
    path("blogPosts/", BlogPostsView.as_view(), name="blog_posts_list"),
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
    path(
        "managerInvitations/<int:canteen_pk>",
        ManagerInvitationsView.as_view(),
        name="manager_invitations",
    ),
    path(
        "addManager/<int:canteen_pk>",
        AddManagerView.as_view(),
        name="add_manager",
    ),
}

urlpatterns = format_suffix_patterns(urlpatterns)
