from datetime import datetime
from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='user')
    is_public = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    # Fixed relationship - point to PredictionHistory
    prediction_history = db.relationship('PredictionHistory', backref='user', lazy=True)
    predictions = db.relationship('Prediction', backref='user', lazy=True)

class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    area = db.Column(db.Float, nullable=False)  # Made required
    rooms = db.Column(db.Integer, nullable=False)  # Made required
    furnished = db.Column(db.Integer, nullable=False)  # Made required (0 or 1)
    city = db.Column(db.String(100), nullable=False)  # Made required
    result = db.Column(db.Float, nullable=False)  # Made required
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<PredictionHistory {self.id} - User {self.user_id}>"

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    result = db.Column(db.String(256))

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    version = db.Column(db.String(50))