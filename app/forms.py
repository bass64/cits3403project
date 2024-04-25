from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField,TextAreaField,DateField
from wtforms.validators import DataRequired,EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignUp(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirm  = PasswordField('Repeat Password',[DataRequired(),EqualTo('password', message='Passwords must match')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CreatePost(FlaskForm):
    songTitle = StringField('Song Title: ',name="songtitle",validators=[DataRequired()])
    author = StringField('Artist/Band Name: ',name="author",validators=[DataRequired()])
    songFile = FileField('Upload your song: ',name="songfile",validators=[FileRequired(),FileAllowed(['wav', 'mp3'], 'Audio only!')])
    imageFile = FileField('Upload Image: ',name="imagefile",validators=[FileRequired(),FileAllowed(['jpg', 'png'], 'Images only!')])
    description = TextAreaField('Description: ',name="desc",validators=[DataRequired()])
    date = DateField('Release Date: ',name="rdate",validators=[DataRequired()])
    language = SelectField(u'Language: ',name="language",choices=[('en', 'English'), ('es', 'Spanish'), ('vi', 'Vietnamese')],validate_choice=True)
    submit = SubmitField('Submit')