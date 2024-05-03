
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CBV_fb_clone.settings.base")
app = Celery("CBC_fb_clone")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind = True)
def debug_task(self):
    print(f'Request:{self.request!r}' )