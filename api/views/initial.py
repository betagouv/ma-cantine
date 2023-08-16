from api.views import LoggedUserView, SectorListView, PartnerTypeListView, CommunityEventsView, VideoTutorialListView
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status


class InitialDataView(APIView):
    def get(self, request, *args, **kwargs):
        json_content = {
            "loggedUser": LoggedUserView.as_view()(request._request).data,
            "sectors": SectorListView.as_view()(request._request).data,
            "partnerTypes": PartnerTypeListView.as_view()(request._request).data,
            "communityEvents": CommunityEventsView.as_view()(request._request).data,
            "videoTutorials": VideoTutorialListView.as_view()(request._request).data,
        }
        return JsonResponse(json_content, status=status.HTTP_200_OK)
