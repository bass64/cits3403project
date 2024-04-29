from app import app, db
from flask import render_template,redirect, url_for,request,flash
from app.forms import LoginForm,SignUp
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Testpage")

@app.route('/')
@app.route("/home")
def home():
    #get list of articles from a database in future
    articles = [{
        "id": 0,
        "title": "Placeholder",
        "album_art": "./../static/artist-placeholder.png",
        "artist": "Artist",
        "year": "1970",
        "type": "EP",
        "star_rating": 7,
        "review_no": 5,
        "rating_no": 20,
        }, {
        "id": 1,
        "title": "Placeholder 2",
        "album_art": "./../static/artist-placeholder2.png",
        "artist": "Artist",
        "year": "1971",
        "type": "EP",
        "star_rating": 1,
        "review_no": 3,
        "rating_no": 17,
        }, {
        "id": 2,
        "title": "Placeholder 3",
        "album_art": "./../static/artist-placeholder3.png",
        "artist": "Artist",
        "year": "1973",
        "type": "Album",
        "star_rating": 10,
        "review_no": 30,
        "rating_no": 174,
        }]
    return render_template("home.html", title="Home", articles=articles)


@app.route('/article/<int:article_id>')
def article(article_id):
    #dummy album data for testing, get this from a database in future
    if (article_id == 0):
        album = {
        "id": 0,
        "title": "Placeholder",
        "album_art": "./../static/artist-placeholder.png",
        "artist": "Artist",
        "year": "1970",
        "type": "EP",
        "star_rating": 7,
        "review_no": 5,
        "rating_no": 20,
        }
    if (article_id == 1):
        album = {
        "id": 1,
        "title": "Placeholder 2",
        "album_art": "./../static/artist-placeholder2.png",
        "artist": "Artist",
        "year": "1971",
        "type": "EP",
        "star_rating": 1,
        "review_no": 3,
        "rating_no": 17,
        }
    if (article_id == 2):
        album = {
        "id": 2,
        "title": "Placeholder 3",
        "album_art": "./../static/artist-placeholder3.png",
        "artist": "Artist",
        "year": "1973",
        "type": "Album",
        "star_rating": 10,
        "review_no": 30,
        "rating_no": 174,
        }

    return render_template("article_full.html", title = "" + album["artist"] + " - " + album["title"], album=album, full=True)

@app.route('/create-post')
def create_post():
    return render_template("create-post.html", title="Create Post")

#renders the login page (only GET request)
@app.route('/login')
def login():
    form = LoginForm()
    createForm = SignUp()
    return render_template('login.html', title='Sign In', form=form,createForm=createForm)

#processes sign up post requests
@app.route('/signup', methods=['POST'])
def signup_post():

    #add user to database
    username = request.form.get('username')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    if not (password == confirm):
        flash('Passwords do not match','signup_error')
        return redirect(url_for('login'))

    #check if user exists
    existing_user = User.query.filter_by(username=username).first()

    #if user already exists do not create new user with same username
    if existing_user:
        flash('User exists','signup_error')
        return redirect(url_for('login'))

    #if user is new, add to database
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return redirect(location=url_for("home"))

#processes login post requests
@app.route('/login', methods=['POST'])
def login_post():

    username = request.form.get('username')
    password = request.form.get('password')

    #check for existing user
    existing_user = User.query.filter_by(username=username).first()

    #if username couldnt be found or the password doesnt match throw an error
    if not existing_user or not (existing_user.password == password):
        flash('Please check your login details','login_failed')
        return redirect(url_for('login'))

    return redirect(location=url_for("home"))

@app.errorhandler(404)
def page_not_found(*args):
    return render_template("error-page.html", title="Page Not Found")
