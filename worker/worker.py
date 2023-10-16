import logging
from celery import Celery

celery_app = Celery("process_task_converter", broker='redis://redis:6379/0')

@celery_app.task(name='convert_process')
def convert_process(username):

    logging.info("PROCESSING TASK FOR USER {username}")
