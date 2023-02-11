from flask_wtf.file import FileRequired
from wtforms import StringField, validators, PasswordField, TextAreaField, EmailField, DateField, FileField, \
    SelectField, SubmitField
from wtforms import Form
from wtforms.validators import DataRequired, Email, InputRequired
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name_user = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class PictureForm(Form):
    name_pick = StringField('', validators=[DataRequired()])
    genre = StringField('', validators=[DataRequired()])
    date_of_create = DateField('', validators=[DataRequired()])
    picture_image = FileField()
    #path_pick = FileField('')///


class AuctionForm(FlaskForm):
    date_of_action = DateField('', validators=[DataRequired()])


class ReviewForm(FlaskForm):
    message = StringField('', validators=[DataRequired()])


class ApplicationForm(FlaskForm):
    variant = SelectField('Role', coerce=int, choices = [
    (0, 'Author'),
    (1, 'Owner'),
        (2, 'Actioneer'),
        (3, 'Reviewer')])
    submit = SubmitField("Отпарвить", id='btn1')


class AuctionPictureForm(FlaskForm):
    cost = StringField('', validators=[DataRequired()])


class RevForm(FlaskForm):
    message = StringField('', validators=[DataRequired()])


class AppDetails(Form):
    group_id = SelectField('', coerce=int)


class OwnerForm(FlaskForm):
    variant = SelectField('Auction', coerce=int, validators = [InputRequired()])
    submit = SubmitField("Отпарвить", id='btn1')


