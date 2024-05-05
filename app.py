from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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

    def __init__(self, name, description=None):
        self.name = name
        self.description = description


class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('flashcard_deck.id'), nullable=False)
    deck = db.relationship('FlashcardDeck', backref=db.backref('flashcards', lazy=True))

    def __init__(self, question, answer, deck_id):
        self.question = question
        self.answer = answer
        self.deck_id = deck_id


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
            return "Benutzername oder E-Mail bereits verwendet!"

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
            return redirect('/dashboard')
        else:
            return 'Ungültige Anmeldedaten!'

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


@app.route('/login-guest', methods=['POST'])
def login_guest():
    # Assign a temporary user_id for guest
    session['user_id'] = 'guest'
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        # Redirect to login if not logged in or if the session is not established.
        return redirect('/login')
    return render_template('dashboard.html')


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to login if user is not logged in
    return render_template('profile.html')


@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect('/login')  # Ensure the user is logged in

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
        # Log out the user and redirect to the login page for re-authentication
        session.pop('user_id', None)
        return redirect('/login')

    return render_template('change_password.html')


@app.route('/learning-sets')
def learning_sets():
    decks = FlashcardDeck.query.all()
    return render_template('learning_sets.html', decks=decks)

@app.route('/new-deck', methods=['GET', 'POST'])
def new_deck():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        if name:
            new_deck = FlashcardDeck(name=name, description=description)
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


if __name__ == '__main__':
    app.run(debug=True)
