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

    def get_queryset(self):
        queryset = self.queryset
        tag = self.request.query_params.get("tag", None)
        if tag is not None:
            queryset = queryset.filter(tags__name=tag)
        return queryset


class BlogPostView(RetrieveAPIView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer
