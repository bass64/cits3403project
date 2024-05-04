from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField,TextAreaField,DateField

from wtforms.validators import DataRequired, EqualTo, InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignUp(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirm  = PasswordField('Repeat Password',[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')

class Search(FlaskForm):
    search = StringField("Search", render_kw={"placeholder": "Search..."})
    sort = SelectField("Sort by", choices=[
        ("album_create_time DESC", "Sort by newest"),
        ("album_create_time ASC", "Sort by oldest"),
        ("album_rating DESC", "Sort by highest rating"),
        ("album_rating ASC", "Sort by lowest rating"),
        ("album_rating_no + album_review_no DESC", "Sort by most ratings"),
        ("album_rating_no + album_review_no ASC", "Sort by least ratings"),
    ])
    submit = SubmitField()

class CreatePostManual(FlaskForm):
    type = SelectField("Type: ", choices=[("Album", "Album"), ("EP", "EP"), ("Single", "Single")])
    title = StringField('Title: ',name="title",validators=[DataRequired()])
    artist = StringField('Artist/Band Name: ',name="artist",validators=[DataRequired()])
    image = FileField('Upload Image: ',name="image",validators=[FileRequired(),FileAllowed(['jpg', 'png'], 'Images only!')])
    date = DateField('Release Date: ',name="date",validators=[InputRequired()])
    submit = SubmitField('Submit')

class CreatePostAuto(FlaskForm):
    url = StringField('Spotify URL: ',name="url",validators=[DataRequired()])
    submit = SubmitField('Submit')
