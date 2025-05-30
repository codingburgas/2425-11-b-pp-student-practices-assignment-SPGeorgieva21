from flask import Flask
from .extensions import db, login_manager, bootstrap, migrate
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)

    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.ai.routes import ai_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(ai_bp)

    # Опционално, ако искаш login_manager да знае къде да праща НЕлогнатите
    login_manager.login_view = 'auth.login'

    return app
