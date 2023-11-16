import logging
import shutil
from moviepy.editor import VideoFileClip
import os
import psycopg2
from config import SQLALCHEMY_DATABASE_URI, GCP_CLOUD_STORAGE_BUCKET, GCP_PROJECT_ID, GCP_SUB_TOPIC_ID
from google.cloud import storage, pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(GCP_PROJECT_ID, GCP_SUB_TOPIC_ID)

def subirVideoOriginalBucket(file_name):
        
    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(GCP_CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob("files/original/"+file_name)
    blob.upload_from_filename("/app/files/base/video1.mp4")
    

def subirVideoConvertidoBucket(output_video_path, output_filename):
        
    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(GCP_CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob("files/converted/"+output_filename)
    blob.upload_from_filename(output_video_path)
    
    os.remove(output_video_path)
    
    return blob


def convertir_video(fileName, newFormat, task_id, user_id):
    try:
        codec_dic = {"avi":"rawvideo","mp4":"libx264","webm":"libvpx","mpeg":"mpeg2video","wmv":"wmv2"}

        input_dir, input_filename = os.path.split(fileName)
        print("input dir {}".format(input_dir))
              
        # Extraer nombre archivo original con el formato => nombre_archivo_idtarea_idusuario.extensionoroginal
        file_name_extension = os.path.splitext(input_filename)[1]
        file_name_original = os.path.splitext(input_filename)[0] + f'_{task_id}' + f'_{user_id}' + f'{file_name_extension}'
        
        subirVideoOriginalBucket(file_name_original)
        
        output_filename = os.path.splitext(input_filename)[0]+ f'_{task_id}' + f'_{user_id}' + f'.{newFormat}'
        output_video_path = os.path.join("/app/files/converted/", output_filename) 
        
        video = VideoFileClip(fileName)
        video.write_videofile(output_video_path, codec=codec_dic[newFormat])

        blob = subirVideoConvertidoBucket(output_video_path, output_filename)

        new_status = "PROCESSED"
        update_task_status(task_id,new_status,blob.public_url)
        
        return f'Conversión exitosa. El video se ha guardado en {blob.public_url}'
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

def callback(message):
    message = message.data.decode('utf-8')
    print(f"Received message: {message}")
    # order input: task_id, fileName, newFormat, user_id
    params = message.split(",")
    conversion_status = convertir_video(params[1],params[2],params[0],params[3])
    logging.info(conversion_status)
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...\n")

with subscriber:
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()