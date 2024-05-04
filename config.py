#get current working directory
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    #initialisation
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'DKSqdnkNDSKndfkSNDKdn2k34i24i3297ruewioru3ewi'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False