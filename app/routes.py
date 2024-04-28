from app import app
from flask import render_template, redirect, url_for, request
from app.forms import LoginForm,SignUp,Search
from app.database import *

@app.before_request
def run_on_start():
    create_database()

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Testpage")

@app.route('/')
@app.route("/home")
def home():
    search = request.args.get("search")
    sort = request.args.get("sort")
    articles = home_query(search, sort)
    form=Search()
    return render_template("home.html", title="Home", articles=articles, form=form)

@app.route('/article/<int:article_id>')
def article(article_id):
    album = Article.query.get(article_id)
    return render_template("article_full.html", title = "" + album.album_artist + " - " + album.album_title, album=album, full=True)

@app.route('/create-post')
def create_post():
    return render_template("create-post.html", title="Create Post")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    createForm = SignUp()
    if form.validate_on_submit():
        return redirect(location=url_for("home"))
    if createForm.validate_on_submit():
        return redirect(location=url_for("home"))
    return render_template('login.html', title='Sign In', form=form,createForm=createForm)

@app.errorhandler(404)
def page_not_found(*args):
    return render_template("error-page.html", title="Page Not Found")
