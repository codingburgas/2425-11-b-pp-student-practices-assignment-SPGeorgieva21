from flask import Flask
from app.extensions import db, login_manager, mail, bootstrap, migrate

def create_app():
    app = Flask(__name__)
    # Тук използваме 'config.Config' (с клас), а не просто 'config'
    app.config.from_object('config.Config')

    # Инициализиране на разширения
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Задаване на login изгледа
    login_manager.login_view = 'auth.login'

    # Регистрация на blueprint-и
    from app.auth import auth_bp
    from app.main import main_bp
    from app.ai import ai_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(ai_bp, url_prefix='/ai')

    # Импортиране на моделите за user_loader
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
