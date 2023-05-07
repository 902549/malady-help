from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from SearchWebsite.Model import User

class RegistrationForm(FlaskForm):
    username =StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])

    confirmpassword = PasswordField('ConfirmPassword', 
                                    validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign-up')

    #Checking if the username still exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different username.')
    
    #Checking if the email still exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different email.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class QueryForm(FlaskForm):
    query = StringField('Search', validators= [DataRequired()])
    submit = SubmitField('Search')