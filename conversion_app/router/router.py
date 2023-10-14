from conversion_app import api
from conversion_app.vistas import VistaSignIn, VistaLogIn

api.add_resource(VistaSignIn, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
