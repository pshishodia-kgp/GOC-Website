from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from goc.models import User

class SignUpForm(FlaskForm):
    username = StringField('Username (Codeforces)', validators=[DataRequired(), Length(max=60)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username has already been taken.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email has already been taken.')

class LoginForm(FlaskForm):
    username_or_email = StringField('Username/Email', validators=[DataRequired(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80)])
    submit = SubmitField('Log In')

    def validate(self, username_or_email, password):
        user1 = User.query.filter_by(username=username_or_email.data, password=password.data).first()
        user2 = User.query.filter_by(username=username_or_email.data, password=password.data).first()
        if (not user1) and (not user2):
            raise ValidationError('Login Failed. Please check username/email and password.')
