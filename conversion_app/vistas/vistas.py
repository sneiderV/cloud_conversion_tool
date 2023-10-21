import logging
import os
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
import hashlib
import re
from celery import Celery
import datetime

from app import db
from modelos import Usuario, Task, TaskSchema, File, Status


task_schema = TaskSchema()

celery = Celery(__name__, broker='redis://redis:6379/0')

def check_email(texto):
    # Definimos una expresión regular para validar direcciones de correo electrónico
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    # Usamos re.match para verificar si el texto coincide con el patrón
    if re.match(patron, texto):
        return True
    else:
        return False
    
def obtener_formato_archivo(ruta_archivo):
        # Utiliza una expresión regular para extraer la extensión del archivo
        formato = re.search(r'\.([a-zA-Z0-9]+)$', ruta_archivo)
        if formato:
            return formato.group(1)
        else:
            return "Desconocido"  # Si no se encuentra una extensión


class VistaSignIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"]).first()
        email=Usuario.query.filter(Usuario.email == request.json["email"]).first()
        if (usuario is None) and (email is None):
            contrasena_encriptada = hashlib.md5(request.json["password"].encode('utf-8')).hexdigest()
            nuevo_usuario = Usuario(usuario=request.json["usuario"], password=contrasena_encriptada,
                                    email=request.json["email"])
            db.session.add(nuevo_usuario)
            db.session.commit()
            return {"mensaje": "usuario creado exitosamente", "id": nuevo_usuario.id}
        else:
            return "El usuario o correo ya existe", 404



class VistaLogIn(Resource):

    def post(self):

        data = request.get_json()
        if (not data) or ('usuario' not in data) or ('password' not in data):
            return {'message': 'Correo electrónico/usuario y contraseña son obligatorios'}, 400

        usuario = None
        contrasena_encriptada = hashlib.md5(request.json["password"].encode('utf-8')).hexdigest()

        if check_email(data.get('usuario')):
            usuario = Usuario.query.filter(Usuario.email == data["usuario"],
                                       Usuario.password == contrasena_encriptada).first()
        else:
            usuario = Usuario.query.filter(Usuario.usuario == data["usuario"],
                                       Usuario.password == contrasena_encriptada).first()
            
        if usuario is None:
            return "El usuario con las credenciales proporcionadas no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id}


class VistaTasks(Resource):

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        tareas = Task.query.filter_by(userId=current_user).all()
        # Aplica parámetros de consulta, si están presentes
        max_param = request.args.get('max', type=int)
        order_param = request.args.get('order', type=int)

        # Verifica si se proporcionó el parámetro 'max' y lo utiliza para limitar la cantidad de registros
        if max_param is not None:
            tareas = tareas[:max_param]
        
        # Verifica si se proporcionó el parámetro 'order' y lo utiliza para ordenar las tareas
        if order_param == 1:
            tareas = sorted(tareas, key=lambda tarea: tarea.uploadTime, reverse=True)
        elif order_param == 0:
            tareas = sorted(tareas, key=lambda tarea: tarea.uploadTime)
            

        return [task_schema.dump(tarea) for tarea in tareas]
    

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        file_name = request.json["fileName"]
        original_format = obtener_formato_archivo(file_name)
        new_format = request.json["newFormat"]
        status="UPLOADED"
        upload_time = datetime.datetime.now()
        new_file = File(fileName=file_name,originalFormat=original_format,newFormat=new_format)
        db.session.add(new_file)
        db.session.commit()
        new_task = Task(idFile=new_file.id,status=status,uploadTime=upload_time,userId=current_user)
        db.session.add(new_task)
        db.session.commit()
        send_task_to_process.apply_async(args=[new_task.id,file_name,new_format,new_task.userId], queue="process_task_converter")

        return "Su transaccion esta en proceso con el task_id: {}".format(new_task.id)

class VistaTask(Resource):
    @jwt_required()
    def get(self, id_task):
        return task_schema.dump(Task.query.get_or_404(id_task))
    
    @jwt_required()
    def delete(self, id_task):
        registro = Task.query.get_or_404(id_task)
        file = File.query.get_or_404(registro.idFile)

        if registro.status == Status.PROCESSED:
            output_filename = os.path.splitext(file.fileName)[0]+ f'_{registro.id}' + f'_{registro.userId}' + f'.{file.newFormat}'
            output_video_path = "/app/files/converted/" + output_filename.split("/")[-1]
            
            if os.path.exists(output_video_path):
                os.remove(output_video_path)
                
            original_filename = os.path.splitext(file.fileName)[0]+ f'_{registro.id}' + f'_{registro.userId}' + f'.{file.originalFormat}'
            original_video_path = "/app/files/original/" + original_filename.split("/")[-1]
            
            if os.path.exists(original_video_path):
                os.remove(original_video_path)

            db.session.delete(registro)
            db.session.delete(file)
            db.session.commit()
            
            return "Registro eliminado exitosamente."
        else:
            return "La tarea no puede ser eliminada. Tarea en proceso."
    
    


@celery.task(name="convert_process")
def send_task_to_process(*args):
    logging.info('### Enviando mensaje a la queue')
