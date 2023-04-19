import os
import time
from celery import Celery
from celery import shared_task
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_api.settings.base')

app = Celery('quiz_api')
app.conf.broker_url = 'redis://localhost:6379/0'
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     print("setup", crontab)
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'))

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'RRRRequest: {self.request!r}')

print("in_SELERY")
@shared_task
def add(x, y):
    print("処理中")
    z = x + y
    print("処理完了",z)
    # return z

@app.task
def test(arg):
    print("test_executeed")
    print('test',arg)

@shared_task
def hello():
    print('SSSHA!')

# add.delay(2,4)

@app.task()
def user_test_reset():
    from user.models import User
    print("RESET_USER TEST_TAKzEN")
    users = User.objects.get(username='sasuke')
    print(users)
    users.test_taken = False
    users.save()
