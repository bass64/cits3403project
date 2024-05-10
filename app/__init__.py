from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import DeploymentConfig

#initialisation
db = SQLAlchemy()

def create_app(config=DeploymentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    from app.blueprints import main
    app.register_blueprint(main)

    return app
