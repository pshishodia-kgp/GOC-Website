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
    return render_template('allblogs.j2', title = 'Blogs')


if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0", port = 8000)
