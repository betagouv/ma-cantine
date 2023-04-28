from rest_framework.generics import ListAPIView
from data.models import VideoTutorial
from api.serializers import VideoTutorialSerializer


class VideoTutorialListView(ListAPIView):
    model = VideoTutorial
    serializer_class = VideoTutorialSerializer
    queryset = VideoTutorial.objects.filter(published=True)
