#!usr/bin/python
from app.models import Article, Review, User
from app import db
from sqlalchemy.sql import text
import datetime, os
from flask_login import current_user
from flask import current_app, flash
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID='c85b55132e4e4e33bf4852c481147a1d'
SPOTIPY_CLIENT_SECRET='983c70ccd5a949a29f6f7215d96555ea'

def create_database():
    #create tables
    db.create_all()
    #clear any info 
    Article.query.delete()
    Review.query.delete()
    User.query.delete()
    #delete any images in albums
    for file in os.listdir("./app/static/albums"):
        os.remove("./app/static/albums/" + file)

    users = json.loads(open("./app/json/User.json").read())
    for i in range(10):
        new_user = User(
            user_id=users[str(i)]["user_id"],
            username=users[str(i)]["username"],
            password_hash=users[str(i)]["password_hash"],
        )
        db.session.add(new_user)

    articles = json.loads(open("./app/json/Article.json").read())
    for i in range(20):
        new_article = Article (
            album_id=articles[str(i)]["album_id"],
            album_artist=articles[str(i)]["album_artist"],
            album_title=articles[str(i)]["album_title"],
            album_art=articles[str(i)]["album_art"],
            album_year=articles[str(i)]["album_year"],
            album_type=articles[str(i)]["album_type"],
            album_rating=articles[str(i)]["album_rating"],
            album_review_no=articles[str(i)]["album_review_no"],
            album_rating_no=articles[str(i)]["album_rating_no"],
            user_id=articles[str(i)]["user_id"],
            album_create_time=datetime.datetime.now()
        )
        db.session.add(new_article)

    reviews = json.loads(open("./app/json/Review.json").read())
    for i in range(50):
        new_review = Review(
            album_id=reviews[str(i)]["album_id"],
            review_id=reviews[str(i)]["review_id"],
            review_text=reviews[str(i)]["review_text"],
            review_rating=reviews[str(i)]["review_rating"],
            user_id=reviews[str(i)]["user_id"],
            review_create_time=datetime.datetime.now()
        )
        db.session.add(new_review)
        update_album(reviews[str(i)]["album_id"], reviews[str(i)]["review_rating"], reviews[str(i)]["review_text"])

    #add info, then commit
    db.session.commit()

def home_query(search, sort):
    query = db.session.query(Article, User).join(User, User.user_id == Article.user_id)
    if sort != None:
        order = "article_" + sort
    #default sort, by newest
    elif sort == None:
        order = "article_album_create_time DESC"
    if search != None:
        #search checks artist, title, year and type
        return query.order_by(text(order)).filter(\
            Article.album_artist.like(f'%{search}%')\
            | Article.album_title.like(f'%{search}%')\
            | Article.album_year.like(f'%{search}%')\
            | Article.album_type.like(f'%{search}%')\
            )
    else:
        return query.order_by(text(order))
    
def spotify_link(request):
    #get link and split it to just id
    link = request.form.get("url")
    link = link.split("/")
    link = link[-1]
    if "?" in link:
        link = link.split("?")
        link = link[0]

    #use api to get info on link
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))
    try:
        album = sp.album(album_id=link)
    except:
        flash("Invalid URL", "post_auto_error")
        return "error"

    #construct an object for the album info
    new_id = db.session.query(Article).order_by(Article.album_id.desc()).first().album_id + 1
    album_object = Article(
        album_id=new_id,
        album_artist=album["artists"][0]["name"],
        album_title=album["name"],
        album_art= album["images"][1]["url"],
        album_year=album["release_date"][:4],
        album_type=str(album["album_type"]).capitalize(),
        album_rating=0,
        album_review_no=0,
        album_rating_no=0,
        user_id=current_user.get_id(),
        album_create_time=datetime.datetime.now()
    )

    #add to db
    #current_app.logger.info(album_object)
    db.session.add(album_object)
    db.session.commit()
    
def add_album_to_db(request):
    form = request.form
    #queries article, sorts by highest id, gets the first row, gets its id, and adds 1 to it
    new_id = db.session.query(Article).order_by(Article.album_id.desc()).first().album_id + 1

    #default path if no image provided
    if (request.files["image"] == None):
        path = "./../static/no_image.png"
    else:
        upload = request.files["image"]
        path = os.path.join("app/static/albums/", str(new_id) + ".png")
        upload.save(path)
        path = "./../" + path[3:]


    album = Article(
        album_id=new_id,
        album_artist=form.get("artist"),
        album_title=form.get("title"),
        album_art=path,
        album_year=form.get("date")[:4],
        album_type=form.get("type"),
        album_rating=0,
        album_review_no=0,
        album_rating_no=0,
        user_id=current_user.get_id(),
        album_create_time=datetime.datetime.now()
    )

    #current_app.logger.info(album)
    db.session.add(album)
    db.session.commit()

def add_review_to_db(form, article_id):
    #if user has already reviewed this album, return early
    if (db.session.query(Review).filter(Review.album_id == article_id).filter(Review.user_id == current_user.get_id()).first() != None):
        flash("You have already posted a review for this album", "review_error")
        return

    #queries review, sorts by highest id, gets the first row, gets its id, and adds 1 to it
    new_id = db.session.query(Review).order_by(Review.review_id.desc()).first().review_id + 1

    review = Review(
            album_id=article_id,
            review_id=new_id,
            review_text=form.get("review"),
            review_rating=form.get("choose_rating"),
            user_id=current_user.get_id(),
            review_create_time=datetime.datetime.now()
        )

    db.session.add(review)
    #current_app.logger.info(review)
    update_album(article_id, form.get("choose_rating"), form.get("review"))
    db.session.commit()

def update_album(album_id, rating, review):
    #get an updated average rating
    current_rating = db.session.query(Article).filter(Article.album_id == album_id).first().album_rating
    num_reviews = db.session.query(Article).filter(Article.album_id == album_id).first().album_review_no
    num_ratings = db.session.query(Article).filter(Article.album_id == album_id).first().album_rating_no
    #average of current_rating and new_rating, factoring in that current_ratings already been averaged n-1 times
    new_rating = ((current_rating * float(num_ratings + num_reviews)) + float(rating)) / float(num_ratings + num_reviews + 1)

    db.session.query(Article).filter(Article.album_id == album_id).\
    update({"album_rating": new_rating}, synchronize_session = False)

    if (review == ""):
        db.session.query(Article).filter(Article.album_id == album_id).\
        update({"album_rating_no": num_ratings + 1}, synchronize_session = False)
    else:
        db.session.query(Article).filter(Article.album_id == album_id).\
        update({"album_review_no": num_reviews + 1}, synchronize_session = False)