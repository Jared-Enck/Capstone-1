from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
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