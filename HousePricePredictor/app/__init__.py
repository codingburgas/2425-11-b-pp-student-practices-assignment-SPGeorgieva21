from flask import Flask
from app.models import db
from app.auth.routes import auth_bp
from app.main.routes import main_bp
from app.ai.routes import ai_bp
from app.admin.routes import admin_bp
from flask_login import LoginManager
from app.models import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(admin_bp)

    return app
