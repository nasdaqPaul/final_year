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

from app.blueprints.web_app.models import initialize_database, Staff, School, Department, StaffAccount, Announcement, Event
from app.blueprints.mobile.models import Student, StudentAccount, AppInstance
app.register_blueprint(web)
app.register_blueprint(mobile)


@app.shell_context_processor
def make_shell_context():
    return dict(init_db=initialize_database,
                Student=Student,
                StudentAccount=StudentAccount,
                AppInstance=AppInstance,
                StaffAccount=StaffAccount,
                Staff=Staff,
                Department=Department,
                School=School,
                Announcement=Announcement,
                Event=Event)
# Literally hav no shit to do...
#
