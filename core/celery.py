# common.celery.py


"""
Configuration celery
# https://pypi.org/project/celery/
# https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#using-celery-with-django
"""

import os
from django.conf import settings

from celery import Celery

# Set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# You can add the following property when instantiating
# The execution result is put into redis and discarded if
# no one takes it for an hour

app.conf.update(result_expires=3600)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
