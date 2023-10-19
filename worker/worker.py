import logging
import os
from celery import Celery

celery_app = Celery("process_task_converter", broker='redis://redis:6379/0')

@celery_app.task(name='convert_process')
def convert_process(username):

    file = open("/app/files/hola.txt", "w")
    file.write("Primera línea" + os.linesep)
    file.write("Segunda línea")
    
    logging.info("OS CWD -> "+os.getcwd())

    logging.info("PROCESSING TASK FOR USER "+username)
