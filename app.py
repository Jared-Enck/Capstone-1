from flask_cors import CORS
from flask import Flask, redirect, render_template, request, flash, jsonify, url_for, abort
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Card, MainDecklist, MainDeckCard, EggDecklist, EggDeckCard, SideDecklist, SideDeckCard, Deck, SharedDeck
from forms import RegisterForm, LoginForm

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///digimon_tcg_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '3f44cd49d69e821aa140f13a49f432b073e311a264583ab7ed4340b714da0db8'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

BASE_API_URL_1 = 'https://digimoncard.io/api-public/search.php?'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

app.jinja_env.globals.update(main_cards=MainDecklist.main_cards)
app.jinja_env.globals.update(highest_dp_card_img=MainDecklist.highest_dp_card_img)
app.jinja_env.globals.update(get_deck_comments=SharedDeck.get_deck_comments)

@app.route('/')
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
        
    
    return render_template('/User/register.html', form=form)        

@app.route('/login', methods=['GET','POST'])
def login():
    """Log in User, add to session."""
    
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate:
            user = User.authenticate(form.username.data,
                                    form.password.data)
            if user:
                login_user(user)
                flash(f'Welcome back {user.username}!', 'info')
                
                return redirect(url_for('homepage'))
            
            flash("Invalid credentials.", 'danger')
            
    return render_template('/User/login.html', form=form)
                   
@app.route('/logout')
@login_required
def logout():
    """Log out User, remove from session."""
    
    logout_user()
    
    flash('You have been logged out.', 'info')
    
    return redirect(url_for('homepage'))

@app.route('/users/<int:user_id>')
@login_required
def user_details(user_id):
    """Show user details page."""
    
    user = User.query.get_or_404(user_id)
    
    return render_template('/User/detail.html', user=user)