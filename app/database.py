#!usr/bin/python
from app.models import Article, Review, User
from app import db
from sqlalchemy.sql import text
import datetime

def create_database():
    #create tables
    db.create_all()
    #clear any info FIND A BETTER WAY TO DO THIS THIS METHOD SUCKS
    Article.query.delete()
    Review.query.delete()
    User.query.delete()

    #just using python objects for now
    entries = {
        Article(
            album_id=0,
            album_artist="Artist",
            album_title="Placeholder",
            album_art="./../static/artist-placeholder.png",
            album_year=1970,
            album_type="EP",
            album_rating=7.53,
            album_review_no=5,
            album_rating_no=20,
            user_id=0,
            album_create_time=datetime.datetime.now()
        ),
        Article(
            album_id=1,
            album_artist="Artist",
            album_title="Placeholder 2",
            album_art="./../static/artist-placeholder2.png",
            album_year=1971,
            album_type="Album",
            album_rating=0.94,
            album_review_no=3,
            album_rating_no=17,
            user_id=1,
            album_create_time=datetime.datetime.now()
        ),
        Article(
            album_id=2,
            album_artist="Artist",
            album_title="Placeholder 3",
            album_art="./../static/artist-placeholder3.png",
            album_year=1973,
            album_type="Single",
            album_rating=9.99,
            album_review_no=30,
            album_rating_no=170,
            user_id=0,
            album_create_time=datetime.datetime.now()
        ),

        Review(
            album_id=0,
            review_id=0,
            review_text="An amazing first album!",
            review_rating=7,
            user_id=0,
            review_create_time=datetime.datetime.now()
        ),
        Review(
            album_id=0,
            review_id=1,
            review_text="",
            review_rating=6,
            user_id=1,
            review_create_time=datetime.datetime.now()
        ),
        Review(
            album_id=1,
            review_id=2,
            review_text="",
            review_rating=1,
            user_id=1,
            review_create_time=datetime.datetime.now()
        ),
        Review(
            album_id=2,
            review_id=3,
            review_text="A great return to form, 10/10",
            review_rating=10,
            user_id=0,
            review_create_time=datetime.datetime.now()
        ),
        Review(
            album_id=2,
            review_id=4,
            review_text="",
            review_rating=9,
            user_id=1,
            review_create_time=datetime.datetime.now()
        ),
        Review(
            album_id=2,
            review_id=5,
            review_text="What a great album: If you would allow me, I would love to regale you with my magnum opus, a piece of art I simply call, 1000 A's. it goes something like this:\n AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAA",
            review_rating=8,
            user_id=2,
            review_create_time=datetime.datetime.now()
        ),
        Review(
            album_id=2,
            review_id=6,
            review_text="",
            review_rating=10,
            user_id=3,
            review_create_time=datetime.datetime.now()
        ),

        User(
            user_id=0,
            username="berspoke_boy9",
            password="oopsnohash"
        ),

        User(
            user_id=1,
            username="SilentSimon",
            password="oopsnohash"
        ),

        User(
            user_id=2,
            username="The Honourable And Eloquent Adam",
            password="oopsnohash"
        ),

        User(
            user_id=3,
            username="4rd Guy",
            password="oopsnohash"
        )
    }

    #add info, then commit
    for entry in entries:
        db.session.add(entry)
    db.session.commit()

def home_query(search, sort):
    if sort != None:
        order = "article_" + sort
    #default sort, by newest
    elif sort == None:
        order = "article_album_create_time DESC"
    if search != None:
        #search checks artist, title, year and type
        return Article.query.order_by(text(order)).filter(\
            Article.album_artist.like(f'%{search}%')\
            | Article.album_title.like(f'%{search}%')\
            | Article.album_year.like(f'%{search}%')\
            | Article.album_type.like(f'%{search}%')\
            )
    else:
        return Article.query.order_by(text(order))