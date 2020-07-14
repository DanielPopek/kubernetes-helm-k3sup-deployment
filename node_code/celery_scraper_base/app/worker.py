"""Scheduler."""
import os
from celery import Celery

app = Celery(include=('scrapping_task', 'time_log_task', 'embedding_task',
                      'mongo_task'))
app.conf.beat_schedule = {
    'scrap_tweets_of_user': {
        'task': 'scrap_tweets_of_user',
        'schedule': float(os.environ['SCRAP_SCHEDULE']),
        'args': (os.environ['SCRAP_LOCATION'], 300)
    },
    'log_time': {
        'task': 'time_task',
        'schedule': 20.0,
    },
}
