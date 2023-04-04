from celery import Celery

from STINBank import settings

app = Celery(
    'STINBank',
    broker='amqp://localhost',
    backend='rpc://',
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
    app.start()
