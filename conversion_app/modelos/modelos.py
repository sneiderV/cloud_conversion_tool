from werkzeug.security import generate_password_hash, check_password_hash
from conversion_app import db, ma

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

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
    
    
'''
Schemas
'''
class UsuarioSchema(ma.Schema):
    '''
    Representa el schema de un admin
    '''
    class Meta:
        fields = ("id", "usuario", "email", "password")
        
        
usuario_schema = UsuarioSchema()