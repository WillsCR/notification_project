from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
    

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_project.settings')

app = Celery('notification_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.worker_pool = 'solo'

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')