from flask_sqlalchemy import SQLAlchemy

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
    
    
    
##### Deck relationship models. #####

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