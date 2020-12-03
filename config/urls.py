from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path(settings.ADMIN_PANEL_URL, admin.site.urls),
    path('', include('apps.core.urls')),
    path('', include('apps.tg_bot.urls')),
]
