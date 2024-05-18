from app import db,login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import random

STRING_MAX = 500 #temp, get a better max later

#association table to store many to many relationship between the followers (users) and the albums followed (articles)
followingTable = db.Table('followingTable', db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')), db.Column('album_id', db.Integer, db.ForeignKey('article.album_id')))

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True) #unique id
    username = db.Column(db.String(STRING_MAX), unique=True, nullable=False) #username must be unique and non nullable
    password_hash = db.Column(db.String(STRING_MAX), nullable=False) #must have password (non nullable)
    
    #define relationship to store the articles followed by the user
    following_articles = db.relationship("Article", secondary=followingTable, backref=db.backref('followers'))

    def get_id(self):
           return (self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 

    #this representation is the same format as the json files
    def __repr__(self):
        return f"\n\"{self.user_id}\": {{\
            \n\t\"user_id\": {self.user_id},\
            \n\t\"username\": \"{self.username}\",\
            \n\t\"password_hash\": \"{self.password_hash}\"\
            \n}},"

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Article(db.Model):
    album_id = db.Column(db.Integer, primary_key=True, nullable=False) #unique id
    album_artist = db.Column(db.String(STRING_MAX), nullable=False) #string
    album_title = db.Column(db.String(STRING_MAX), nullable=False) #string
    album_art = db.Column(db.String(STRING_MAX), nullable=False) #url of image
    album_year = db.Column(db.Integer, nullable=False) #4 digit int
    album_type = db.Column(db.String(STRING_MAX), nullable=False) #either Album, EP or Single
    album_rating = db.Column(db.Float, nullable=False) #float between 0-10, average
    album_review_no = db.Column(db.Integer, nullable=False) #amount of reviews
    album_rating_no = db.Column(db.Integer, nullable=False) #amount of ratings
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False) #link to user relation
    album_create_time = db.Column(db.DateTime, nullable=False) #time album was posted

    #this representation is the same format as the json files
    def __repr__(self):
        return f"\n\"{self.album_id}\": {{\
            \n\t\"album_id\": {self.album_id},\
            \n\t\"album_artist\": \"{self.album_artist}\",\
            \n\t\"album_title\": \"{self.album_title}\",\
            \n\t\"album_art\": \"{self.album_art}\",\
            \n\t\"album_year\": {self.album_year},\
            \n\t\"album_type\": \"{self.album_type}\",\
            \n\t\"album_rating\": {self.album_rating},\
            \n\t\"album_review_no\": {self.album_review_no},\
            \n\t\"album_rating_no\": {self.album_rating_no},\
            \n\t\"user_id\": {random.randint(0,9)}\
            \n}}," #random user used for testing

class Review(db.Model):
    album_id = db.Column(db.Integer, db.ForeignKey("article.album_id"), nullable=False) #link to article relation
    review_id = db.Column(db.Integer, primary_key=True, nullable=False) #unique id
    review_text = db.Column(db.String(STRING_MAX)) #body of the review, nullable
    review_rating = db.Column(db.Integer, nullable=False) #int between 0-10
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False) #link to user relation
    review_create_time = db.Column(db.DateTime, nullable=False) #time review was posted

    #this representation is the same format as the json files
    def __repr__(self):
        return f"\n\"{self.review_id}\": {{\
            \n\t\"album_id\": {self.album_id},\
            \n\t\"review_id\": {self.review_id},\
            \n\t\"review_text\": \"{self.review_text}\",\
            \n\t\"review_rating\": {self.review_rating},\
            \n\t\"user_id\": {random.randint(0,9)}\
            \n}},"