from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
import hashlib
import re

from modelos import \
    db, \
    Usuario

def esCorreoElectronico(texto):
    # Definimos una expresión regular para validar direcciones de correo electrónico
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    # Usamos re.match para verificar si el texto coincide con el patrón
    if re.match(patron, texto):
        return True
    else:
        return False


class VistaSignIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"]).first()
        correo_electronico=Usuario.query.filter(Usuario.correo_electronico == request.json["correo_electronico"]).first()
        if (usuario is None) and (correo_electronico is None):
            contrasena_encriptada = hashlib.md5(request.json["contrasena"].encode('utf-8')).hexdigest()
            nuevo_usuario = Usuario(usuario=request.json["usuario"], contrasena=contrasena_encriptada,
                                    correo_electronico=request.json["correo_electronico"])
            db.session.add(nuevo_usuario)
            db.session.commit()
            return {"mensaje": "usuario creado exitosamente", "id": nuevo_usuario.id}
        else:
            return "El usuario o correo ya existe", 404



class VistaLogIn(Resource):

    def post(self):

        data = request.get_json()
        if (not data) or ('usuario' not in data) or ('contrasena' not in data):
            return {'message': 'Correo electrónico/usuario y contraseña son obligatorios'}, 400

        usuario = None
        contrasena_encriptada = hashlib.md5(request.json["contrasena"].encode('utf-8')).hexdigest()

        if esCorreoElectronico(data.get('usuario')):
            usuario = Usuario.query.filter(Usuario.correo_electronico == data["usuario"],
                                       Usuario.contrasena == contrasena_encriptada).first()
        else:
            usuario = Usuario.query.filter(Usuario.usuario == data["usuario"],
                                       Usuario.contrasena == contrasena_encriptada).first()
            
        if usuario is None:
            return "El usuario con las credenciales proporcionadas no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id}

