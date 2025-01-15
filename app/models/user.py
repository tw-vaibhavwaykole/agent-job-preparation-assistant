from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Add relationships
    test_results = db.relationship('TestResult', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>' 