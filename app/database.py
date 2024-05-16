#!usr/bin/python
from app.models import Article, Review, User
from app import db, app
from sqlalchemy.sql import text
import datetime, os
from flask_login import current_user

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

    #just using python objects for now
    entries = {
        Article(
            album_id=0,
            album_artist="Artist",
            album_title="Placeholder",
            album_art="./../static/artist-placeholder.png",
            album_year=1970,
            album_type="EP",
            album_rating=6.5,
            album_review_no=1,
            album_rating_no=1,
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
            album_rating=0.5,
            album_review_no=0,
            album_rating_no=1,
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
            album_rating=9.25,
            album_review_no=2,
            album_rating_no=2,
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
            username="bespoke_boy9",
            password_hash="oopsnohash"
        ),

        User(
            user_id=1,
            username="SilentSimon",
            password_hash="oopsnohash"
        ),

        User(
            user_id=2,
            username="The Honourable And Eloquent Adam",
            password_hash="oopsnohash"
        ),

        User(
            user_id=3,
            username="4rd Guy",
            password_hash="oopsnohash"
        )
    }

    #add info, then commit
    for entry in entries:
        db.session.add(entry)
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

    db.session.add(album)
    db.session.commit()

def add_review_to_db(form, article_id):
    #if user has already reviewed this album, return early
    if (db.session.query(Review).filter(Review.album_id == article_id).filter(Review.user_id == current_user.get_id()).first() != None):
        #TODO print a message when multiple reviews by same user
        return

    #queries review, sorts by highest id, gets the first row, gets its id, and adds 1 to it
    new_id = db.session.query(Review).order_by(Review.review_id.desc()).first().review_id + 1

    review = Review(
            album_id=article_id,
            review_id=new_id,
            review_text=form.get("review"),
            review_rating=form.get("rating"),
            user_id=current_user.get_id(),
            review_create_time=datetime.datetime.now()
        )

    db.session.add(review)
    update_album(article_id, form)
    db.session.commit()

def update_album(album_id, form):
    #get an updated average rating
    current_rating = db.session.query(Article).filter(Article.album_id == album_id).first().album_rating
    num_reviews = db.session.query(Article).filter(Article.album_id == album_id).first().album_review_no
    num_ratings = db.session.query(Article).filter(Article.album_id == album_id).first().album_rating_no
    new_rating = current_rating + (float(form.get("rating")) / float(num_ratings + num_reviews + 1))

    db.session.query(Article).filter(Article.album_id == album_id).\
    update({"album_rating": new_rating}, synchronize_session = False)

    if (form.get("review") == ""):
        db.session.query(Article).filter(Article.album_id == album_id).\
        update({"album_rating_no": num_ratings + 1}, synchronize_session = False)
    else:
        db.session.query(Article).filter(Article.album_id == album_id).\
        update({"album_review_no": num_reviews + 1}, synchronize_session = False)