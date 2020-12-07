import os, json
from flask import Flask, render_template, redirect, url_for

TEMPLATE_DIR = os.path.join("..", "templates")
STATIC_DIR = os.path.join("..", "static")

app = Flask(__name__, template_folder = TEMPLATE_DIR, static_folder = STATIC_DIR)

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

@app.route('/login')
def login(): 
    pass

@app.route('/signup')
def signup(): 
    pass

if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0", port = 8000)
