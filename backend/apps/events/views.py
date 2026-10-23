from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Event
from .serializers import EventDetailSerializer, EventListSerializer


class EventListView(generics.ListAPIView):
    """活动列表：支持分类 category、关键词 q、热门 hot 筛选"""

    serializer_class = EventListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Event.objects.filter(status="on").prefetch_related("sessions__ticket_types")
        category = self.request.query_params.get("category")
        q = self.request.query_params.get("q")
        hot = self.request.query_params.get("hot")
        if category:
            qs = qs.filter(category=category)
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(venue__icontains=q)
                | Q(city__icontains=q)
                | Q(description__icontains=q)
            )
        if hot == "1":
            qs = qs.filter(is_hot=True)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"code": 0, "message": "ok", "data": serializer.data})


class EventDetailView(generics.RetrieveAPIView):
    """活动详情：含场次与票档"""

    serializer_class = EventDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Event.objects.filter(status="on").prefetch_related("sessions__ticket_types")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"code": 0, "message": "ok", "data": serializer.data})
