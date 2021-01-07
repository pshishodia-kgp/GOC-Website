from goc import db, login_manager, admin, STATIC_DIR
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask_login import UserMixin
import enum

Association = db.Table('association_table',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

CommentVotes = db.Table('comment_votes_table', 
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id')),
    db.Column('vote_id', db.Integer, db.ForeignKey('vote.id'))
)

PostVotes = db.Table('post_votes_table', 
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('vote_id', db.Integer, db.ForeignKey('vote.id'))
)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    shortlisting_content = db.Column(db.Text, nullable=False)
    interview_content = db.Column(db.Text, nullable=True)
    rounds = db.relationship('Round', backref='blog', lazy=True)

class PostOrComment(enum.Enum): 
    post = 'post'
    comment = 'comment'
class Vote(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    vote_value = db.Column(db.Integer, default = 0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    vote_on = db.Column(db.Enum(PostOrComment), nullable = False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    blog = db.relationship('Blog', uselist = False, backref="post", lazy=True)
    published_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref = 'post', lazy = True)
    tags = db.relationship('Tag', backref='post', secondary='association_table', lazy="dynamic")
    votes_count = db.Column(db.Integer, default = 0)
    votes = db.relationship('Vote', secondary = PostVotes, lazy = "dynamic")

    def __repr__(self):
        return self.title
    

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    posts = db.relationship('Post', backref='tag', secondary='association_table', lazy="dynamic")
    isCompany = db.Column(db.Boolean, default=False)

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
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=True)
    selected = db.Column(db.Boolean, default=0)
    joining = db.Column(db.Boolean, default=0)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    profile_pic_url = db.Column(db.String(255), default = '//userpic.codeforces.com/no-title.jpg')
    name = db.Column(db.String(40), nullable=False)
    comments = db.relationship('Comment', backref = 'author', lazy = True)
    posts = db.relationship('Post', backref='author', lazy=True)
    votes = db.relationship('Vote', backref = 'user', lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Comment(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    parent = db.relationship(lambda: Comment, remote_side = id, backref = 'children')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    depth = db.Column(db.Integer, default = 0)
    published_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    votes = db.relationship('Vote', secondary = CommentVotes, lazy = "dynamic")
    votes_count = db.Column(db.Integer, default = 0)

    def __repr__(self): 
        return f"Comment('{self.content}', by: {self.author.username})"

class Kgpians(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    maxrating = db.Column(db.Integer, nullable=False)

admin.add_view(ModelView(Blog, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))
# admin.add_view(ModelView(RoundType, db.session))
admin.add_view(ModelView(Round, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Vote, db.session))