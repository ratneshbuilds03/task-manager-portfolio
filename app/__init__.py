import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy.exc import OperationalError

from app.config import Config
from app.utils.error_handlers import register_error_handlers


db = SQLAlchemy()
jwt = JWTManager()


def _create_tables_with_retry(max_retries=30, delay=2):
    for attempt in range(1, max_retries + 1):
        try:
            db.create_all()
            print("✅ Database tables created successfully")
            return
        except OperationalError as exc:
            message = str(exc).lower()
            if "can't connect to mysql server" not in message and "connection refused" not in message:
                raise
            if attempt == max_retries:
                print("⚠️  Could not connect to database. Make sure DATABASE_URL is set in environment variables.")
                print("   For Render: Add DATABASE_URL environment variable and redeploy.")
                return
            time.sleep(delay)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = Config.resolve_database_url()
    secret_key = app.config.get("JWT_SECRET_KEY")
    if not isinstance(secret_key, str) or len(secret_key.encode("utf-8")) < 32:
        raise RuntimeError("JWT_SECRET_KEY must contain at least 32 bytes")

    db.init_app(app)
    jwt.init_app(app)

    @jwt.unauthorized_loader
    def handle_missing_token(_reason):
        return {"error": "Authentication required"}, 401

    @jwt.invalid_token_loader
    def handle_invalid_token(_reason):
        return {"error": "Invalid authentication token"}, 401

    @jwt.expired_token_loader
    def handle_expired_token(_jwt_header, _jwt_payload):
        return {"error": "Authentication token has expired"}, 401

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    register_error_handlers(app)

    from app.routes.task_routes import task_bp
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(task_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')

    with app.app_context():
        from app.models.task import Task
        from app.models.user import User
        _create_tables_with_retry()

    return app
