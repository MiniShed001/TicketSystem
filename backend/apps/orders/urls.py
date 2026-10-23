from django.urls import path

from .views import (
    OrderCancelView,
    OrderCreateView,
    OrderDetailView,
    OrderListView,
    OrderPayView,
    VerifyTicketView,
)

urlpatterns = [
    path("", OrderCreateView.as_view(), name="order-create"),
    path("list/", OrderListView.as_view(), name="order-list"),
    path("verify/", VerifyTicketView.as_view(), name="order-verify"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("<int:pk>/pay/", OrderPayView.as_view(), name="order-pay"),
    path("<int:pk>/cancel/", OrderCancelView.as_view(), name="order-cancel"),
]
