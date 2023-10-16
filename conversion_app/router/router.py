from app import api
from vistas import VistaSignIn, VistaLogIn

api.add_resource(VistaSignIn, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
