from flask import Flask
from flask_jwt_extended import JWTManager

from app.auth.routes import auth_bp
from app.config.db import db
from app.config.settings import settings
from app.strategies.routes import strategy_bp

jwt = JWTManager()


def create_app() -> Flask:
    """
    Initializes the Flask application, configures the database and JWT secret keys, initializes extensions, registers blueprints, and sets up the database.

    :return:
        Flask: The initialized Flask application instance.
    """
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = settings.sqlalchemy__database_url
    app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix=settings.auth_prefix)
    app.register_blueprint(strategy_bp, url_prefix=settings.strategies_prefix)

    # init db
    with app.app_context():
        db.drop_all()
        db.create_all()

    return app
