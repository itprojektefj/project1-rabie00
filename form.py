from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):

    user_email = StringField('Email Address', [validators.DataRequired(), Length(min=6, max=35)])
    username = StringField('Username', [validators.DataRequired(), Length(min=4, max=25)])
    password = PasswordField('New Password', [validators.DataRequired(), Length(min=4, max=25)])
    confirm_password = PasswordField('Confirm password', [validators.DataRequired(), EqualTo('password' )])


class LoginForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Email('email')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])


class SearchForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])