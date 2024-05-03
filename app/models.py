from app import db

STRING_MAX = 500

class User(db.Model):
     user_id = db.Column(db.Integer, primary_key=True) #unique id
     username = db.Column(db.String(STRING_MAX), unique=True, nullable=False) #username must be unique and non nullable
     password = db.Column(db.String(STRING_MAX), nullable=False) #must have password (non nullable)

     def __repr__(self) -> str:
         return f'<User {self.username} {self.password}>'

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

    def __repr__(self):
        return "[ID:{}, {} - {}]".format(self.album_id, self.album_artist, self.album_title)

class Review(db.Model):
    album_id = db.Column(db.Integer, db.ForeignKey("article.album_id"), nullable=False) #link to article relation
    review_id = db.Column(db.Integer, primary_key=True, nullable=False) #unique id
    review_text = db.Column(db.String(STRING_MAX)) #body of the review, nullable
    review_rating = db.Column(db.Integer, nullable=False) #int between 0-10
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False) #link to user relation
    review_create_time = db.Column(db.DateTime, nullable=False) #time review was posted