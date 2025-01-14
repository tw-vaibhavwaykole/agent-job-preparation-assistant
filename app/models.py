from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    interests = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text)
    external_link = db.Column(db.String(256))

class MockTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(64))
    duration = db.Column(db.Integer)  # in minutes
    questions = db.relationship('Question', backref='test', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('mock_test.id'))
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON)
    correct_answer = db.Column(db.String(1)) 