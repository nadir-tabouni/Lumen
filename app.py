from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, session, flash
import random

app = Flask(__name__)
app.secret_key = 'secret_key'

# db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lumenDB.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))


class FlashcardDeck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('decks', lazy=True))

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id


class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('flashcard_deck.id'), nullable=False)
    deck = db.relationship('FlashcardDeck', backref=db.backref('flashcards', lazy='dynamic'))


@app.before_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username or email already exists
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            return "Username or email already in use!"

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert new user into the database
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and the password is correct
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect('/learning-hub')
        else:
            return 'Invalid login credentials!'

    return render_template('login.html')


@app.route('/login-guest', methods=['POST'])
def login_guest():
    # Assign a temporary user_id for guest
    session['user_id'] = 'guest'
    return redirect('/learning-hub')


@app.route('/learning-hub')
def learning_hub():
    if 'user_id' not in session:
        # Redirect to login if not logged in or if the session is not established.
        return redirect('/login')
    return render_template('learning_hub.html')


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to login if user is not logged in

    is_guest = session.get('user_id') == 'guest'
    return render_template('profile.html', is_guest=is_guest)


@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session or session['user_id'] == 'guest':
        flash('Access denied: guests cannot change passwords.', 'error')
        return redirect('/profile')  # Redirect guests trying to access directly

    user = User.query.get(session['user_id'])
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']

        if not check_password_hash(user.password_hash, old_password):
            return "Old password is incorrect!"

        if new_password != confirm_new_password:
            return "New passwords do not match!"

        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        flash('Password changed successfully.', 'info')
        session.pop('user_id', None)  # Log out the user
        return redirect('/login')

    return render_template('change_password.html')


@app.route('/learning-sets')
def learning_sets():
    user_id = session.get('user_id')
    if user_id == 'guest':
        decks = FlashcardDeck.query.filter_by(user_id=0).all()
    else:
        decks = FlashcardDeck.query.filter_by(user_id=user_id).all()
    return render_template('learning_sets.html', decks=decks)


@app.route('/new-deck', methods=['GET', 'POST'])
def new_deck():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        user_id = session.get('user_id')
        if user_id == 'guest':
            user_id = 0  # Guests have no user_id
            existing_deck = FlashcardDeck.query.filter_by(user_id=0).first()
            if existing_deck:
                flash('Guests can only create one deck. Please register for an account to create more decks.')
                return redirect('/learning-sets')

        if name:
            new_deck = FlashcardDeck(name=name, description=description, user_id=user_id)
            db.session.add(new_deck)
            db.session.commit()
            return redirect('/learning-sets')
    return render_template('new_deck.html')


@app.route('/deck/<int:deck_id>')
def view_deck(deck_id):
    deck = FlashcardDeck.query.get_or_404(deck_id)
    return render_template('view_deck.html', deck=deck)


@app.route('/deck/<int:deck_id>/add-flashcard', methods=['GET', 'POST'])
def add_flashcard(deck_id):
    deck = FlashcardDeck.query.get_or_404(deck_id)
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        if question and answer:
            flashcard = Flashcard(question=question, answer=answer, deck_id=deck.id)
            db.session.add(flashcard)
            db.session.commit()
            return redirect(f'/deck/{deck_id}')
    return render_template('add_flashcard.html', deck=deck)


@app.route('/flashcard/<int:flashcard_id>/edit', methods=['GET', 'POST'])
def edit_flashcard(flashcard_id):
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    if request.method == 'POST':
        flashcard.question = request.form['question']
        flashcard.answer = request.form['answer']
        db.session.commit()
        flash('Flashcard updated successfully.')
        return redirect(f'/deck/{flashcard.deck_id}')
    return render_template('edit_flashcard.html', flashcard=flashcard)


@app.route('/deck/<int:deck_id>/delete', methods=['POST'])
def delete_deck(deck_id):
    deck = FlashcardDeck.query.get_or_404(deck_id)
    try:
        # First, remove all associated flashcards to avoid foreign key constraint errors
        Flashcard.query.filter_by(deck_id=deck_id).delete()
        # Now, remove the deck itself
        db.session.delete(deck)
        db.session.commit()
        flash('Deck deleted successfully.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting deck: ' + str(e), 'error')
    return redirect('/learning-sets')


@app.route('/flashcard/<int:flashcard_id>/delete', methods=['POST'])
def delete_flashcard(flashcard_id):
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    if flashcard:
        db.session.delete(flashcard)
        db.session.commit()
        flash('Flashcard deleted successfully.')
    else:
        flash('Flashcard not found.')
    return redirect(request.referrer or '/learning-sets')


@app.route('/deck/<int:deck_id>/learn')
def learn_deck(deck_id):
    deck = FlashcardDeck.query.get_or_404(deck_id)
    flashcards = deck.flashcards.all()
    flashcards_list = [{"id": flashcard.id, "question": flashcard.question, "answer": flashcard.answer} for flashcard in flashcards]
    return render_template('learn_deck.html', deck=deck, flashcards=flashcards_list)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if session.get('user_id') == 'guest':
        # Delete guest decks on logout
        Flashcard.query.filter(Flashcard.deck.has(user_id=0)).delete()
        FlashcardDeck.query.filter_by(user_id=0).delete()
        db.session.commit()
    session.pop('user_id', None)
    return redirect('/')


@app.route('/browse-decks', methods=['GET', 'POST'])
def browse_decks():
    search_query = request.form.get('search', '')

    query = FlashcardDeck.query
    if search_query:
        query = query.filter(FlashcardDeck.name.contains(search_query))

    decks = query.all()
    return render_template('browse_decks.html', decks=decks, search_query=search_query)


@app.route('/deck/<int:deck_id>/edit', methods=['GET', 'POST'])
def edit_deck(deck_id):
    deck = FlashcardDeck.query.get_or_404(deck_id)
    if request.method == 'POST':
        deck.name = request.form['name']
        deck.description = request.form['description']
        db.session.commit()
        flash('Deck updated successfully.')
        return redirect(f'/deck/{deck_id}')
    return render_template('edit_deck.html', deck=deck)


if __name__ == '__main__':
    app.run(debug=True)
