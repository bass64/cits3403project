from app import db
from app.blueprints import main
from flask import render_template, redirect, url_for, request, flash
from app.forms import LoginForm, SignUp, Search, CreatePostManual, CreatePostAuto, CreateReview
from app.models import User, Article, Review, followingTable
from app.database import home_query, create_database, add_album_to_db, add_review_to_db
from flask_login import login_user, logout_user, current_user, login_required
from app.controllers import sign_user_up, SignUpError, log_user_in, LoginError
from sqlalchemy import and_


@main.route('/')
@main.route("/home")
def home():
    search = request.args.get("search")
    sort = request.args.get("sort")
    articles = home_query(search, sort)
    form=Search()
    form3 = CreateReview()
    return render_template("home.html", title="Home", articles=articles, form=form, form3=form3, user=current_user)



@main.route('/article/<int:article_id>')
def article(article_id):
    form3 = CreateReview()
    album = db.session.query(Article, User).join(User, User.user_id == Article.user_id).filter(Article.album_id == article_id).first()
    reviews = db.session.query(Review, User).join(User, User.user_id == Review.user_id).filter(Review.album_id == article_id).all()
    return render_template("article_full.html", 
                           title = "" + album.Article.album_artist + " - " + album.Article.album_title, 
                           album=album, 
                           reviews=reviews, 
                           full=True, 
                           user=current_user,
                           form3=form3)


@main.route('/article/<int:article_id>/create_review', methods=['POST'])
def post_review(article_id):
    error = add_review_to_db(request.form, article_id)
    if error == "duplicate user":
        #TODO handle error when user posts multiple reivews
        return redirect(location=url_for("main.article", article_id=article_id, error="duplicate user"))
    return redirect(location=url_for("main.article", article_id=article_id))
  

@main.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form1 = CreatePostAuto()
    form2 = CreatePostManual()
    return render_template("create-post.html", title="Create Post",form1=form1, form2=form2)

@main.route('/create-post-auto', methods=['POST'])
def create_post_auto():
    form = CreatePostAuto()
    if form.validate_on_submit():
        #spotify link
        add_album_to_db(request)
        return redirect(location=url_for("main.home"))
    #if didn't validate, send back to create post
    #TODO handle this error
    return redirect(location=url_for("main.create_post", error="invalid post"))
  
    
@main.route('/create-post-manual', methods=['POST'])
def create_post_manual():
    form = CreatePostManual()
    if form.validate_on_submit():
        #user entry
        add_album_to_db(request)
        return redirect(location=url_for("main.home"))
    #if didn't validate, send back to create post
    #TODO handle this error
    return redirect(location=url_for("main.create_post", error="invalid post"))

#follows an article if the user is logged in
@main.route('/follow_article', methods=['POST'])
@login_required
def follow_article():
    article_id = request.form.get('article_id')
    article = Article.query.filter_by(album_id=article_id).first()
    current_user.following_articles.append(article)
    db.session.commit()

    #redirect to the site that sent the follow request (either article full or home)
    return redirect(request.referrer)

@main.route('/unfollow_article', methods=['POST'])
@login_required
def unfollow_article():
    article_id = request.form.get('article_id')
    article = Article.query.filter_by(album_id=article_id).first()
    current_user.following_articles.remove(article)
    db.session.commit()
    
    #redirect to the site that sent the follow request (either article full or home)
    return redirect(request.referrer)

#renders the login page (only GET request)
@main.route('/login')
def login():
    form = LoginForm()
    createForm = SignUp()
    redirect = request.args.get('next')
    return render_template('login.html', title='Sign In', form=form, createForm=createForm, redirect=redirect)

#processes sign up post requests
@main.route('/signup', methods=['POST'])
def signup_post():

    form = LoginForm()
    createForm = SignUp()

    if not createForm.validate_on_submit():
        render_template('login.html', title='Sign In', form=form,createForm=createForm)
    
    #add user to database
    username = request.form.get('username')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    if request.form.get('remember_me'):
        remember = True
    else:
        remember = False

    try:
        sign_user_up(username,password,confirm, remember)
    except SignUpError as e:
        flash(e.message, 'signup_error')
        return redirect(url_for('main.login'))

    return redirect(location=url_for("main.home"))

#processes login post requests
@main.route('/login', methods=['POST'])
def login_post():

    form = LoginForm()
    createForm = SignUp()

    if not form.validate_on_submit():
        render_template('login.html', title='Sign In', form=form,createForm=createForm)

    username = request.form.get('username')
    password = request.form.get('password')

    if request.form.get('remember_me'):
        remember = True
    else:
        remember = False

    try:
        log_user_in(username, password, remember)
    except LoginError as e:
        flash(e.message,'login_failed')
        return redirect(url_for('main.login'))
        
    return redirect(location=url_for("main.home"))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(location=url_for("main.home"))


@main.route('/following')
@login_required
def following():
    #query = db.session.query(Article, User).join(User, User.user_id == Article.user_id)
    query = db.session.query(Article, User).join(User, User.user_id == Article.user_id).join(followingTable, and_(followingTable.c.user_id == User.get_id(current_user), followingTable.c.album_id == Article.album_id))
    return render_template("following.html", title="Following", query=query)
  
@main.route("/<path:invalid_path>")
def page_not_found(invalid_path):
    return render_template("error-page.html", title="Page Not Found")

