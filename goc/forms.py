from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from goc.models import User
import requests

class SignUpForm(FlaskForm):
    username = StringField('Username (Codeforces)', validators=[DataRequired(), Length(max=60)])
    email = StringField('Gmail', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    user_data = {}

    def validate_username(self, username): 
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username has already been taken.')

    def validate_email(self, email): 
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email has already been taken.')

    def validate(self):
        if not FlaskForm.validate(self): 
            return False

        username_errors, email_errors = [], []

        url = 'https://codeforces.com/api/user.info?handles=' + str(self.username.data)
        data = requests.get(url).json()

        print(data)

        if(data['status'] == "FAILED"):
            username_errors.append('Invalid Username. Please provide a valid codeforces username')
        elif('email' not in data['result'][0]):
            email_errors.append('Email Address not yet public on codeforces')
        else: 
            email = data['result'][0]['email']
            if email != str(self.email.data) : 
                email_errors.append('Email address is different than on codeforces')

        if len(username_errors) > 0 or len(email_errors) > 0: 
            self.username.errors = tuple(username_errors)
            self.email.errors = tuple(email_errors)
            return False
        return True

class LoginForm(FlaskForm):
    username_or_email = StringField('Username/Email', validators=[DataRequired(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80)])
    submit = SubmitField('Log In')