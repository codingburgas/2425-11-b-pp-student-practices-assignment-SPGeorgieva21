from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from app.extensions import db, login_manager, mail, bootstrap, migrate

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
app.config.from_object('config.Config')

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    migrate.init_app(app, db)

    # Инициализиране на разширения
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Задаване на login изгледа
    login_manager.login_view = 'auth.login'

    # Регистрация на blueprint-и
    from app.auth import auth_bp
    from app.main import main_bp
    from app.ai import ai_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(ai_bp, url_prefix='/ai')

    # Импортиране на моделите тук, за да работи user_loader
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
