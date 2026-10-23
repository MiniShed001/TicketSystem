from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User
from .serializers import (
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
    get_tokens_for_user,
)


class UserRegisterView(generics.CreateAPIView):
    """用户注册，注册成功后直接返回 token 实现自动登录"""

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response(
            {
                "code": 0,
                "message": "注册成功",
                "data": {
                    "user": UserSerializer(user, context={"request": request}).data,
                    "tokens": tokens,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class UserInfoView(generics.RetrieveUpdateAPIView):
    """获取 / 修改当前登录用户信息"""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return UserUpdateSerializer
        return UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response({"code": 0, "message": "ok", "data": serializer.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        result = UserSerializer(instance, context={"request": request}).data
        return Response({"code": 0, "message": "修改成功", "data": result})


class LoginView(TokenObtainPairView):
    """登录：账号密码换取 JWT（返回统一格式）"""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(
                {"code": 1, "message": "用户名或密码错误"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        data = serializer.validated_data
        user = serializer.user
        return Response(
            {
                "code": 0,
                "message": "登录成功",
                "data": {
                    "user": UserSerializer(user, context={"request": request}).data,
                    "tokens": {
                        "refresh": data["refresh"],
                        "access": data["access"],
                    },
                },
            }
        )


class TokenRefreshAPIView(TokenRefreshView):
    """刷新 token"""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "code": 0,
                "message": "ok",
                "data": {"access": serializer.validated_data["access"]},
            }
        )
