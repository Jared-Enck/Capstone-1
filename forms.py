from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField, SelectField
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
    
class AdvancedSearchForm(FlaskForm):
    """Search API for cards with specified params and return card data."""
    
    color_choices = [('Black','Black'),
                     ('Blue','Blue'),
                     ('Colorless','Colorless'),
                     ('Green','Green'),
                     ('Purple','Purple'),
                     ('Red','Red'),
                     ('White','White'),
                     ('Yellow','Yellow')]
    
    type_choices = [('Digimon','Digimon'), 
                    ('Digi-Egg','Digi-Egg'),
                    ('Option','Option'),
                    ('Tamer','Tamer')]
    
    level_choices = [('2','2'),
                     ('3','3'),
                     ('4','4'),
                     ('5','5'),
                     ('6','6'),
                     ('7','7')]
    
    attr_choices = [('Data','Data'),
                     ('Free','Free'),
                     ('Vaccine','Vaccine'),
                     ('Variable','Variable'),
                     ('Virus','Virus')]
    
    color = SelectField('Color', choices=color_choices)
    type = SelectField('Type', choices=type_choices)
    level = SelectField('Level', choices=level_choices)
    attr = SelectField('Attribute', choices=attr_choices)
    
    search = StringField('Search by card name')