from flask import Flask
from .extensions import db, login_manager, mail, migrate, bootstrap
from .auth import auth_bp
from .main import main_bp
from .ai import ai_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py', silent=True)

    # Инициализация на разширения
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    # Регистриране на Blueprint-и
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(ai_bp)

    return app
