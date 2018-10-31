import os
from celery import Celery 

os.environ.setdefault('DJANGO_SETTINGS_MODULE','currentaffairs.settings')

app =\
Celery('currentaffairs',backend='redis://localhost',broker='amqp://')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()

