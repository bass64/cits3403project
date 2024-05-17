from app import db
from app.blueprints import main
from flask import render_template, redirect, url_for, request, flash
from app.forms import LoginForm, SignUp, Search, CreatePostManual, CreatePostAuto, PostReview
from app.models import User, Article, Review
from app.database import home_query, create_database, add_album_to_db, add_review_to_db
from flask_login import login_user, logout_user, current_user, login_required
from app.controllers import sign_user_up, SignUpError, log_user_in, LoginError


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html", title="Testpage")



@main.route('/')
@main.route("/home")
def home():
    search = request.args.get("search")
    sort = request.args.get("sort")
    articles = home_query(search, sort)
    form=Search()
    return render_template("home.html", title="Home", articles=articles, form=form, user=current_user)



@main.route('/article/<int:article_id>')
def article(article_id):
    album = db.session.query(Article, User).join(User, User.user_id == Article.user_id).filter(Article.album_id == article_id).first()
    reviews = db.session.query(Review, User).join(User, User.user_id == Review.user_id).filter(Review.album_id == article_id).all()
    return render_template("article_full.html", 
                           title = "" + album.Article.album_artist + " - " + album.Article.album_title, 
                           album=album, 
                           reviews=reviews, 
                           full=True, 
                           user="test") #need to figure out how sibi implemented this


#@main.route('/article/<int:article_id>/post_review', methods=['POST'])
#def post_review(article_id):
#    form = PostReview()
#    if form.validate_on_submit():
#        add_review_to_db(request, article_id)
#        return redirect(location=url_for("main.article/<int:article_id>"))

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
    
@main.route('/create-post-manual', methods=['POST'])
def create_post_manual():
    form = CreatePostManual()
    if form.validate_on_submit():
        #user entry
        print(request.form.get("image"))
        add_album_to_db(request)
        return redirect(location=url_for("main.home"))



@main.route('/post-review')
@login_required
def post_review():
    return render_template("post-review.html", title="Post Review")



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

@main.route("/<path:invalid_path>")
def page_not_found(invalid_path):
    return render_template("error-page.html", title="Page Not Found")