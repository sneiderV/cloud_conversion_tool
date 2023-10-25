from app import api
from vistas import VistaSignIn, VistaLogIn, VistaTasks, VistaTask, VistaPing

api.add_resource(VistaSignIn, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')
api.add_resource(VistaPing, '/api/ping')