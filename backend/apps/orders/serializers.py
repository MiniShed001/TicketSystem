from django.utils import timezone
from rest_framework import serializers

from apps.events.models import Session, TicketType
from apps.events.serializers import SessionSerializer

from .models import Order


class OrderCreateSerializer(serializers.Serializer):
    """下单参数校验"""

    session_id = serializers.IntegerField()
    ticket_type_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, max_value=10)
    remark = serializers.CharField(max_length=255, required=False, allow_blank=True, default="")

    def validate(self, attrs):
        try:
            session = Session.objects.select_related("event").get(id=attrs["session_id"])
        except Session.DoesNotExist:
            raise serializers.ValidationError({"session_id": "场次不存在"})
        if session.status != "open":
            raise serializers.ValidationError({"session_id": "该场次不可售票"})
        try:
            ticket_type = TicketType.objects.select_for_update().get(
                id=attrs["ticket_type_id"], session=session
            )
        except TicketType.DoesNotExist:
            raise serializers.ValidationError({"ticket_type_id": "票档不存在"})
        if ticket_type.remain_count < attrs["quantity"]:
            raise serializers.ValidationError({"quantity": f"余票不足，仅剩 {ticket_type.remain_count} 张"})
        attrs["session"] = session
        attrs["ticket_type"] = ticket_type
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器"""

    event_title = serializers.CharField(read_only=True)
    session_name = serializers.CharField(read_only=True)
    ticket_type_name = serializers.CharField(read_only=True)
    unit_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    session_start_time = serializers.DateTimeField(source="session.start_time", read_only=True)
    venue = serializers.CharField(source="session.event.venue", read_only=True)
    city = serializers.CharField(source="session.event.city", read_only=True)
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id", "order_no", "event_title", "session_name", "ticket_type_name",
            "quantity", "unit_price", "amount", "status", "status_display",
            "ticket_code", "remark", "session_start_time", "venue", "city",
            "cover_url", "created_at", "paid_at", "used_at",
        ]

    def get_cover_url(self, obj):
        request = self.context.get("request")
        cover = obj.session.event.cover
        if cover and hasattr(cover, "url"):
            return request.build_absolute_uri(cover.url) if request else cover.url
        return ""


class OrderDetailSerializer(OrderSerializer):
    """订单详情：附加场次完整信息"""

    session = SessionSerializer(read_only=True)

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ["session"]
