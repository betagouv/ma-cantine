import logging
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from api.serializers import BlogPostSerializer
from data.models import BlogPost

logger = logging.getLogger(__name__)


class BlogPostsPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 30


class BlogPostsView(ListAPIView):
    model = BlogPost
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.filter(published=True)
    pagination_class = BlogPostsPagination


class BlogPostView(RetrieveAPIView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer
