import os
from dotenv import load_dotenv

load_dotenv()
OUR_HOST=os.getenv("DB_HOST", "34.41.67.239")
OUR_DB=os.getenv("DB_DB", "conversion_db")
OUR_USER=os.getenv("DB_USER", "admin_db")
OUR_PORT=os.getenv("DB_PORT", "5432")
OUR_PW=os.getenv("DB_PW", "admin_conversion_tool_db")
OUR_SECRET=os.getenv("SECRET", "conversiontooldb")
OUR_JWTSECRET=os.getenv("JWTSECRET", "conversiontooldb")

DEBUG = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(OUR_USER, OUR_PW, OUR_HOST, OUR_PORT, OUR_DB)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = OUR_JWTSECRET
SECRET_KEY = OUR_SECRET
PROPAGATE_EXCEPTIONS = True

GCP_PROJECT_ID = "mystical-ship-403002"
GCP_TOPIC_ID = "topic-cct"