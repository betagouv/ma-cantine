import factory
from data.models import VideoTutorial


class VideoTutorialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VideoTutorial
