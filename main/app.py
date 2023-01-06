from flask_cors import CORS
from flask import Flask, redirect, render_template, request, flash, jsonify, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_debugtoolbar import DebugToolbarExtension
from .models import db, connect_db, User, Card, MainDecklist, EggDecklist, SideDecklist, Deck, SharedDeck, MainDeckCard, EggDeckCard, SideDeckCard, DeckLikes
from .forms import RegisterForm, LoginForm, EditUserForm,AdvancedSearchForm
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.curdir), 'instance'), instance_relative_config=True)

app.config.from_pyfile('config.py')

CORS(app)

toolbar = DebugToolbarExtension(app)

connect_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

@login_manager.unauthorized_handler
def unauthorized():
    flash('Please login first.', 'danger')
    
    return redirect(url_for('login'))

login_manager.login_view = 'login'

app.jinja_env.globals.update(get_stats=Card.serialize_stats)

@app.route('/home', methods=['GET'])
def homepage():
    """Show homepage."""
        
    shared_decks = SharedDeck.query.order_by(SharedDeck.timestamp.desc()).limit(20).all()
    
    return render_template('index.html', shared_decks=shared_decks)

#############################
######## User routes ########

@app.route('/register', methods=['GET','POST'])
def register():
    """Register user info if form validated, or display register form."""
    
    form = RegisterForm()
    
    try:
        if form.validate_on_submit():
            user = User.register(form.data)
            
            login_user(user)
            
            flash('Successfully created your account!','success')
            
            return redirect(url_for('homepage'))
    except IntegrityError as err:
        err_info = jsonify(err.orig.args[0]).get_json()
        
        if "users_username_key" in err_info:
            flash('Username already taken.', 'danger')
        if "users_email_key" in err_info:
            flash('Email already taken.', 'danger')
    
    return render_template('/user/register.html', form=form)        

@app.route('/login', methods=['GET','POST'])
def login():
    """Log in User, add to session."""
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                form.password.data)
        if user:
            login_user(user, remember=True)
            flash(f'Welcome back {user.username}!', 'info')
            
            return redirect(url_for('homepage'))
        
        flash("Invalid credentials.", 'danger')
            
    return render_template('/user/login.html', form=form)
                   
@app.route('/logout')
@login_required
def logout():
    """Log out User, remove from session."""
    
    logout_user()
    
    flash('You have been logged out.', 'info')
    
    return redirect(url_for('homepage'))

@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show user details page."""
    
    user = User.query.get_or_404(user_id)
    
    return render_template('/user/detail.html', user=user)

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Update info for current user."""
    
    user = User.query.get_or_404(user_id)   
    form = EditUserForm(obj=user)
    
    if form.validate_on_submit():
        form.populate_obj(user)
        
        db.session.commit()
        
        flash(f"{user.username}'s info has been updated.", 'info')
        
        return redirect(url_for('user_details', user_id=user_id))
    
    return render_template('/user/edit_user.html', form=form, user=user)

@app.route('/users/delete', methods=['POST'])
@login_required
def delete_user():    
    
    user = User.query.get_or_404(current_user.id)
    
    logout_user()
    db.session.delete(user)
    
    db.session.commit()
    
    flash('Deleted your account.', 'info')
    
    return redirect(url_for('homepage'))

@app.route('/users/<int:user_id>/likes')
def user_deck_likes(user_id):
    """Gets all decks that a user liked."""
    
    user = User.query.get_or_404(user_id)
    
    liked_decks = db.session.query(SharedDeck).join(DeckLikes).filter(DeckLikes.user_id == user.id).all()
    
    return render_template('/user/liked_decks.html', user=user, liked_decks=liked_decks)
    
#############################
######## Card routes ########

@app.route('/cards/<number>', methods=['GET','PATCH'])
def show_card(number):
    """Show card details."""
    
    card = Card.query.filter(Card.cardnumber == number).first()
    
    stat_list = Card.get_detail_stats(card)
    
    if request.method == 'PATCH':
        serialized_stats = Card.serialize_stats(card)
        return jsonify(serialized_stats)
    
    return render_template('/card/card_details.html', card=card, stat_list=stat_list)

@app.route('/adv_search')
def show_adv_search():
    """Show adv search page."""
    
    return render_template('/search/adv_search.html')

@app.route('/cards/advanced')
def adv_search():
    """Show adv search html."""
    
    adv_form = AdvancedSearchForm()
    
    return render_template('/card/adv_search.html',adv_form=adv_form)


#############################
######## Deck routes ########

@app.route('/decks', methods=['GET','POST'])
@login_required
def user_decks():
    """Show all decks for user and deck builder on btn click"""
        
    decks = Deck.query.filter(Deck.user_id == current_user.id).all()
    
    adv_form = AdvancedSearchForm()
    
    if request.method == 'POST':
        
        deck = request.get_json()

        decklist_ids = Deck.create_decklists()
        
        Deck.generate_decklist_cards(decklist_ids,deck)
        
        deck_img = MainDecklist.highest_dp_card_img(MainDecklist.main_cards(decklist_ids['main_id']))
        
        new_deck = Deck(
                        name=deck['name'],
                        user_id=current_user.id,
                        main_decklist_id=decklist_ids['main_id'],
                        egg_decklist_id=decklist_ids['egg_id'],
                        side_decklist_id=decklist_ids['side_id'],
                        HDP_deck_img=deck_img
                        )
        
        db.session.add(new_deck)
        db.session.commit()
                
        serialized = new_deck.serialize_deck()
                
        return (jsonify(deck=serialized), 201)
        
    return render_template('/deck/decks.html', decks=decks,adv_form=adv_form)

@app.route('/decks/<int:deck_id>', methods=['GET','POST'])
def show_deck(deck_id):
    """Shows deck, or allows deck owner to share/delete."""
    
    deck = Deck.query.get_or_404(deck_id) 

    if request.method == 'POST':
        
        db.session.delete(deck)
        db.session.commit()
        
        return redirect(url_for('user_decks'))
    
    decklist = {
        'Main': MainDecklist.main_cards(deck.main_decklist_id),
        'Egg': EggDecklist.egg_cards(deck.egg_decklist_id),
        'Side': SideDecklist.side_cards(deck.side_decklist_id)
    }
    
    def list_str_stats(stat_obj): 
        
        return [ stat + ': ' + stat_obj[stat] for stat in stat_obj if stat_obj[stat] != None and stat != 'image_url' ]

    if current_user.is_authenticated:
        user = User.query.get_or_404(current_user.id)
    
        liked_decks = db.session.query(SharedDeck).join(DeckLikes).filter(DeckLikes.user_id == user.id).all()
        
        liked_deck_ids = [deck.id for deck in liked_decks]
        
        return render_template('/deck/deck_details.html',deck=deck,decklist=decklist, list_str_stats=list_str_stats,likes=liked_deck_ids)
    else:
        return render_template('/deck/deck_details.html',deck=deck,decklist=decklist, list_str_stats=list_str_stats)

@app.route('/share/<int:deck_id>', methods=['POST'])
@login_required
def share_deck(deck_id):
    """Save shared deck."""
    
    deck = Deck.query.get_or_404(deck_id)
        
    shared_deck = SharedDeck(deck_id=deck.id,
                                user_id=deck.user.id)
    
    deck.is_shared = True
    
    db.session.add(shared_deck)
    db.session.commit()
    
    flash(f'Shared new deck {deck.name}', 'success')
    
    return redirect(url_for('homepage'))

@app.route('/decks/<int:deck_id>/likes', methods=['POST'])
@login_required
def liked_deck(deck_id):
    """Toggle deck like for logged in user and add or remove like from DeckLikes."""
    
    user = User.query.get_or_404(current_user.id)
    
    liked_deck = SharedDeck.query.filter(SharedDeck.deck_id == deck_id).first()
    
    user_likes = db.session.query(SharedDeck).join(DeckLikes).filter(DeckLikes.user_id == user.id).all()
    
    if liked_deck in user_likes:
        user_likes = [like for like in user_likes if like != liked_deck]
        like = DeckLikes.query.filter(DeckLikes.shared_deck_id == liked_deck.id).first()
        db.session.delete(like)
    else:
        user_likes.append(liked_deck)
        new_like = DeckLikes(shared_deck_id=liked_deck.id, user_id=user.id)
        
        db.session.add(new_like)
    
    db.session.commit()
    
    return redirect( url_for('show_deck',deck_id=deck_id) )