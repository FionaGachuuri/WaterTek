import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.models.base_model import Base
from app.models import storage
from flask_jwt_extended import JWTManager


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
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


    # Initialize JWT Manager
    jwt = JWTManager(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.web_flask.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.web_flask.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from app.web_flask.routes.billing import billing_bp
    app.register_blueprint(billing_bp, url_prefix="/billing")

    from app.web_flask.routes.user import user_bp
    app.register_blueprint(user_bp, url_prefix="/user")


    return app