#!usr/bin/python
from app.models import Article, Review, User
from app import db
from sqlalchemy.sql import text
import datetime, os
from flask_login import current_user
import json

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
    for i in range(4):
        new_user = User(
            user_id=users[str(i)]["user_id"],
            username=users[str(i)]["username"],
            password_hash=users[str(i)]["password_hash"],
        )
        db.session.add(new_user)

    articles = json.loads(open("./app/json/Article.json").read())
    for i in range(3):
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
    for i in range(7):
        new_review = Review(
            album_id=reviews[str(i)]["album_id"],
            review_id=reviews[str(i)]["review_id"],
            review_text=reviews[str(i)]["review_text"],
            review_rating=reviews[str(i)]["review_rating"],
            user_id=reviews[str(i)]["user_id"],
            review_create_time=datetime.datetime.now()
        )
        db.session.add(new_review)

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
        return "duplicate user"

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
    update_album(article_id, form)
    db.session.commit()
    return "no errors"

def update_album(album_id, form):
    #get an updated average rating
    current_rating = db.session.query(Article).filter(Article.album_id == album_id).first().album_rating
    num_reviews = db.session.query(Article).filter(Article.album_id == album_id).first().album_review_no
    num_ratings = db.session.query(Article).filter(Article.album_id == album_id).first().album_rating_no
    new_rating = current_rating + (float(form.get("choose_rating")) / float(num_ratings + num_reviews + 1))

    db.session.query(Article).filter(Article.album_id == album_id).\
    update({"album_rating": new_rating}, synchronize_session = False)

    if (form.get("review") == ""):
        db.session.query(Article).filter(Article.album_id == album_id).\
        update({"album_rating_no": num_ratings + 1}, synchronize_session = False)
    else:
        db.session.query(Article).filter(Article.album_id == album_id).\
        update({"album_review_no": num_reviews + 1}, synchronize_session = False)