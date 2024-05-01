from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Testpage")

@app.route('/login')
def login():
    return render_template("login.html", title="Login")

@app.route('post-review')
def post_review():
    return render_template("post-review.html", title="Post Review")
