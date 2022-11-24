from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from wtforms import PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length, Optional
from models import db, User, Deck, Comment

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session
    
class RegisterForm(ModelForm):
    class Meta:
        model = User
        password = PasswordField(validators=[Length(min=6)])
        
class LoginForm(ModelForm):
    class Meta:
        model = User
        only = ['username', 'password']