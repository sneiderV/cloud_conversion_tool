
OUR_HOST="db"
OUR_DB="conversion_db"
OUR_USER="admin_db"
OUR_PORT="5432"
OUR_PW="admin_conversion_tool_db"
OUR_SECRET="conversiontooldb"
OUR_JWTSECRET="conversiontooldb"

DEBUG = False
SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}:{}/{}'.format(OUR_USER, OUR_PW, OUR_HOST, OUR_PORT, OUR_DB)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = OUR_JWTSECRET
SECRET_KEY = OUR_SECRET
PROPAGATE_EXCEPTIONS = True

CLOUD_STORAGE_BUCKET="cloud-conversion-tool-bucket-g8"