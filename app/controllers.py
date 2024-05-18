from app.models import User
from app import db
from flask_login import login_user

class SignUpError(Exception):
    pass

class LoginError(Exception):
    pass

def sign_user_up(username, password, confirm, remember):

    if not (password == confirm):
        raise SignUpError("Passwords do not match")
    
    if len(password) < 8:
        raise SignUpError("Password must have at least 8 characters")

    contains_upper = False
    for letter in password:
        if letter.isupper():
            contains_upper = True
            break

    if not contains_upper:
        raise SignUpError("Password must have at least one upper case character", "signup_error")

    contains_digit = False
    for letter in password:
        if letter.isdigit():
            contains_digit = True
            break

    if not contains_digit:
        raise SignUpError("Password must have at least one number")
    
    #check if user exists
    existing_user = User.query.filter_by(username=username).first()

    #if user already exists do not create new user with same username
    if existing_user:
        raise SignUpError("User exists")
    
    #if user is new, add to database
    user = User(username=username)
    user.set_password(password)
    user.following_articles = []
    db.session.add(user)
    db.session.commit()

    login_user(user, remember=remember)

def log_user_in(username, password, remember):
    #check for existing user
    existing_user = User.query.filter_by(username=username).first()

    #if username couldnt be found or the password doesnt match throw an error
    if not existing_user or not existing_user.check_password(password):
        raise LoginError("Please check your login details")

    login_user(existing_user, remember=remember)