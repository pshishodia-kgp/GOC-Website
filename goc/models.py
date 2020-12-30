from goc import db, login_manager, admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask_login import UserMixin
import enum

class Association(db.Model):
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    shortlisting_content = db.Column(db.Text, nullable=False)
    interview_content = db.Column(db.Text, nullable=True)
    tags = db.relationship('Association', backref='blog')
    rounds = db.relationship('Round', backref='blog', lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    blog = db.relationship('Blog', uselist = False, backref="post", lazy=True)
    published_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref = 'post', lazy = True)

    def __repr__(self):
        return self.title
    

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    blogs = db.relationship('Association', backref='tag')


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
    profile_pic_url = db.Column(db.String(255))
    name = db.Column(db.String(40), nullable=False)
    comments = db.relationship('Comment', backref = 'author', lazy = True)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Comment(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    parent = db.relationship(lambda: Comment, remote_side = id, backref = 'children')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    upvotes = db.Column(db.Integer, default = 0)
    downvotes = db.Column(db.Integer, default = 0)
    depth = db.Column(db.Integer, default = 0)
    published_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self): 
        return f"Comment('{self.content}', by: {self.author.username})"

admin.add_view(ModelView(Blog, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))
# admin.add_view(ModelView(RoundType, db.session))
admin.add_view(ModelView(Round, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))