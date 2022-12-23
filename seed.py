from app import db
from models import Card
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

save_all_cards()

