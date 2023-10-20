import logging
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
import hashlib
import re
from celery import Celery
import datetime

from app import db
from modelos import Usuario, Task, TaskSchema, File


task_schema = TaskSchema()

celery = Celery(__name__, broker='redis://redis:6379/0')

def esCorreoElectronico(texto):
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

        if esCorreoElectronico(data.get('usuario')):
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
        tareas = Task.query.all()
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
        fileName = request.json["fileName"]
        originalFormat = obtener_formato_archivo(fileName)
        newFormat = request.json["newFormat"]
        status="UPLOADED"
        uploadTime = datetime.datetime.now()
        new_file = File(fileName=fileName,originalFormat=originalFormat,newFormat=newFormat)
        db.session.add(new_file)
        db.session.commit()
        new_task = Task(idFile=new_file.id,status=status,uploadTime=uploadTime,userId=current_user)
        db.session.add(new_task)
        db.session.commit()
        send_task_to_process.apply_async(args=[new_task.id,fileName,newFormat], queue="process_task_converter")

        return "Su transaccion esta en proceso con el task_id: {}".format(new_task.id)

class VistaTask(Resource):
    @jwt_required()
    def get(self, id_task):
        return task_schema.dump(Task.query.get_or_404(id_task))
    
    @jwt_required()
    def delete(self, id_task):
        registro = Task.query.get_or_404(id_task)
        db.session.delete(registro)
        db.session.commit()
        return "Registro eliminado exitosamente"
    
    

            

@celery.task(name="convert_process")
def send_task_to_process(*args):
    logging.info('### Enviando mensaje a la queue')
