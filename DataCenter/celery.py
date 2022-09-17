# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery_once import QueueOnce
from .settings import celery_broker_url

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataCenter.settings')

app = Celery('DataCenter')

app.config_from_object('django.conf.settings', namespace='CELERY')
app.conf.ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': celery_broker_url,
        'default_timeout': 60 * 60,
     }
}
# app.conf.result_expires = 7776000
app.conf.result_expires = 86400     # 保留1天日志
# app.conf.result_expires = 172800  # 保留2天日志
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
