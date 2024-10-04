import json

from django.http import JsonResponse
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework import status
from rest_framework.views import APIView


class InitialDataView(APIView):
    def get(self, request, *args, **kwargs):
        from api.views import (
            CanteenMinistriesView,
            CommunityEventsView,
            LoggedUserView,
            PartnerTypeListView,
            SectorListView,
            UserCanteenPreviews,
            VideoTutorialListView,
        )

        is_authenticated = request.user.is_authenticated
        json_content = {
            "logged_user": LoggedUserView.as_view()(request._request).data,
            "sectors": SectorListView.as_view()(request._request).data,
            "partner_types": PartnerTypeListView.as_view()(request._request).data,
            "community_events": CommunityEventsView.as_view()(request._request).data,
            "video_tutorials": VideoTutorialListView.as_view()(request._request).data,
            "canteen_previews": UserCanteenPreviews.as_view()(request._request).data if is_authenticated else None,
            "line_ministries": CanteenMinistriesView.as_view()(request._request).data,
        }
        payload = json.loads(CamelCaseJSONRenderer().render(json_content))
        return JsonResponse(payload, status=status.HTTP_200_OK)
