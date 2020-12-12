from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

db = SQLAlchemy()


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    published_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    tags = db.relationship('Tag', backref='blog', lazy=True)
    rounds = db.relationship('Round', backref='blog', lazy=True)
    author = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return self.title


class Tag(db.Model):
    name = db.Column(db.String(20), nullable=False, primary_key=True)
    blog = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=True)

    def __repr__(self):
        return self.name


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    blogs = db.relationship('Blog', backref='author', lazy=True)

    def __repr__(self):
        return self.name


class RoundType(enum.Enum):
    shortlisting = 'shortlisting'
    interview = 'interview'

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_type = db.Column(db.Enum(RoundType), nullable=False)
    company_name = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    blog = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"