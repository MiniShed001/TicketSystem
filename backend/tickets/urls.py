"""tickets URL Configuration"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # 业务 API
    path("api/users/", include("apps.users.urls")),
    path("api/events/", include("apps.events.urls")),
    path("api/orders/", include("apps.orders.urls")),
]

# 开发环境提供媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
