import random
import string

from django.conf import settings
from django.db import models


def gen_order_no():
    """生成订单号：日期 + 随机数字"""
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"TK{ts}{random.randint(1000, 9999)}"


def gen_ticket_code():
    """生成验票码：8 位字母数字"""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


class Order(models.Model):
    """订单"""

    STATUS_CHOICES = [
        ("pending", "待支付"),
        ("paid", "已支付"),
        ("used", "已使用"),
        ("cancelled", "已取消"),
        ("refunded", "已退款"),
    ]

    order_no = models.CharField("订单号", max_length=32, unique=True, default=gen_order_no)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders", verbose_name="用户"
    )
    session = models.ForeignKey(
        "events.Session", on_delete=models.PROTECT, related_name="orders", verbose_name="场次"
    )
    ticket_type = models.ForeignKey(
        "events.TicketType", on_delete=models.PROTECT, related_name="orders", verbose_name="票档"
    )
    quantity = models.IntegerField("数量", default=1)
    amount = models.DecimalField("订单金额(元)", max_digits=10, decimal_places=2)
    status = models.CharField("状态", max_length=12, choices=STATUS_CHOICES, default="pending")
    ticket_code = models.CharField("验票码", max_length=16, blank=True, default="")
    remark = models.CharField("备注", max_length=255, blank=True, default="")
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    paid_at = models.DateTimeField("支付时间", null=True, blank=True)
    used_at = models.DateTimeField("使用时间", null=True, blank=True)

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name
        ordering = ["-id"]

    def __str__(self):
        return self.order_no

    @property
    def event_title(self):
        return self.session.event.title

    @property
    def session_name(self):
        return self.session.name

    @property
    def ticket_type_name(self):
        return self.ticket_type.name

    @property
    def unit_price(self):
        return self.ticket_type.price
