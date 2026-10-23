from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """注册序列化器"""

    password = serializers.CharField(write_only=True, min_length=6, max_length=128)
    confirm_password = serializers.CharField(write_only=True, min_length=6, max_length=128)

    class Meta:
        model = User
        fields = ["id", "username", "nickname", "phone", "password", "confirm_password"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "两次输入的密码不一致"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        nickname = validated_data.pop("nickname", "") or validated_data.get("username", "")
        user = User(**validated_data, nickname=nickname)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""

    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "nickname", "phone", "avatar", "avatar_url", "email", "date_joined"]
        read_only_fields = ["id", "date_joined"]

    def get_avatar_url(self, obj):
        request = self.context.get("request")
        if obj.avatar and hasattr(obj.avatar, "url"):
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return ""


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户资料修改序列化器"""

    class Meta:
        model = User
        fields = ["nickname", "phone", "avatar", "email"]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


def get_tokens_for_user(user):
    """生成 JWT token 对"""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
