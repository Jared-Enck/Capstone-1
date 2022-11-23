from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
DEFAULT_IMG_URL = ''

##### User relationship models. #####

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
    
    @classmethod
    def register(cls, username, password, email, image_url):
        """Register user.
        Hash password and add user to db.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        if image_url and image_url != '':
            user = User(
                username=username,
                email=email,
                password=hashed_pwd,
                image_url=image_url,
            )
        else:
            user = User(
                username=username,
                email=email,
                password=hashed_pwd,
            )

        db.session.add(user)
        
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with entered username and password.
        Returns user obj if username and hashed password match, else returns false.
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
    
    content = db.Column(db.String(200), 
                        nullable=False)
    
    timestamp = db.Column(db.DateTime, 
                          nullable=False, 
                          default=datetime.utcnow())
    
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
    
    @classmethod
    def decklists(cls, card_id):
        """Get decklists associated with card."""
        
        main_decklists = db.session.query(MainDecklist).\
            join(MainDeckCard).filter(
                MainDeckCard.card_id == card_id).all()
        
        return main_decklists
    
class MainDecklist(db.Model):
    """Main decklist."""
    
    __tablename__ = 'main_decklist'
    
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
                             db.ForeignKey('main_decklist.id', 
                             ondelete='cascade'))
    
    m_card_id = db.Column(db.Integer, 
                             db.ForeignKey('cards.id', 
                             ondelete='cascade'))
    
class EggDecklist(db.Model):
    """Egg decklist."""
    
    __tablename__ = 'egg_decklist'
    
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
                             db.ForeignKey('egg_decklist.id', 
                             ondelete='cascade'))
    
    e_card_id = db.Column(db.Integer, 
                             db.ForeignKey('cards.id', 
                             ondelete='cascade'))
    
class SideDecklist(db.Model):
    """Side decklist."""
    
    __tablename__ = 'side_decklist'
    
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
                             db.ForeignKey('side_decklist.id', 
                             ondelete='cascade'))
    
    e_card_id = db.Column(db.Integer, 
                             db.ForeignKey('cards.id', 
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
                        db.ForeignKey('users.id', 
                                      ondelete='cascade'))

    main_decklist_id = db.Column(db.Integer, 
                        db.ForeignKey('main_decklist.id', 
                                      ondelete='cascade'))

    egg_decklist_id = db.Column(db.Integer, 
                        db.ForeignKey('egg_decklist.id', 
                                      ondelete='cascade'))

    side_decklist_id = db.Column(db.Integer, 
                        db.ForeignKey('side_decklist.id', 
                                      ondelete='cascade'))