from collections import OrderedDict
import logging
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from api.serializers import BlogPostSerializer
from data.models import BlogPost
from django.contrib.postgres.search import SearchQuery, SearchVector

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

    def get_queryset(self):
        queryset = self.queryset
        tag = self.request.query_params.get("tag", None)
        if tag is not None:
            queryset = queryset.filter(tags__name=tag)
        search = self.request.query_params.get("search", None)
        if search is not None:
            queryset = queryset.annotate(
                search=SearchVector("title", "tagline", "body"),
            ).filter(search=SearchQuery(search))
        return queryset


class BlogPostView(RetrieveAPIView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer
