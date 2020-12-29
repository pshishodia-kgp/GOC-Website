from goc import db, login_manager, admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask_login import UserMixin
import enum

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    published_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    shortlisting_content = db.Column(db.Text, nullable=False)
    interview_content = db.Column(db.Text, nullable=True)
    tags = db.relationship('Tag', backref='blog', lazy=True)
    rounds = db.relationship('Round', backref='blog', lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref = 'blog', lazy = True)

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



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    blogs = db.relationship('Blog', backref='author', lazy=True)
    comments = db.relationship('Comment', backref = 'author', lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Comment(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable = False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    parent = db.relationship(lambda: Comment, remote_side = id, backref = 'children')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    upvotes = db.Column(db.Integer, default = 0)
    downvotes = db.Column(db.Integer, default = 0)
    depth = db.Column(db.Integer, default = 0)

    def __repr__(self): 
        return f"Comment('{self.content}', by: {self.author.username})"

admin.add_view(ModelView(Blog, db.session))
admin.add_view(ModelView(Tag, db.session))
# admin.add_view(ModelView(RoundType, db.session))
admin.add_view(ModelView(Round, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))
