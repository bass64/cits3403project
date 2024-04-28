#!usr/bin/python
from app.models import Article, Review
from app import db
from sqlalchemy.sql import text
import datetime

def create_database():
    #create tables
    db.create_all()
    #clear any info
    Article.query.delete()

    #just using python objects for now
    articles = {
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
            album_creator=0,
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
            album_creator=0,
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
            album_creator=0,
            album_create_time=datetime.datetime.now()
        )
    }

    #add info, then commit
    for entry in articles:
        db.session.add(entry)
    db.session.commit()

def home_query(search, sort):
    #values for sort will be like...
    #album_create_time.desc()
    order = "article_" + sort
    if search != "":
        return Article.query.order_by(text(order)).filter_by(search in Article.album_artist)
    else:
        return Article.query.order_by(text(order))
    
    
def article_query(id):
    return Article.query.get(id)