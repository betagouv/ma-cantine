from rest_framework.generics import ListAPIView

from api.serializers import VideoTutorialSerializer
from data.models import VideoTutorial


class VideoTutorialListView(ListAPIView):
    model = VideoTutorial
    serializer_class = VideoTutorialSerializer
    queryset = VideoTutorial.objects.filter(published=True)
