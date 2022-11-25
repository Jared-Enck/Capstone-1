from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField
from wtforms.validators import Length, Optional, DataRequired, Email, URL
from models import db, User, Deck, Comment
    
class RegisterForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired(message='Enter a username.')])
    password = PasswordField('Password', validators=[Length(min=6, message='Password be at least 6 characters.')])
    email = EmailField('Email', validators=[Email(message='Enter a valid email.')])
        
class LoginForm(FlaskForm):
    """Log in user form"""
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])