from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
DEFAULT_IMG_URL = '/static/digi_avatars/blank-digivice.gif'

##### User relationship models. #####

class User(db.Model, UserMixin):
    """User."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    username = db.Column(db.String(20), 
                         nullable=False, 
                         unique=True)
    
    password = db.Column(db.String(), 
                         nullable=False)
    
    email = db.Column(db.String(), 
                      nullable=False,
                      unique=True)
    
    avatar = db.Column(db.String, 
                          nullable=True, 
                          default=DEFAULT_IMG_URL)
        
    decks = relationship('Deck', backref='users')
    
    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"
    
    @classmethod
    def register(cls, form):
        """Register user.
        Hash password and add user to db.
        """

        hashed_pwd = bcrypt.generate_password_hash(form['password']).decode('UTF-8')

        user = User(
            username=form['username'],
            password=hashed_pwd,
            email=form['email'],
            avatar=DEFAULT_IMG_URL
        )

        db.session.add(user)
        db.session.commit()
        
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with entered username and password.
        Returns true if username and hashed password match, else returns false.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Comment(db.Model):
    """Comment."""
    
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    user_id = db.Column(db.Integer, 
                        ForeignKey('users.id', 
                                      ondelete='cascade'))
    
    timestamp = db.Column(db.DateTime, 
                          nullable=False, 
                          default=datetime.utcnow())
    
    content = db.Column(db.String(200), 
                        nullable=False)
    
    shared_deck_id = db.Column(db.Integer, 
                        ForeignKey('shared_decks.id', 
                                      ondelete='cascade'))
    
    user = relationship('User', backref='comments')
    
    deck = relationship('SharedDeck', backref='comments')
    
    def __repr__(self):
        return f"<Comment #{self.id}: {self.user.username}, {self.timestamp}, {self.content}>"
    
class CommentLikes(db.Model):
    """Mapping user likes to comments."""
    
    __tablename__ = 'comment_likes'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    comment_id = db.Column(db.Integer, 
                        ForeignKey('comments.id', 
                                      ondelete='cascade'))
    
    user_id = db.Column(db.Integer, 
                        ForeignKey('users.id', 
                                      ondelete='cascade'))
    
class UserComment(db.Model):
    """User comments."""
    
    __tablename__ = 'user_comments'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    comment_id = db.Column(db.Integer, 
                        ForeignKey('comments.id', 
                                      ondelete='cascade'))
    
    user_id = db.Column(db.Integer, 
                        ForeignKey('users.id', 
                                      ondelete='cascade'))
    
class SharedDeck(db.Model):
    """Deck shared with others by user."""
    
    __tablename__ = 'shared_decks'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    deck_id = db.Column(db.Integer, 
                        ForeignKey('decks.id', 
                                      ondelete='cascade'))
    
    user_id = db.Column(db.Integer, 
                        ForeignKey('users.id', 
                                      ondelete='cascade'))
    
    timestamp = db.Column(db.DateTime, 
                          nullable=False, 
                          default=datetime.utcnow())
    
    user = relationship('User', backref='shared_decks')
        
    likes = db.relationship('User',
                            secondary='deck_likes')
    
    @classmethod
    def get_deck_comments(cls, shared_deck_id):
        """Get all comments for the shared deck."""
        
        comments = db.session.query(Comment).filter(
                Comment.shared_deck_id == shared_deck_id
            ).all()
        
        return comments
    
class DeckLikes(db.Model):
    """Mapping user likes to shared decks."""
    
    __tablename__ = 'deck_likes'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    shared_deck_id = db.Column(db.Integer, 
                        ForeignKey('shared_decks.id', 
                                      ondelete='cascade'))
    
    user_id = db.Column(db.Integer, 
                        ForeignKey('users.id', 
                                      ondelete='cascade'))
    
##### Deck relationship models. #####

class Card(db.Model):
    """Card."""
    
    __tablename__ = 'cards'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    name = db.Column(db.Text, 
                     nullable=False)
    type = db.Column(db.Text, 
                     nullable=False)
    color = db.Column(db.Text, 
                      nullable=False)
    stage = db.Column(db.Text, 
                      nullable=True)
    digi_type = db.Column(db.Text, 
                          nullable=True)
    attribute = db.Column(db.Text, 
                          nullable=True)
    level = db.Column(db.Text, 
                      nullable=True)
    play_cost = db.Column(db.Integer, 
                          nullable=True)
    evolution_cost = db.Column(db.Text, 
                               nullable=True)
    cardrarity = db.Column(db.Text, 
                           nullable=True)
    artist = db.Column(db.Text, 
                       nullable=True)
    dp = db.Column(db.Text, 
                   nullable=True)
    cardnumber = db.Column(db.Text, 
                           nullable=False)
    maineffect = db.Column(db.Text, 
                           nullable=True)
    soureeffect = db.Column(db.Text, 
                            nullable=True)
    set_name = db.Column(db.Text, 
                         nullable=False)
    image_url = db.Column(db.Text, 
                          nullable=False)
    
    def __repr__(self):
        return f"<Card #{self.id}: {self.name}, {self.color}, {self.cardnumber}>"
    
    @classmethod
    def decklists(cls, card_id):
        """Get decklists associated with card."""
        
        main_decklists = db.session.query(MainDecklist).\
            join(MainDeckCard).filter(
                MainDeckCard.card_id == card_id).all()
        
        return main_decklists
    
class MainDecklist(db.Model):
    """Main decklist."""
    
    __tablename__ = 'main_decklists'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    @classmethod
    def main_cards(cls, main_decklist_id):
        """Get all cards in main decklist."""
        
        m_cards = db.session.query(Card).\
            join(MainDeckCard).filter(
                MainDeckCard.main_decklist_id == main_decklist_id
            ).all()
        
        return m_cards
        
class MainDeckCard(db.Model):
    """Card assigned to a main deck id."""
    
    __tablename__ = 'main_deck_cards'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    main_decklist_id = db.Column(db.Integer, 
                             ForeignKey('main_decklists.id', 
                             ondelete='cascade'))
    
    m_card_id = db.Column(db.Integer, 
                             ForeignKey('cards.id', 
                             ondelete='cascade'))
    
class EggDecklist(db.Model):
    """Egg decklist."""
    
    __tablename__ = 'egg_decklists'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    @classmethod
    def egg_cards(cls, egg_decklist_id):
        """Get all cards in egg decklist."""
        
        cards = db.session.query(Card).\
            join(EggDeckCard).filter(
                EggDeckCard.egg_decklist_id == egg_decklist_id
            ).all()
        
        return cards
        
class EggDeckCard(db.Model):
    """Card assigned to a egg deck id."""
    
    __tablename__ = 'egg_deck_cards'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    egg_decklist_id = db.Column(db.Integer, 
                             ForeignKey('egg_decklists.id', 
                             ondelete='cascade'))
    
    e_card_id = db.Column(db.Integer, 
                             ForeignKey('cards.id', 
                             ondelete='cascade'))
    
class SideDecklist(db.Model):
    """Side decklist."""
    
    __tablename__ = 'side_decklists'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    @classmethod
    def side_cards(cls, side_decklist_id):
        """Get all cards in side decklist."""
        
        s_cards = db.session.query(Card).\
            join(SideDeckCard).filter(
                SideDeckCard.side_decklist_id == side_decklist_id
            ).all()
        
        return s_cards
        
class SideDeckCard(db.Model):
    """Card assigned to a side deck id."""
    
    __tablename__ = 'side_deck_cards'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    side_decklist_id = db.Column(db.Integer, 
                             ForeignKey('side_decklists.id', 
                             ondelete='cascade'))
    
    e_card_id = db.Column(db.Integer, 
                             ForeignKey('cards.id', 
                             ondelete='cascade'))

class Deck(db.Model):
    """Deck."""
    
    __tablename__ = 'decks'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    name = db.Column(db.String(30), 
                     nullable=False)
    
    user_id = db.Column(db.Integer, 
                        ForeignKey('users.id', 
                                      ondelete='cascade'))

    main_decklist_id = db.Column(db.Integer, 
                        ForeignKey('main_decklists.id', 
                                      ondelete='cascade'))

    egg_decklist_id = db.Column(db.Integer, 
                        ForeignKey('egg_decklists.id', 
                                      ondelete='cascade'))

    side_decklist_id = db.Column(db.Integer, 
                        ForeignKey('side_decklists.id', 
                                      ondelete='cascade'))
    
    def __repr__(self):
        return f"<Deck #{self.id}: {self.name}, {self.user_id}>"