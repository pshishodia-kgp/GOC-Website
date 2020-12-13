import json
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user
from goc import app
from goc.forms import SignUpForm, LoginForm

# Home Page
@app.route('/')
def home():
    return render_template('home.j2', title = '')


# Listing the blogs
@app.route('/blogs')
def blogList():
    # tags should always include all distinct company name (do it while inserting in database)
    # Published at should store time gap 
    # Only need to send these columns. 
    blogs = [{'id': '3434', 'title' : 'First blog', 
        'content' :  'hello my name is blah blah blah, welcome to blah blah blah', 
        'published_at': '2 days ago', 'tags': ['google', 'facebook', 'help', 'hello', 'bye', 'hehe', 'wtf', 'last'],
        'author': 'thelethalcode'}, 
        {'id': '3434', 'title' : 'Second Blog', 
        'content' :  'hello my name is blah blah blah, welcome to blah blah blah', 
        'published_at': '2 days ago', 'tags': ['google', 'facebook', 'help', 'hello', 'bye', 'hehe'],
        'author': 'fugazi'}]
    
    allTags = ['google', 'facebook', 'help', 'hello', 'wtf', 'blah', 'fugazi', 'lethalcode']
    return render_template('allblogs.j2', title = 'Blogs', blogs = blogs, allTags = allTags)

@app.route('/blog')           ## get single blog having given id
def blog():
    blog_id = request.args.get('blog_id') 
    blog = {
        'id': '3434', 'title' : 'Second Blog',
        'content' :  'hello my name is blah blah blah, welcome to blah blah blah',
        'shortlisting_content' : 'shortlisting rounds were easy aF',
        'shortlisting_rounds' : [{'company_name' : 'google', 'content': 'Idk it was usual'}, {'company_name' : 'uber', 'content': 'Idk it was usual'}],
        'interview_content' : 'yeah, the usual stuff but they ask a shitload of crap too',
        'interview_rounds': [{'company_name' : 'facebook', 'content': 'Idk it was usual'}, {'company_name' : 'nutanix', 'content': 'Idk it was usual'}],
        'published_at': '2 days ago', 'tags': ['google', 'facebook', 'help', 'hello', 'bye', 'hehe', 'wtf', 'last'],
        'author': 'thelethalcode'
    }
    if(blog_id == '3434'):
        return render_template('blog.j2', title = blog['title'], blog = blog)
    else : 
        return 'Error'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        #get the user from database
        #login_user(user)
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
        return redirect(url_for('login'))
    return render_template('signup.j2', title='Sign Up', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
