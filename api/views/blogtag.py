import logging
from rest_framework.generics import ListAPIView
from api.serializers import BlogTagSerializer
from data.models import BlogTag

logger = logging.getLogger(__name__)


class BlogTagListView(ListAPIView):
    model = BlogTag
    serializer_class = BlogTagSerializer
    queryset = BlogTag.objects.all()
