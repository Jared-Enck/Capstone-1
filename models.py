from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
DEFAULT_IMG_URL = ''

class Card(db.Model):
    """Card."""
    
    __tablename__ = 'cards'
    
    id = db.Column(db.Integer,  
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.Text, 
                     nullable=False)
    
    number = db.Column(db.Text, 
                       nullable=False)
    
    
class User(db.Model):
    """User."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    username = db.Column(db.String(20), 
                         nullable=False, 
                         unique=True)
    
    password = db.Column(db.Text, 
                         nullable=False)
    
    email = db.Column(db.Text, 
                      nullable=False, 
                      unique=True)
    
    image_url = db.Column(db.Text, 
                          nullable=False, 
                          default=DEFAULT_IMG_URL)
    
class Deck(db.Model):
    """Deck."""
    
    __tablename__ = 'decks'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    name = db.Column(db.String(30), 
                     nullable=False)
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id', ondelete='cascade'))