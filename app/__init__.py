from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)

from app.blueprints.web_app.routes import web
from app.blueprints.mobile.routes import mobile

app.register_blueprint(web)
app.register_blueprint(mobile)
