from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id", "order_no", "user", "session", "ticket_type", "quantity",
        "amount", "status", "ticket_code", "created_at",
    ]
    list_filter = ["status", "created_at"]
    search_fields = ["order_no", "user__username", "ticket_code", "session__event__title"]
    readonly_fields = ["order_no", "created_at", "paid_at", "used_at"]
