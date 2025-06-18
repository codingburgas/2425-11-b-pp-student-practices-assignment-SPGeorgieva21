import pytest
from app import create_app, db as _db
from app.models import User
from flask_login import login_user

@pytest.fixture
def app():
    app = create_app('testing')  # Ensure you have a testing config
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    return _db

@pytest.fixture
def user(db):
    user = User(username='testuser', email='test@example.com', role='user')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user
