from collections import OrderedDict
import logging
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from api.serializers import BlogPostSerializer
from data.models import BlogPost
from django_filters import rest_framework as django_filters
from .utils import UnaccentSearchFilter

logger = logging.getLogger(__name__)


class BlogPostsPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 30
    tags = []

    def paginate_queryset(self, queryset, request, view=None):
        self.tags = BlogPost.objects.filter(published=True).values_list("tags__name", flat=True)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("results", data),
                    ("tags", self.tags),
                ]
            )
        )


class BlogPostsView(ListAPIView):
    model = BlogPost
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.filter(published=True)
    pagination_class = BlogPostsPagination

    filter_backends = [django_filters.DjangoFilterBackend, UnaccentSearchFilter]
    search_fields = ["title", "tagline", "body"]

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
