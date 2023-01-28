import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsAndCommentsProject.settings')

app = Celery('NewsAndCommentsProject')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mails':{
        'task': 'news.tasks.send_week_mails',
        'schedule': crontab(day_of_week='monday', hour='8'),
    },
}
