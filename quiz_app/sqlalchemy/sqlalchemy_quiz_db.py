from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

username = 'root'
password = 'test'
engine = create_engine(f'mysql+pymysql://{username}:{password}@localhost/quiz_web_app')

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(16), nullable=False, unique=True)
    password_hash = Column(String(32), nullable=False)
    answer = Column(Text)
    create_time = Column(DateTime, nullable=True, default=datetime.utcnow)

class Administrator(Base):
    __tablename__ = 'administrator'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(16), nullable=False, unique=True)
    password_hash = Column(String(32), nullable=False)
    first_name = Column(String(45))
    last_name = Column(String(45))
    create_time = Column(DateTime, nullable=True, default=datetime.utcnow)

class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(45), nullable=False, unique=True)
    question = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False)
    category = Column(String(45))
    administrator_id = Column(Integer, ForeignKey('administrator.id'))
    administrator = relationship('Administrator', backref='quizzes')

class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    answer = Column(Text, nullable=False, unique=True)
    correct = Column(Boolean, nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id'))
    quiz = relationship('Quiz', backref='answers')

class UserHasQuiz(Base):
    __tablename__ = 'user_has_quiz'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), primary_key=True)
    user = relationship('User', backref='quizzes')
    quiz = relationship('Quiz', backref='users')
