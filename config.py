# config.py
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = "b'\xdd\xa7\xdb\xb9/\x84Ev\x07\xb0f\t?XZvC\xa8\xa3I\x8bR\x86m6y\xff\xa4l\x056}\xb9\xe4\x13\x85\x93\xc7\xed\x95\x94\xddl\x0e[\x90\x9dU\x13\xd7\xed\xacX\x93tO\x15tB\x8b\x16\xe1Zg'"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Production and dev configs use the same database URI
class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ix:AwesomePassword1234@postgres:5432/postgres'
    SQLALCHEMY_ECHO = True

    
class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ix:AwesomePassword1234@postgres:5432/postgres'
    SQLALCHEMY_ECHO = False

