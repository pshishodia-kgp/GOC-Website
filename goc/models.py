from goc import db, login_manager, admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask_login import UserMixin
import enum

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    shortlisting_content = db.Column(db.Text, nullable=False)
    interview_content = db.Column(db.Text, nullable=True)
    tags = db.relationship('Tag', backref='blog', lazy=True)
    rounds = db.relationship('Round', backref='blog', lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    blogs = db.relationship('Blog', backref="post", lazy=True)
    published_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return self.title
    

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=True)


class RoundType(enum.Enum):
    shortlisting = 'shortlisting'
    interview = 'interview'

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_type = db.Column(db.Enum(RoundType), nullable=False)
    company_name = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=True)
    selected = db.Column(db.Boolean, default=0)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

admin.add_view(ModelView(Blog, db.session))
admin.add_view(ModelView(Tag, db.session))
# admin.add_view(ModelView(RoundType, db.session))
admin.add_view(ModelView(Round, db.session))
admin.add_view(ModelView(User, db.session))
