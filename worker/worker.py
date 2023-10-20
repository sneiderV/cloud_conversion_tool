import logging
from celery import Celery
from moviepy.editor import VideoFileClip
import os
import psycopg2
from config import SQLALCHEMY_DATABASE_URI


celery_app = Celery("process_task_converter", broker='redis://redis:6379/0')
#celery_app = Celery("process_task_converter", broker='redis://localhost:6379/0')

def convertir_video(fileName,newFormat,task_id):
    try:
        codec_dic = {"avi":"rawvideo","mp4":"libx264","webm":"libvpx","mpeg":"mpeg2video","wmv":"wmv2"}

        input_dir, input_filename = os.path.split(fileName)
        print("input dir {}".format(input_dir))
        output_filename = os.path.splitext(input_filename)[0] + f'.{newFormat}'

        output_video_path = os.path.join(input_dir, output_filename) 
        print("output path{}".format(output_video_path))
        video = VideoFileClip(fileName)
        video.write_videofile(output_video_path, codec=codec_dic[newFormat])
        newStatus = "PROCESSED"
        update = update_task_status(task_id,newStatus,output_video_path)
        logging.info(update)
        
        return f'Conversión exitosa. El video se ha guardado en {output_video_path}'
    except Exception as e:
        return f'Error al convertir el video: {str(e)}'

def update_task_status(task_id, new_status,output_video_path):
    try:
        connection = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
        cursor = connection.cursor()
        cursor.execute("UPDATE task SET status = '{}' WHERE id='{}'".format(new_status, task_id))
        cursor.execute("UPDATE task SET url = '{}' WHERE id='{}'".format(output_video_path, task_id))
        connection.commit()
        connection.close()
        return "Se actualizo el estado de la tarea a {}".format(new_status)
    except Exception as e:
        return f'Error al actualizar el status: {str(e)}'




@celery_app.task(name='convert_process')
def convert_process(task_id,fileName,newFormat):
    logging.info("PROCESSING TASK WITH ID "+ str(task_id))
    conversion_status = convertir_video(fileName,newFormat,task_id)
    logging.info(conversion_status)
    
    

