from flask import Flask, session, render_template, request, redirect, url_for, flash, g
from flask_wtf.csrf import CSRFProtect
from .utils import *
from .users import users
from .quizes import quizes
from .questions import questions
from .answers import answers
from quiz_app.utils import get_user

app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(questions)
app.register_blueprint(quizes)
app.register_blueprint(answers)

app.config['SECRET_KEY'] = 'my_secret_key'
csrf = CSRFProtect(app)

@app.before_request
def before_request():
    # Store some data in g before each request
    g.user = db_query_single('SELECT * FROM user WHERE id = %s', (session.get('id'),))


# Define the context processor
@app.context_processor
def inject_variables():
    # Determine if the user is an administrator
    is_admin = False
    is_anonymous = False
    is_regular = False
    if user := get_user():
        is_admin = user.get('is_admin')
        is_anonymous = user.get('is_anonymous')
        is_regular = user.get('is_regular')
    
    # Define the variables to be available in all templates
    return dict(is_admin=is_admin, is_anonymous=is_anonymous, is_regular=is_regular, user=user)
