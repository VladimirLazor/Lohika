import os

from celery import Celery

from .settings import CeleryConfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('Bot')
app.config_from_object(CeleryConfig)
app.autodiscover_tasks()
