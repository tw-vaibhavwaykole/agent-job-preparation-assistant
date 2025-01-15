from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class MockTest(Base):
    __tablename__ = "mock_tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String)
    duration = Column(Integer)  # in minutes
    total_marks = Column(Integer)
    passing_marks = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    questions = relationship("Question", back_populates="test")
    results = relationship("TestResult", back_populates="test")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'duration': self.duration,
            'total_marks': self.total_marks,
            'passing_marks': self.passing_marks,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("mock_tests.id"))
    question_text = Column(String, nullable=False)
    question_type = Column(String(50))  # MCQ, descriptive, etc.
    marks = Column(Integer)
    correct_answer = Column(String)
    explanation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    test = relationship("MockTest", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

    def to_dict(self):
        return {
            'id': self.id,
            'test_id': self.test_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'marks': self.marks,
            'explanation': self.explanation,
            'created_at': str(self.created_at)
        }

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    answer_text = Column(String)
    is_correct = Column(Boolean)
    marks_obtained = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    question = relationship("Question", back_populates="answers")
    user = relationship("User", back_populates="answers")

    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'user_id': self.user_id,
            'answer_text': self.answer_text,
            'is_correct': self.is_correct,
            'marks_obtained': self.marks_obtained,
            'created_at': str(self.created_at)
        }

class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("mock_tests.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    total_marks_obtained = Column(Float)
    percentage = Column(Float)
    passed = Column(Boolean)
    completed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    test = relationship("MockTest", back_populates="results")
    user = relationship("User", back_populates="test_results")

    def to_dict(self):
        return {
            'id': self.id,
            'test_id': self.test_id,
            'user_id': self.user_id,
            'total_marks_obtained': self.total_marks_obtained,
            'percentage': self.percentage,
            'passed': self.passed,
            'completed_at': str(self.completed_at)
        } 