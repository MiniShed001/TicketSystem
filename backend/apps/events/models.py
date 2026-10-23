from django.db import models


class Event(models.Model):
    """活动 / 演出（演唱会、话剧、展览、电影等）"""

    CATEGORY_CHOICES = [
        ("concert", "演唱会"),
        ("drama", "话剧"),
        ("exhibition", "展览"),
        ("movie", "电影"),
        ("sports", "体育"),
        ("other", "其他"),
    ]

    STATUS_CHOICES = [
        ("on", "上架"),
        ("off", "下架"),
    ]

    title = models.CharField("活动名称", max_length=128)
    category = models.CharField("分类", max_length=20, choices=CATEGORY_CHOICES, default="concert")
    cover = models.ImageField("封面图", upload_to="covers/", null=True, blank=True)
    description = models.TextField("活动介绍", blank=True, default="")
    venue = models.CharField("场馆", max_length=128, blank=True, default="")
    city = models.CharField("城市", max_length=64, blank=True, default="")
    address = models.CharField("详细地址", max_length=255, blank=True, default="")
    start_time = models.DateTimeField("开始时间", null=True, blank=True)
    end_time = models.DateTimeField("结束时间", null=True, blank=True)
    status = models.CharField("状态", max_length=10, choices=STATUS_CHOICES, default="on")
    is_hot = models.BooleanField("热门推荐", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "活动"
        verbose_name_plural = verbose_name
        ordering = ["-id"]

    def __str__(self):
        return self.title

    @property
    def cover_url(self):
        if self.cover and hasattr(self.cover, "url"):
            return self.cover.url
        return ""


class Session(models.Model):
    """场次：一个活动可有多个场次（不同日期/时间）"""

    STATUS_CHOICES = [
        ("open", "售票中"),
        ("soldout", "已售罄"),
        ("closed", "已结束"),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="sessions", verbose_name="活动")
    name = models.CharField("场次名称", max_length=64, default="")
    start_time = models.DateTimeField("场次开始时间")
    end_time = models.DateTimeField("场次结束时间", null=True, blank=True)
    status = models.CharField("状态", max_length=10, choices=STATUS_CHOICES, default="open")

    class Meta:
        verbose_name = "场次"
        verbose_name_plural = verbose_name
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.event.title} - {self.name}"


class TicketType(models.Model):
    """票档：一场次下的票价分级（VIP / 一等座 / 二等座）"""

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="ticket_types", verbose_name="场次")
    name = models.CharField("票档名称", max_length=64)
    price = models.DecimalField("价格(元)", max_digits=10, decimal_places=2)
    total_count = models.IntegerField("总票数", default=0)
    sold_count = models.IntegerField("已售数量", default=0)
    description = models.CharField("说明", max_length=255, blank=True, default="")

    class Meta:
        verbose_name = "票档"
        verbose_name_plural = verbose_name
        ordering = ["price"]

    def __str__(self):
        return f"{self.session.name} - {self.name}"

    @property
    def remain_count(self):
        """剩余票数"""
        return max(self.total_count - self.sold_count, 0)
