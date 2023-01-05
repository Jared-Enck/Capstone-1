from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField, SelectField
from wtforms.validators import Length, Optional, DataRequired, Email

class RegisterForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired(message='Enter a username.'), Length(max=20)])
    password = PasswordField('Password', validators=[Length(min=6, message='Password be at least 6 characters.')])
    email = EmailField('Email', validators=[Email(message='Enter a valid email.')])
        
class LoginForm(FlaskForm):
    """Log in user form"""
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    
class AdvancedSearchForm(FlaskForm):
    """Search API for cards with specified params and return card data."""
    
    color_choices = [('','Select Color'),
                     ('Black','Black'),
                     ('Blue','Blue'),
                     ('Colorless','Colorless'),
                     ('Green','Green'),
                     ('Purple','Purple'),
                     ('Red','Red'),
                     ('White','White'),
                     ('Yellow','Yellow')]
    
    type_choices = [('','Select Type'),
                    ('Digimon','Digimon'), 
                    ('Digi-Egg','Digi-Egg'),
                    ('Option','Option'),
                    ('Tamer','Tamer')]
    
    attr_choices = [('','Select Attribute'),
                    ('Data','Data'),
                     ('Free','Free'),
                     ('Vaccine','Vaccine'),
                     ('Variable','Variable'),
                     ('Virus','Virus')]
    
    sort_choices = [('','Sort By'),
                    ('name','Name'),
                     ('power','Power'),
                     ('code','Code'),
                     ('color','Color')]
    
    color = SelectField('Color', choices=color_choices, default='Select Color')
    type = SelectField('Type', choices=type_choices, default='Select Type')
    attribute = SelectField('Attribute', choices=attr_choices, default='Select Attribute')
    sort = SelectField('Sort', choices=sort_choices, default='Sort By')
        
class EditUserForm(FlaskForm):
    """Edit user info form."""
    
    username = StringField('Username', validators=[DataRequired(message='Enter a username.')])
    email = EmailField('Email', validators=[Email(message='Enter a valid email.')])
    
    choices = [('/static/digi_avatars/agumon.gif','Agumon'),
               ('/static/digi_avatars/angemon.jpg','Angemon'),
               ('/static/digi_avatars/angewoman.png','Angewomon'),
               ('/static/digi_avatars/bit-agumon.gif','Bit-Agumon'),
               ('/static/digi_avatars/biyomon.gif','Biyomon'),
               ('/static/digi_avatars/blank-digivice.gif','Digivice'),
               ('/static/digi_avatars/botamon.gif','Botamon'),
               ('/static/digi_avatars/gomamon.gif','Gomamon'),
               ('/static/digi_avatars/jesmon.jpg','Jesmon'),
               ('/static/digi_avatars/ladydevimon.jpg','LadyDevimon'),
               ('/static/digi_avatars/metalgreymon.png','MetalGreymon'),
               ('/static/digi_avatars/omegamon.jpg','Omnimon'),
               ('/static/digi_avatars/palmon.gif','Palmon'),
               ('/static/digi_avatars/patamon.gif','Patamon'),
               ('/static/digi_avatars/tentamon.gif','Tentamon'),
               ('/static/digi_avatars/wargreymon.jpg','WarGreymon')]
    
    avatar = SelectField('Avatar', choices=choices, validators=[Optional()])