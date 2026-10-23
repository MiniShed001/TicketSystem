from django.contrib import admin

from .models import Event, Session, TicketType


class SessionInline(admin.TabularInline):
    model = Session
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "category", "city", "venue", "status", "is_hot", "start_time"]
    list_filter = ["category", "status", "city"]
    search_fields = ["title", "venue"]
    list_editable = ["status", "is_hot"]
    inlines = [SessionInline]


class TicketTypeInline(admin.TabularInline):
    model = TicketType
    extra = 0


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["id", "event", "name", "start_time", "status"]
    list_filter = ["status"]
    search_fields = ["event__title", "name"]
    inlines = [TicketTypeInline]


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "session", "name", "price", "total_count", "sold_count", "remain_count"]
    search_fields = ["name", "session__event__title"]
