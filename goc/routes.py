import json, requests, random
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from goc import app, db, USERNAME_REGEX_NOT
from goc.forms import *
from goc.models import *


# Home Page
@app.route('/')
def home():
    return render_template('home.j2', title = '')

@app.route('/forum')
def postList():
    page = request.args.get('page', 1, int)
    posts = Post.query.order_by(Post.published_at.desc()).paginate(per_page=2, page=page)
    tags = Tag.query.group_by(Tag.name).all()
    allTags = [tag.name for tag in tags]
    return render_template('allblogs.j2', title='Posts', posts=posts, allTags=allTags)

@app.route('/post')           ## get single blog having given id
def post():
    post_id = request.args.get('post_id')
    if not post_id:
        return redirect(url_for('postList'))

    post = Post.query.filter_by(id=int(post_id)).first()

    if post:
        return render_template('blog.j2', title=post.title, post=post)
    else:
        flash('Post Not Found!', 'danger')
        return redirect(url_for('postList'))


# login and sign up routes

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter((User.username==form.username_or_email.data) | (User.email==form.username_or_email.data)).first()
        login_user(user)
        return redirect(url_for('home'))
    else:
        flash('Login Failed. Please check username/email and password', 'danger')
    return render_template('login.j2', title='Login', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        print(form.username.data)
        user = User(username=form.username.data, email=form.email.data,
            name=form.name.data, password=form.password.data,
            profile_pic_url = form.profile_pic_url.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('signup_verified'))
    return render_template('signup.j2', title='Sign Up', form = form)


@app.route('/signup-verified', methods=['GET', 'POST'])
def signup_verified():
    return render_template('signup_verified.j2', title='Verify Signup')


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been successfully logged out!', 'success')
    return redirect(url_for('home'))


# blog submission route

@app.route('/createPost',methods = ['POST','GET'])
@login_required
def submitPost():

    isBlog = request.args.get('interview')

    if isBlog == 'True':
        blog_form = BlogForm()

        if(blog_form.addInterview.data):
            blog_form.interview.rounds.append_entry()        
            return render_template('blogform.j2', post_form=blog_form)
        
        if(blog_form.addShortListing.data):
            blog_form.shortlisting.rounds.append_entry()
            return render_template('blogform.j2', post_form=blog_form)
        
        if(blog_form.addTag.data):
            blog_form.tags.append_entry()
            return render_template('blogform.j2', post_form=blog_form)
        
        if(blog_form.validate_on_submit()):
            #First make all tags unique
            tags = [str(x) for x in set(blog_form.tags.data)]

            post_data = Post(
                title = str(blog_form.title.data),
                content = str(blog_form.content.data),
                author_id = current_user.id
            )

            try:
                db.session.add(post_data)
                db.session.commit()
            except:
                return "Error in adding Post"

            post_id = post_data.id

            blog_data = Blog(            
                post_id = post_id,
                shortlisting_content = str(blog_form.shortlisting.content.data),
                interview_content = str(blog_form.interview.content.data)
            )

            try:
                db.session.add(blog_data)
                db.session.commit()
            except:
                return "Error in adding Blog"
            
            blog_id = blog_data.id

            for ttag in tags:
                tag = Tag(name=ttag, blog_id=blog_id)
                try:
                    db.session.add(tag)
                except:
                    return "Error in Adding Tag"              
            
            for round in blog_form.shortlisting.rounds:
                current_round = Round(
                    round_type = RoundType.shortlisting,
                    company_name = str(round.company_name.data),
                    content = str(round.content.data),
                    blog_id = blog_id,
                    selected = round.selected.data
                )
                try:
                    db.session.add(current_round)
                except:
                    return "Error in Adding ShortListing Data"
            
            for round in blog_form.interview.rounds:
                current_round = Round(
                    round_type = RoundType.interview,
                    company_name = str(round.company_name.data),
                    content = str(round.content.data),
                    blog_id = blog_id
                )
                try:
                    db.session.add(current_round)
                except:
                    return "Error in Adding Interview Round Data"
            
            try:
                db.session.commit()                       
            except:
                return "Error in commiting changes"

            flash('Post Added Successfully!', 'success')
            return redirect(url_for('postList'))

        return render_template('blogform.j2', post_form=blog_form)
    elif isBlog == 'False':
        post_form = PostForm()
        if post_form.validate_on_submit():

            post_data = Post(
                title = str(post_form.title.data),
                content = str(post_form.content.data),
                author_id = current_user.id
            )

            try:
                db.session.add(post_data)
                db.session.commit()
            except:
                return "Error in adding Post"
            
            flash('Post Added Successfully!', 'success')
            return redirect(url_for('postList'))

        return render_template('postform.j2', post_form=post_form)
    else: 
        return redirect(url_for('home'))

@app.route('/add_comment', methods = ['GET', 'POST'])
@login_required
def addComment():
    try: 
        form = request.form
        parent_id = int(form.get('parent_id'))
        # Should actually check in database. Works in general until user tries to abuse the system
        parent_id = parent_id if parent_id != -1 else None
        
        # Put checks here. 
        comment = Comment(
            content = form.get('content'),
            post_id = int(form.get('post_id')),
            parent_id = parent_id,
            author_id = current_user.id,
            depth = int(form.get('depth')),
        )

        db.session.add(comment)
        db.session.commit()
    except: 
        return 'Error in adding comment'
    if form.get('post_id'): 
        return redirect('/post?post_id=' + form.get('post_id'))
    return redirect(url_form('home'))


@app.route('/profile/<username>')
def profile(username): 
    if re.search(USERNAME_REGEX_NOT, username): 
        return 'Invalid Username'
    user = User.query.filter_by(username = str(username)).first()
    if not user: 
        return 'Invalid Username'
    
    return render_template('user_profile.j2', user = user)