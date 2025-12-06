import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boiler_analysis.settings')

app = Celery('boiler_analysis')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()