from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import DeploymentConfig
from flask_login import LoginManager

#initialisation
db = SQLAlchemy()
login = LoginManager()

def create_app(config=DeploymentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    from app.blueprints import main
    app.register_blueprint(main)
    db.init_app(app)
    login.init_app(app)
    login.login_view = 'main.login'

    return app

from app import models
