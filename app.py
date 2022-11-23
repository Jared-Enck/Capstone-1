from flask_cors import CORS
from flask import Flask, redirect, render_template, request, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Card, MainDecklist, MainDeckCard, EggDecklist, EggDeckCard, SideDecklist, SideDeckCard, Deck

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///digimon_tcg_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '3f44cd49d69e821aa140f13a49f432b073e311a264583ab7ed4340b714da0db8'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)

BASE_API_URL_1 = 'https://digimoncard.io/api-public/search.php?'

@app.route('/')
def homepage():
    """Show homepage."""
    
    return render_template('index.html')