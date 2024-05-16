from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.forms import LoginForm, SignUp, Search, CreatePostManual, CreatePostAuto, CreateReview
from app.models import User, Article, Review
from app.database import home_query, create_database, add_album_to_db, add_review_to_db
from flask_login import login_user, logout_user, current_user, login_required


@app.before_request
def run_on_start():
    app.before_request_funcs[None].remove(run_on_start) #removes this function so its only run on startup
    create_database()



@app.route('/')
def root():
    return redirect(location=url_for("home"))

@app.route("/home")
def home():
    search = request.args.get("search")
    sort = request.args.get("sort")
    articles = home_query(search, sort)
    form=Search()
    form3 = CreateReview()
    return render_template("home.html", title="Home", articles=articles, form=form, form3=form3, user=current_user)



@app.route('/article/<int:article_id>')
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


@app.route('/article/<int:article_id>/create_review', methods=['POST'])
def post_review(article_id):
    add_review_to_db(request.form, article_id)
    return redirect(location=url_for("article", article_id=article_id))

@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form1 = CreatePostAuto()
    form2 = CreatePostManual()
    return render_template("create-post.html", title="Create Post",form1=form1, form2=form2)

@app.route('/create-post-auto', methods=['POST'])
def create_post_auto():
    form = CreatePostAuto()
    if form.validate_on_submit():
        #spotify link
        add_album_to_db(request)
        return redirect(location=url_for("home"))
    
@app.route('/create-post-manual', methods=['POST'])
def create_post_manual():
    form = CreatePostManual()
    if form.validate_on_submit():
        #user entry
        add_album_to_db(request)
        return redirect(location=url_for("home"))


#renders the login page (only GET request)
@app.route('/login')
def login():
    form = LoginForm()
    createForm = SignUp()
    redirect = request.args.get('next')
    return render_template('login.html', title='Sign In', form=form, createForm=createForm, redirect=redirect)

#processes sign up post requests
@app.route('/signup', methods=['POST'])
def signup_post():

    form = LoginForm()
    createForm = SignUp()

    if not createForm.validate_on_submit():
        render_template('login.html', title='Sign In', form=form,createForm=createForm)
    
    #add user to database
    username = request.form.get('username')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    if not (password == confirm):
        flash('Passwords do not match','signup_error')
        return redirect(url_for('login'))

    #check if user exists
    existing_user = User.query.filter_by(username=username).first()

    #if user already exists do not create new user with same username
    if existing_user:
        flash('User exists','signup_error')
        return redirect(url_for('login'))

    #if user is new, add to database
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    if request.form.get('remember_me'):
        remember = True
    else:
        remember = False

    login_user(user, remember=remember)

    return redirect(location=url_for("home"))

#processes login post requests
@app.route('/login', methods=['POST'])
def login_post():

    form = LoginForm()
    createForm = SignUp()

    if not form.validate_on_submit():
        render_template('login.html', title='Sign In', form=form,createForm=createForm)

    username = request.form.get('username')
    password = request.form.get('password')

    #check for existing user
    existing_user = User.query.filter_by(username=username).first()

    #if username couldnt be found or the password doesnt match throw an error
    if not existing_user or not existing_user.check_password(password):
        flash('Please check your login details','login_failed')
        return redirect(url_for('login'))

    if request.form.get('remember_me'):
        remember = True
    else:
        remember = False

    login_user(existing_user, remember=remember)
    return redirect(location=url_for("home"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(location=url_for("home"))

@app.errorhandler(404)
def page_not_found(*args):
    return render_template("error-page.html", title="Page Not Found")
