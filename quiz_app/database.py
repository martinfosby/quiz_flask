

from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine, ForeignKey, Column, String, Integer

from datetime import datetime

from . import app


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'


db = SQLAlchemy(app)



class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(60), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f'username: {self.username}'

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(60), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f'admin: {self.username}'

# class quiz(db.Model):
