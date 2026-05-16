from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String) # 'admin', 'faculty', 'student'

    subjects = relationship("Subject", back_populates="creator")
    quizzes = relationship("Quiz", back_populates="creator")
    results = relationship("Result", back_populates="student")

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    description = Column(String)
    created_by_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="subjects")
    quizzes = relationship("Quiz", back_populates="subject")

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    duration_minutes = Column(Integer)
    total_marks = Column(Integer)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))

    subject = relationship("Subject", back_populates="quizzes")
    creator = relationship("User", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="quiz", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question_text = Column(String)
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)
    correct_option = Column(String) # 'A', 'B', 'C', or 'D'
    marks = Column(Integer)

    quiz = relationship("Quiz", back_populates="questions")

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    score = Column(Integer)
    total_marks = Column(Integer)
    percentage = Column(Float)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("User", back_populates="results")
    quiz = relationship("Quiz", back_populates="results")
