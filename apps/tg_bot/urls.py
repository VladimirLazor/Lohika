from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from config.settings import TG_WEB_HOOK_URL
from .views import tg_web_hook

urlpatterns = [
    path(TG_WEB_HOOK_URL, csrf_exempt(tg_web_hook)),
]
