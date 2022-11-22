from app import db
import requests
from models import Card

db.drop_all()
db.create_all()
    
def save_all_cards():
    
    resp = requests.get('https://digimoncard.io/api-public/getAllCards.php?sort=name')
    
    cards = resp.json()
    
    for card in cards:
        c = Card(name=card['name'], 
                 number=card['cardnumber']
                 )
        
        db.session.add(c)

    db.session.commit()
    
save_all_cards()