import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.models.base_model import Base
from app.models import storage


load_dotenv()

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app():
    app = Flask(__name__,
                template_folder="web_flask/templates",
                static_folder="web_flask/static")

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    # from app.web_flask.routes.auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix="/auth")

    # from app.web_flask.routes.admin import admin as admin_blueprint
    # app.register_blueprint(admin_blueprint, url_prefix="/admin")

    # from app.web_flask.routes.billing import billing as billing_blueprint
    # app.register_blueprint(billing_blueprint, url_prefix="/billing")

    # from app.web_flask.routes.dashboard import dashboard as dashboard_blueprint
    # app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")

    # from app.web_flask.routes.issues import issues as issues_blueprint
    # app.register_blueprint(issues_blueprint, url_prefix="/issues")


    return app