from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型：在 Django 默认用户基础上扩展手机号、昵称、头像"""

    nickname = models.CharField("昵称", max_length=64, blank=True, default="")
    phone = models.CharField("手机号", max_length=20, unique=True, null=True, blank=True)
    avatar = models.ImageField("头像", upload_to="avatars/", null=True, blank=True)
    created_at = models.DateTimeField("注册时间", auto_now_add=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ["-id"]

    def __str__(self):
        return self.username
