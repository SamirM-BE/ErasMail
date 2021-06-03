import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "erasmail.settings")
app = Celery("erasmail")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()