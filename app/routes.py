from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Testpage")

@app.route('/article/<int:article_id>')
def article(article_id):
    #dummy album data for testing, get this from a database in future
    if (article_id == 0):
        album = {
        "id": 0,
        "title": "Placeholder",
        "album_art": "https://cdn.discordapp.com/attachments/1229708541569269811/1229708580932948048/artist_-_placeholder.png?ex=6630aa5c&is=661e355c&hm=7d4c8fa2dc2be498ce4bbe1b83754477734627d85f97d6684e162901afb70431&",
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
        "album_art": "https://cdn.discordapp.com/attachments/1229708541569269811/1229726976277872650/artist_-_placeholder_2.png?ex=6630bb7e&is=661e467e&hm=ff19805dd91cbf428109f67915d36e58151aa14c548523d22ef7619643ac35d0&",
        "artist": "Artist",
        "year": "1971",
        "type": "EP",
        "star_rating": 1,
        "review_no": 3,
        "rating_no": 17,
        }
    return render_template("article_full.html", title = "" + album["artist"] + " - " + album["title"], album=album)

