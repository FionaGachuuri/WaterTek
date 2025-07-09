import os
from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.models.base_model import Base
from app.models import storage
from flask_jwt_extended import JWTManager, get_jwt_identity
from app.models.user import User


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
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False



    # Initialize JWT Manager
    jwt = JWTManager(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Context processor to make current_user available in templates
    @app.context_processor
    def inject_user():
        try:
            user_id = get_jwt_identity()
            if user_id:
                current_user = storage.get(User, user_id)
                return {'current_user': current_user}
        except:
            pass
        return {'current_user': None}

    # Register Blueprints
    from app.web_flask.routes import main_bp
    app.register_blueprint(main_bp)

    from app.web_flask.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.web_flask.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from app.web_flask.routes.billing import billing_bp
    app.register_blueprint(billing_bp, url_prefix="/billing")

    from app.web_flask.routes.user import user_bp
    app.register_blueprint(user_bp, url_prefix="/user")

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        # Log the error for debugging
        app.logger.error(f"Unhandled exception: {str(error)}")
        return render_template('errors/500.html'), 500

    return app