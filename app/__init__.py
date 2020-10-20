from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from firebase_admin import initialize_app

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# setup models
# TODO: find a way to put load models in blueprints
from .web_app import models as web_models
from .web_app.auth import models as web_auth_models
from .web_app.announcements import models as web_announcements_models
from .web_app.activities import models as web_activities_models
from .mobile.auth import models as mobile_auth_models


def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # FCM config
    initialize_app()

    with app.app_context():
        # Import web_app routes
        from .web_app.activities import routes as web_activities_routes
        from .web_app.announcements import routes as web_announcements_routes
        from .web_app.main import routes as web_main_routes
        from .web_app.auth import routes as web_auth_routes
        # Import mobile routes
        from .mobile.auth import routes as mobile_auth_routes
        from .mobile.announcements import routes as mobile_announcements_routes

        # Register Blueprints
        app.register_blueprint(web_activities_routes.web_activities)
        app.register_blueprint(web_announcements_routes.web_announcements)
        app.register_blueprint(web_main_routes.web_main)
        app.register_blueprint(web_auth_routes.web_auth)
        app.register_blueprint(mobile_auth_routes.mobile)
        app.register_blueprint(mobile_announcements_routes.mobile)

        @app.shell_context_processor
        def shell_context():
            return dict(
                        db=db,
                        Student=mobile_auth_models.Student,
                        StudentAccount=mobile_auth_models.StudentAccount,
                        AppInstance=mobile_auth_models.AppInstance,
                        StaffAccount=web_auth_models.StaffAccount,
                        Staff=web_auth_models.Staff,
                        Department=web_models.Department,
                        School=web_models.School,
                        Announcement=web_announcements_models.Announcement,
                        Activity=web_activities_models.Activity)
        return app
