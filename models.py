from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from operator import attrgetter

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
DEFAULT_IMG_URL = '/static/digi_avatars/botamon.gif'

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
        
    decks = relationship('Deck', 
                         secondary='user_decks')
    
    comments = relationship('Comment', 
                            secondary='user_comments')
    
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
    
    deck = relationship('Deck', backref='shared_decks')
    
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
                           primary_key=True,
                           nullable=False)
    main_effect = db.Column(db.Text, 
                           nullable=True)
    source_effect = db.Column(db.Text, 
                            nullable=True)
    set_name = db.Column(db.Text, 
                         nullable=False)
    image_url = db.Column(db.Text, 
                          nullable=False)
    
    def __repr__(self):
        return f"<Card: {self.name}, {self.color}, {self.cardnumber}>"
    
    @classmethod
    def decklists(cls, card_num):
        """Get decklists associated with card."""
        
        main_decklists = db.session.query(MainDecklist).\
            join(MainDeckCard).filter(
                MainDeckCard.m_card_num == card_num).all()
        
        return main_decklists
    
    def get_detail_stats(card):
        """Returns dictionary for stats obj"""
        
        stat_obj = list({'Color': card.color,
                    'Type': card.type,
                    'Stage': card.stage,
                    'DP': card.dp,
                    'Level': card.level,
                    'Play Cost': card.play_cost,
                    'Attribute': card.attribute,
                    'Number': card.cardnumber,
                    'Rarity': card.cardrarity}.items())

        return [ stat_obj[0:3], stat_obj[3:6], stat_obj[6:] ]
    
    def serialize_stats(self):
        """Serialize card stats for deck builder."""
        
        return {
            'name': self.name,
            'type': self.type,
            'color': self.color,
            'play_cost': self.play_cost,
            'cardnumber': self.cardnumber,
            'main_effect': self.main_effect,
            'image_url': self.image_url
        }
        
    
class MainDecklist(db.Model):
    """Main decklist."""
    
    __tablename__ = 'main_decklists'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    def main_cards(main_decklist_id):
        """Get all cards in main decklist."""
        
        m_cards = db.session.query(Card).join(MainDeckCard).filter(
                MainDeckCard.main_decklist_id == main_decklist_id
            ).all()
        
        return m_cards
    
    def highest_dp_card_img(main_cards):
        """Get highest dp card in main cards."""
        
        dp_sorted_cards = [card for card in main_cards if card.type == 'Digimon']
        
        hdp_card = max(dp_sorted_cards, key=attrgetter('dp'))
        
        return hdp_card.image_url
        
class MainDeckCard(db.Model):
    """Card assigned to a main deck id."""
    
    __tablename__ = 'main_deck_cards'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    main_decklist_id = db.Column(db.Integer, 
                             ForeignKey('main_decklists.id', 
                             ondelete='cascade'))
    
    m_card_num = db.Column(db.Text, 
                           ForeignKey('cards.cardnumber'))
    qty = db.Column(db.Integer)
    
class EggDecklist(db.Model):
    """Egg decklist."""
    
    __tablename__ = 'egg_decklists'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    def egg_cards(egg_decklist_id):
        """Get all cards in egg decklist."""
        
        e_cards = db.session.query(Card).join(EggDeckCard).filter(
                EggDeckCard.egg_decklist_id == egg_decklist_id
            ).all()
        
        return e_cards
        
class EggDeckCard(db.Model):
    """Card assigned to a egg deck id."""
    
    __tablename__ = 'egg_deck_cards'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    egg_decklist_id = db.Column(db.Integer, 
                             ForeignKey('egg_decklists.id', 
                             ondelete='cascade'))
    
    e_card_num = db.Column(db.Text, 
                           ForeignKey('cards.cardnumber'))
    qty = db.Column(db.Integer)
    
class SideDecklist(db.Model):
    """Side decklist."""
    
    __tablename__ = 'side_decklists'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    def side_cards(side_decklist_id):
        """Get all cards in side decklist."""
        
        s_cards = db.session.query(Card).join(SideDeckCard).filter(
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
    
    s_card_num = db.Column(db.Text, 
                           ForeignKey('cards.cardnumber'))
    qty = db.Column(db.Integer)

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
    
    HDP_deck_img = db.Column(db.Text)
    
    def __repr__(self):
        return f"<Deck #{self.id}: {self.name}, {self.user_id}>"
    
    def serialize_deck(self):
        """Deck obj to dict."""
        
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'main_decklist_id': self.main_decklist_id,
            'egg_decklist_id': self.egg_decklist_id,
            'side_decklist_id': self.side_decklist_id,
            'HDP_deck_img': self.HDP_deck_img
        }
    
    def user_decks(current_user):
        """Get all decks for current user."""
        
        decks = Deck.query.filter(Deck.user_id == current_user.id).all()
        
        return decks
    
    def create_decklists():
        """Create decklists for main, egg, and side."""
        
        MD = MainDecklist()
        ED = EggDecklist()
        SD = SideDecklist()
        
        db.session.add(MD)
        db.session.add(ED)
        db.session.add(SD)
        
        db.session.commit()
        
        return {
            'main_id': MD.id,
            'egg_id': ED.id,
            'side_id': SD.id
        }
        
    def generate_decklist_cards(decklists, deck_obj):
        """Save cards to each decklist."""

        m_deck = deck_obj['decklist']['mainDeck']
        e_deck = deck_obj['decklist']['eggDeck']
        s_deck = deck_obj['decklist']['sideDeck']
        
        for card_num, qty in m_deck.items():
            
            m_card = MainDeckCard(main_decklist_id=decklists['main_id'], m_card_num=card_num, qty=qty)
            
            db.session.add(m_card)
        
        if e_deck:
            
            for card_num, qty in e_deck.items():
                e_card = EggDeckCard(egg_decklist_id=decklists['egg_id'], e_card_num=card_num,qty=qty)
                
                db.session.add(e_card)
        
        if s_deck:
        
            for card_num, qty in s_deck.items():
                s_card = SideDeckCard(side_decklist_id=decklists['side_id'], s_card_num=card_num,qty=qty)
                
                db.session.add(s_card)

        db.session.commit()
    
class UserDeck(db.Model):
    """User decks."""
    
    __tablename__ = 'user_decks'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    deck_id = db.Column(db.Integer, 
                        ForeignKey('decks.id', 
                                      ondelete='cascade'))
    
    user_id = db.Column(db.Integer, 
                        ForeignKey('users.id', 
                                      ondelete='cascade'))