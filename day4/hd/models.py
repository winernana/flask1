from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(256))

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    c_name = db.Column(db.String(255),unique=True,nullable=False)
    arts = db.relationship('Article',backref='category')
    __tablename__ = 'category'

class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(255),unique=True,nullable=False)
    desc = db.Column(db.String(255),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    type = db.Column(db.Integer,db.ForeignKey('category.id'))