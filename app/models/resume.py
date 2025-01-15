from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="resumes")
    experiences = relationship("Experience", back_populates="resume")
    education = relationship("Education", back_populates="resume")
    skills = relationship("Skill", back_populates="resume")

class Experience(Base):
    __tablename__ = "experiences"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    company = Column(String(255))
    position = Column(String(255))
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    description = Column(String)
    resume = relationship("Resume", back_populates="experiences")

class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    institution = Column(String(255))
    degree = Column(String(255))
    field = Column(String(255))
    graduation_date = Column(DateTime)
    resume = relationship("Resume", back_populates="education")

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    name = Column(String(255))
    level = Column(String(50))
    resume = relationship("Resume", back_populates="skills") 