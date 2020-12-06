import os, json
from flask import Flask, render_template, redirect

TEMPLATE_DIR = os.path.join("..", "templates")
STATIC_DIR = os.path.join("..", "static")


# Initialise the app
def initApp():
    app = Flask(__name__, template_folder = TEMPLATE_DIR, static_folder = STATIC_DIR)
    app.debug = True
    return app


# Home Page
@app.route('/')
def home():
    return "Welcome to Grimoire of Code homepage. WIP"


# Listing the blogs
@app.route('/blogs')
def blogList():
    pass


if __name__ == '__main__':

    app = initApp()
    app.run("0.0.0.0", port = 8000)
