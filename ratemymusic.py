from app import db,create_app
from app.config import DeploymentConfig
from flask_migrate import Migrate
from flask_login import LoginManager

app = create_app(DeploymentConfig)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
