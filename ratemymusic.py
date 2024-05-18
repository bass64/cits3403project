from app import db, create_app
from app.config import DeploymentConfig
from flask_migrate import Migrate
from app.database import create_database

app = create_app(DeploymentConfig)
migrate = Migrate(app, db)