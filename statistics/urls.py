from django.urls import path

from statistics.views import CanteenStatisticsView

urlpatterns = [
    path("canteenStatistics/", CanteenStatisticsView.as_view(), name="canteen_statistics"),
]
