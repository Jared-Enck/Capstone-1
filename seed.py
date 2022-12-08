from app import db
from models import Card, User, Deck, MainDeckCard, SharedDeck, MainDecklist
import requests

db.drop_all()
db.create_all()

def save_all_cards():
    """Call to API for all cards in series Digimon Card Game and save them to db."""

    resp = requests.get('https://digimoncard.io/api-public/search.php?series=Digimon Card Game')

    cards = resp.json()
    
    for card in cards:
        c = Card(name=card['name'],
                type=card['type'],
                color=card['color'],
                stage=card['stage'],
                digi_type=card['digi_type'], 
                attribute=card['attribute'],
                level=card['level'],
                play_cost=card['play_cost'],
                evolution_cost=card['evolution_cost'],
                cardrarity=card['cardrarity'],
                artist=card['artist'],
                dp=card['dp'],
                cardnumber=card['cardnumber'],
                main_effect=card['maineffect'],
                source_effect=card['soureeffect'],
                set_name=card['set_name'],
                image_url=card['image_url'])
        
        db.session.add(c)
    db.session.commit()
    
def gen_users():
    """Generate users for setting up test decks."""
    
    form1 = {
        'username': 'test_user1',
        'password':'test_user1',
        'email':'testemail1@me.com'
    }
    form2 = {
        'username': 'test_user2',
        'password':'test_user2',
        'email':'testemail2@me.com'
    }
    
    test_user1 = User.register(form1)
    
    test_user2 = User.register(form2)
    
    db.session.add(test_user1)
    db.session.add(test_user2)
    
    db.session.commit()
    
    gen_decks(test_user1)
    gen_decks(test_user2)

def gen_decks(user):
    """Generate test decks for test users."""
    
    main_deck1 = MainDecklist()
    main_deck2 = MainDecklist()
    
    db.session.add(main_deck1)
    db.session.add(main_deck2)
    db.session.commit()
    
    md1_card = MainDeckCard(main_decklist_id=main_deck1.id,m_card_id=21)
    md2_card = MainDeckCard(main_decklist_id=main_deck2.id,m_card_id=19)
    
    db.session.add(md1_card)
    db.session.add(md2_card)
    
    db.session.commit()
    
    deck1 = Deck(name='deck1',user_id=user.id,main_decklist_id=main_deck1.id)
    deck2 = Deck(name='deck2',user_id=user.id,main_decklist_id=main_deck2.id)
    
    db.session.add(deck1)
    db.session.add(deck2)
    
    db.session.commit()

save_all_cards()
gen_users()

