

from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import fields
import enum
from app import db, ma


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tasks = tasks = db.relationship('Task', backref='usuario', lazy=True)

    def hashear_clave(self):
        '''
        Hashea la clave en la base de datos
        '''
        self.password = generate_password_hash(self.password, 'sha256')

    def verificar_clave(self, clave):
        '''
        Verifica la clave hasheada con la del parámetro
        '''
        return check_password_hash(self.password, clave)

class Status(enum.Enum):
   UPLOADED = 1
   PROCESSED = 2
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idFile = db.Column(db.Integer, db.ForeignKey('file.id'))
    status = db.Column(db.Enum(Status))
    uploadTime = db.Column(db.TIMESTAMP)
    userId = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    file = db.relationship('File')

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String)
    originalFormat = db.Column(db.String)
    newFormat = db.Column(db.String)
    task = db.relationship('Task', back_populates='file')

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}
    
    
class TaskSchema(ma.Schema):
    status = EnumADiccionario(attribute=("status"))
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
        include_fk = True
        
    id = fields.Integer()
    idFile = fields.Integer()
    uploadTime = fields.DateTime()
    userId = fields.Integer()

