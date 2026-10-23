from rest_framework import serializers

from .models import Event, Session, TicketType


class TicketTypeSerializer(serializers.ModelSerializer):
    """票档序列化器"""

    remain_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = TicketType
        fields = [
            "id", "name", "price", "total_count", "sold_count", "remain_count", "description",
        ]


class SessionSerializer(serializers.ModelSerializer):
    """场次序列化器（含票档）"""

    ticket_types = TicketTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ["id", "name", "start_time", "end_time", "status", "ticket_types"]


class EventListSerializer(serializers.ModelSerializer):
    """活动列表序列化器"""

    cover_url = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id", "title", "category", "cover_url", "venue", "city",
            "start_time", "is_hot", "min_price",
        ]

    def get_cover_url(self, obj):
        request = self.context.get("request")
        if obj.cover and hasattr(obj.cover, "url"):
            return request.build_absolute_uri(obj.cover.url) if request else obj.cover.url
        return ""

    def get_min_price(self, obj):
        """该活动所有在售票档中的最低价"""
        prices = [
            t.price
            for s in obj.sessions.all()
            for t in s.ticket_types.all()
        ]
        return float(min(prices)) if prices else None


class EventDetailSerializer(serializers.ModelSerializer):
    """活动详情序列化器（含场次与票档）"""

    cover_url = serializers.SerializerMethodField()
    sessions = SessionSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "title", "category", "cover_url", "description",
            "venue", "city", "address", "start_time", "end_time",
            "status", "is_hot", "sessions",
        ]

    def get_cover_url(self, obj):
        request = self.context.get("request")
        if obj.cover and hasattr(obj.cover, "url"):
            return request.build_absolute_uri(obj.cover.url) if request else obj.cover.url
        return ""
