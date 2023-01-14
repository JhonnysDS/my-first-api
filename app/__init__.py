from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import local
db = SQLAlchemy()


def create_app():
    settings_module = local
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}, headers=["Authorization", "Content-Type"])



    # Carga los parámetros de configuración según el entorno
    app.config.from_object(settings_module)

    # Carga la configuración del directorio instance
    if app.config.get('TESTING', False):
        app.config.from_pyfile('config-testing.py', silent=True)
    else:
        app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.app_context().push()

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .comments import comments_bp
    app.register_blueprint(comments_bp)

    from .posts import posts_bp
    app.register_blueprint(posts_bp)

    return app