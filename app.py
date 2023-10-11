from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_session import Session
from database import close_db, get_db
from forms import RegistrationForm
from functools import wraps
from datetime import datetime
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "Jesus-Is-Lord"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.teardown_appcontext
def close_db_at_end_of_requests(e=None):
    close_db(e)

@app.before_request
def load_logged_in_user():
    g.username = session.get("username", None)
    g.card = session.get("bingo_card", None)

def login_required(view):
    @wraps(view)                       
    def wrapped_view(**kwargs):
        if g.username is None:
            return redirect(url_for('register', next=request.url)) 
        return view(**kwargs)
    return wrapped_view

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        db = get_db()
        if db.execute("""SELECT * FROM users
                        WHERE username = ?""", (username,)
                        ).fetchone() is not None:
                form.username.errors.append("Username already exists!")
        else:
             session["username"] = username
             bingo_card = ["Same birth month", "Same Shoe Size as You", "Who is enjoying today", "Who Likes Spicy Food", "Wearing Glasses",  "Prefers Sweet over Salty Food", "Has Held a Snake",
                "Has an Iphone", "Is an Only Child", "Fearfully and Wonderfully Made", "Prefers Tea over Coffee", "Has Never Been on a Plane", "Eaten Chips for Lunch", "Able to Juggle",
                "Here For a Good Time", "Who is Wearing a Hoodie", "Speaks Two or More Languages", "Plays an Instrument", "Plays Sport", "Who is a Night Owl", "Who is a Morning Person",
                "Who has read the bible today", "Loves Reading", "Has Blue Eyes", "Loves to Cook", "From the same county/country", "Who has Never been to a Concert", "Have Eaten Snails",
                "Haven't Watched Barbie", "Has lived in More than One Country", "Is The Youngest Child", "Has a Driving License", "Have a Pet", "Has a Tattoo", "Has a Piercing"]
    
             bingo_card = random.sample(bingo_card, 25)
             session['bingo_card'] = bingo_card
             
             return redirect(url_for("bingo"))
    return render_template('registration.html', form=form)

@app.route('/bingo')
@login_required
def bingo():
    g.card = session.get("bingo_card", None)
    return render_template('bingo.html', bingo_card=g.card)
