from flask_cors import CORS
from flask import Flask, redirect, render_template, request, flash, jsonify, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Card, MainDecklist, EggDecklist, SideDecklist, Deck, SharedDeck
from forms import RegisterForm, LoginForm, EditUserForm,AdvancedSearchForm

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///digimon_tcg_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '3f44cd49d69e821aa140f13a49f432b073e311a264583ab7ed4340b714da0db8'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
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

app.jinja_env.globals.update(main_cards=MainDecklist.main_cards)
app.jinja_env.globals.update(egg_cards=EggDecklist.egg_cards)
app.jinja_env.globals.update(side_cards=SideDecklist.side_cards)
app.jinja_env.globals.update(highest_dp_card_img=MainDecklist.highest_dp_card_img)
app.jinja_env.globals.update(get_deck_comments=SharedDeck.get_deck_comments)

@app.route('/', methods=['GET'])
def homepage():
    """Show homepage."""
    
    shared_decks = SharedDeck.query.order_by(SharedDeck.timestamp.desc()).limit(10).all()
    
    return render_template('index.html', shared_decks=shared_decks)

############################
######## User views ########

@app.route('/register', methods=['GET','POST'])
def register():
    """Register user info if form validated, or display register form."""
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        user = User.register(form.data)
        
        login_user(user)
        
        flash('Successfully created your account!','success')
        
        return redirect(url_for('homepage'))
        
    
    return render_template('/user/register.html', form=form)        

@app.route('/login', methods=['GET','POST'])
def login():
    """Log in User, add to session."""
    
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate:
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
        
        flash(f"{user.username}'s info has been updated.", 'success')
        
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
    
############################
######## Card views ########

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


############################
######## Deck views ########

@app.route('/decks', methods=['GET','POST'])
@login_required
def user_decks():
    """Show all decks for user and deck builder on btn click"""
    
    decks = Deck.user_decks(current_user)
    
    adv_form = AdvancedSearchForm()
    
    if request.method == 'POST':
        
        deck = request.get_json()

        decklist_ids = Deck.create_decklists(deck)
        
        new_deck = Deck(
                        name=deck['name'],
                        user_id=current_user.id,
                        main_decklist_id=decklist_ids['main_id'],
                        egg_decklist_id=decklist_ids['egg_id'],
                        side_decklist_id=decklist_ids['side_id']
                        )
        
        db.session.add(new_deck)
        db.session.commit()
        
        flash(f'Saved new deck {new_deck.name}', 'success')
        
        return redirect(url_for('homepage'))
        
    return render_template('/deck/decks.html', decks=decks,adv_form=adv_form)

@app.route('/decks/<int:deck_id>')
def show_deck(deck_id):
    """Shows deck, or allows deck owner to edit."""
    
    deck = Deck.query.get_or_404(deck_id)
    
    return render_template('/deck/deck_details.html',deck=deck)