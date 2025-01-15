from app import db
from datetime import datetime

class MockTest(db.Model):
    __tablename__ = 'mock_test'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('Question', backref='mock_test', lazy=True)
    test_results = db.relationship('TestResult', backref='mock_test', lazy=True)

class Question(db.Model):
    __tablename__ = 'question'
    
    id = db.Column(db.Integer, primary_key=True)
    mock_test_id = db.Column(db.Integer, db.ForeignKey('mock_test.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    
    # Remove the circular reference and clearly specify the relationship
    answers = db.relationship('Answer', 
                            backref='question',
                            lazy=True,
                            foreign_keys='Answer.question_id')
    
    # Specify the correct answer relationship separately
    correct_answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=True)
    correct_answer = db.relationship('Answer',
                                   foreign_keys=[correct_answer_id],
                                   uselist=False,
                                   post_update=True)  # Prevents circular dependency

class Answer(db.Model):
    __tablename__ = 'answer'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)

class TestResult(db.Model):
    __tablename__ = 'test_result'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mock_test_id = db.Column(db.Integer, db.ForeignKey('mock_test.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow) 