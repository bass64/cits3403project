from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Testpage")

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

    return render_template("article_full.html", title = "" + album["artist"] + " - " + album["title"], album=album)

@app.route('/login')
def login():
    return render_template("login.html", title="Login")

@app.errorhandler(404)
def page_not_found(*args):
    return render_template("error-page.html", title="Page Not Found")