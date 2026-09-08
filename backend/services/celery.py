from celery import Celery, Task
from app import app
from celery.schedules import crontab


celery_app = Celery('tasks', broker='redis://localhost:6379/1', backend='redis://localhost:6379/2', include=['services.tasks'])


class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
        

celery_app.Task = FlaskTask   



celery_app.conf.timezone = 'Asia/Kolkata'

celery_app.conf.beat_schedule = {
    'monthly-report': {
        'task': 'services.tasks.monthly_report',
        'schedule': crontab(hour=10, minute=1, day_of_month=1),
    },

    'daily-reminder': {
        'task': 'services.tasks.daily_drive_reminder',
        'schedule': crontab(hour=21, minute=9),
    },
    

    'testing': {
        'task': 'services.tasks.task1',
        'schedule': crontab(hour=20, minute=27),
        # 'schedule': 10,
    }
}