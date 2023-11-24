
OUR_HOST="34.41.67.239"
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

GCP_CLOUD_STORAGE_BUCKET = "cloud-conversion-tool-bucket-g8"
GCP_PROJECT_ID = "mystical-ship-403002"
GCP_SUB_TOPIC_ID = "topic-cct-sub"