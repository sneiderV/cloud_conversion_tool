import logging
import shutil
import base64
from moviepy.editor import VideoFileClip
import os
import psycopg2
from config import SQLALCHEMY_DATABASE_URI, GCP_CLOUD_STORAGE_BUCKET
from google.cloud import storage
from flask import Flask
from flask import request

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def subirVideoOriginalBucket(file_name):
    try:    
        # Create a Cloud Storage client.
        gcs = storage.Client()

        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(GCP_CLOUD_STORAGE_BUCKET)

        # Create a new blob and upload the file's content.
        blob = bucket.blob("files/original/"+file_name)
        blob.upload_from_filename("/app/files/base/video1.mp4")
    except Exception as e:
        logging.error(f'Error en subirVideoOriginalBucket: {str(e)}')

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

@app.route("/",methods=['POST'])
def recived():
    req = request.get_json()
    print(str(req))
    m_encode = req['message']['data']
    decoded_message = base64.b64decode(m_encode).decode('utf-8')
    print(f"Received message decode: {decoded_message}")
    params = decoded_message.split(",")
    conversion_status = convertir_video(params[1], params[2], params[0], params[3])
    logging.info(conversion_status)
    return f"Received: {req}!"

@app.route("/",methods=['GET'])
def ping():
    return "Worker Pong!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))