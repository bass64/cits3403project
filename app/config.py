#get current working directory
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    #initialisation
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'DKSqdnkNDSKndfkSNDKdn2k34i24i3297ruewioru3ewi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DeploymentConfig(Config):
    #initialisation
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

class TestConfig:
    #initialisation
    SQLALCHEMY_DATABASE_URI = 'sqlite:///"memory'
    TESTING = True