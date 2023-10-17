from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__, instance_relative_config=True)

# Configuración de la aplicación desde el archivo config.py
try:
    app.config.from_pyfile('./instance/config.py')
except FileNotFoundError:
    print("ERROR FILENOTFOUND")
    #pass

# Extensiones
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
api = Api(app)
cors = CORS(app)

# Importación de módulos
import modelos.modelos
import vistas.vistas
import router.router

# Crear las tablas de la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
