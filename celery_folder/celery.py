from celery import Celery

import settings

app = Celery('tasks', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND, include=['celery_folder.tasks'])


if __name__ == '__main__':
    app.start()
#
# client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# client.conf.update(app.config)