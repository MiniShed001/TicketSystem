from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.events.models import TicketType

from .models import Order, gen_ticket_code
from .serializers import OrderCreateSerializer, OrderDetailSerializer, OrderSerializer


class OrderCreateView(APIView):
    """创建订单：校验库存并扣减票数（事务 + 行锁防超卖）"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        session = data["session"]
        ticket_type = data["ticket_type"]
        quantity = data["quantity"]
        remark = data.get("remark", "")

        with transaction.atomic():
            # 行锁重新锁定票档，防止并发超卖
            locked = TicketType.objects.select_for_update().get(id=ticket_type.id)
            if locked.remain_count < quantity:
                return Response(
                    {"code": 1, "message": f"余票不足，仅剩 {locked.remain_count} 张"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            locked.sold_count += quantity
            locked.save(update_fields=["sold_count"])
            amount = locked.price * Decimal(quantity)
            order = Order.objects.create(
                user=request.user,
                session=session,
                ticket_type=locked,
                quantity=quantity,
                amount=amount,
                remark=remark,
            )
        return Response(
            {
                "code": 0,
                "message": "下单成功",
                "data": OrderDetailSerializer(order, context={"request": request}).data,
            },
            status=status.HTTP_201_CREATED,
        )


class OrderListView(generics.ListAPIView):
    """我的订单列表：可选状态筛选 status=pending/paid/used/cancelled"""

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Order.objects.filter(user=self.request.user).select_related(
            "session__event", "ticket_type"
        )
        status_filter = self.request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"code": 0, "message": "ok", "data": serializer.data})


class OrderDetailView(generics.RetrieveAPIView):
    """订单详情"""

    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("session__event", "ticket_type")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"code": 0, "message": "ok", "data": serializer.data})


class OrderPayView(APIView):
    """模拟支付：支付成功后订单变为已支付并生成验票码"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.select_for_update().get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"code": 1, "message": "订单不存在"}, status=status.HTTP_404_NOT_FOUND)

        if order.status != "pending":
            return Response({"code": 1, "message": "当前订单状态不可支付"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = "paid"
        order.paid_at = timezone.now()
        order.ticket_code = gen_ticket_code()
        order.save(update_fields=["status", "paid_at", "ticket_code"])
        return Response(
            {
                "code": 0,
                "message": "支付成功",
                "data": OrderDetailSerializer(order, context={"request": request}).data,
            }
        )


class OrderCancelView(APIView):
    """取消订单（仅待支付可取消，取消后归还库存）"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        with transaction.atomic():
            try:
                order = Order.objects.select_for_update().get(id=pk, user=request.user)
            except Order.DoesNotExist:
                return Response({"code": 1, "message": "订单不存在"}, status=status.HTTP_404_NOT_FOUND)

            if order.status != "pending":
                return Response(
                    {"code": 1, "message": "仅待支付订单可取消"}, status=status.HTTP_400_BAD_REQUEST
                )

            order.status = "cancelled"
            order.save(update_fields=["status"])
            # 归还库存
            ticket_type = TicketType.objects.select_for_update().get(id=order.ticket_type.id)
            ticket_type.sold_count = max(ticket_type.sold_count - order.quantity, 0)
            ticket_type.save(update_fields=["sold_count"])
        return Response({"code": 0, "message": "订单已取消", "data": {}})


class VerifyTicketView(APIView):
    """验票核销：管理员 / 工作人员凭验票码核销（需要 staff 权限）"""

    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        code = request.data.get("ticket_code", "").strip().upper()
        if not code:
            return Response({"code": 1, "message": "请输入验票码"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.select_for_update().get(ticket_code=code)
        except Order.DoesNotExist:
            return Response({"code": 1, "message": "验票码无效，未找到对应订单"}, status=status.HTTP_404_NOT_FOUND)

        if order.status == "used":
            return Response(
                {"code": 1, "message": f"该票已于 {order.used_at} 使用过，请勿重复核销"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if order.status != "paid":
            return Response(
                {"code": 1, "message": f"订单状态为「{order.get_status_display()}」，不可核销"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = "used"
        order.used_at = timezone.now()
        order.save(update_fields=["status", "used_at"])
        used_at_str = timezone.localtime(order.used_at).strftime("%Y-%m-%d %H:%M:%S") if order.used_at else ""
        return Response(
            {
                "code": 0,
                "message": "核销成功",
                "data": {
                    "order_no": order.order_no,
                    "event_title": order.event_title,
                    "session_name": order.session_name,
                    "ticket_type_name": order.ticket_type_name,
                    "quantity": order.quantity,
                    "used_at": used_at_str,
                },
            }
        )
