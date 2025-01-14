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
    content = db.Column(db.Text)
    content_type = db.Column(db.String(20))  # 'text', 'pdf', 'video', 'code'
    file_path = db.Column(db.String(256))    # For uploaded files
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # AI-related fields
    ai_summary = db.Column(db.Text)          # AI-generated summary
    keywords = db.Column(db.JSON)            # Extracted keywords
    difficulty_level = db.Column(db.String(20))
    estimated_time = db.Column(db.Integer)    # in minutes

class StudyMaterialContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('study_material.id'))
    content_type = db.Column(db.String(20))
    content = db.Column(db.Text)
    file_path = db.Column(db.String(256))
    order = db.Column(db.Integer)

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