from django.urls import path

from .views import LoginView, TokenRefreshAPIView, UserInfoView, UserRegisterView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("token/refresh/", TokenRefreshAPIView.as_view(), name="token-refresh"),
    path("me/", UserInfoView.as_view(), name="user-me"),
]
