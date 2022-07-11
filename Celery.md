# Celery

The reason why I use Celery is that I want to communicate with LabVIEW server periodically to get latest data. As a result I chose Celery to run periodic tasks in the background.

Since Celery 4.x, Windows is no longer supported. Thus, the version I use is Celery:3.1.25 and the broker is rabbitmq:3.7.3. 

NOTE : There is  solution to run Celery on Windows. <a href='https://stackoverflow.com/questions/37255548/how-to-run-celery-on-windows'>stackoverflow : How to run celery on windows?</a>

---

These are the setting steps

In *proj.model1.celery.py*
I write the broker here, instead of creating a celery.py at *\main*
```python
# celery v3.1.25
from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'model1.settings')

from django.conf import settings  # noqa

app = Celery('model1', broker='amqp://celery:password123@rabbitmq:5672/my_vhost')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
```

In *proj.model1.__init__.py*
```python
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
```

Then, the tasks are created in *proj.main.tasks.py*
```python
from __future__ import absolute_import, unicode_literals
from celery import shared_task

...

@shared_task
def update_dev_sec():
#   1. using TCP/IP(socket module) to communicate with LabVIEW server.
#   2. save to database
...

@shared_task
def delete_dev_min():
        TaskResult.objects.all().delete()
        return 'Delete all results successfully !!!'
```

The last is in */settings.py*. Periodic tasks are running by celery beat. 
```python
# CELERY SETTINGS
CELERY_TIMEZONE="Asia/Taipei"
 
CELERYBEAT_SCHEDULE = {
#   or CELERY_BEAT_SCHEDULE = {} 
    'update_devices_five_seconds':{
        'task': 'main.tasks.update_dev_sec',
        'schedule': 5,
    },
    'delete_devices_min':{
        'task': 'main.tasks.delete_dev_min',
        'schedule' : 600,
    },           
}

```

In the end, when we have to start beat, worker shall be start as well. If not in Docker, two cmd or powershell shall be opened.

One is for worker :

`> celery -A model1 worker -l info`

The other is for beat :

`> celery -A model1 beat -l info`