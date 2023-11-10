import logging
import shutil
from celery import Celery
from moviepy.editor import VideoFileClip
import os
import psycopg2
from config import SQLALCHEMY_DATABASE_URI
from google.cloud import storage


celery_app = Celery("process_task_converter", broker='redis://redis:6379/0')

def convertir_video(fileName, newFormat, task_id, user_id):
    try:
        codec_dic = {"avi":"rawvideo","mp4":"libx264","webm":"libvpx","mpeg":"mpeg2video","wmv":"wmv2"}

        input_dir, input_filename = os.path.split(fileName)
        print("input dir {}".format(input_dir))
              
        # Copiar el archivo
        file_name_extension = os.path.splitext(input_filename)[1]
        file_name_original = os.path.splitext(input_filename)[0] + f'_{task_id}' + f'_{user_id}' + f'{file_name_extension}'
        
        shutil.copyfile(fileName, "/app/files/original/"+file_name_original)

        output_filename = os.path.splitext(input_filename)[0]+ f'_{task_id}' + f'_{user_id}' + f'.{newFormat}'
        output_video_path = os.path.join("/app/files/converted/", output_filename) 
        
        print("output path{}".format(output_video_path))
        
        video = VideoFileClip(fileName)
        video.write_videofile(output_video_path, codec=codec_dic[newFormat])
        
        #####################
        CLOUD_STORAGE_BUCKET = "cloud-conversion-tool-bucket-g8"
        
        # Create a Cloud Storage client.
        gcs = storage.Client()

        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

        # Create a new blob and upload the file's content.
        blob = bucket.blob("files/converted/"+output_filename)
        blob.upload_from_filename(output_video_path)
        
        # Make the blob public. 
        #blob.make_public()
        
        os.remove(output_video_path)

        new_status = "PROCESSED"
        update_task_status(task_id,new_status,output_video_path)
        
        return f'Conversión exitosa. El video se ha guardado en {output_video_path} - {blob.public_url}'
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
def convert_process(task_id, fileName, newFormat, user_id):
    logging.info("PROCESSING TASK WITH ID "+ str(task_id))
    conversion_status = convertir_video(fileName,newFormat,task_id,user_id)
    logging.info(conversion_status)
    
    

